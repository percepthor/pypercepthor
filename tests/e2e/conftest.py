"""e2e tier: routes of percepthor authenticated by libauth against a real auth-service.

`auth_service` generates an RSA pair for the session, writes the identity of the
instance in Redis (the keys `percepthor_service_configuration` reads at boot), starts
the working tree of auth-service as a subprocess against packages-test-mongo and the
base 0 of packages-test-redis, and waits for `/api/auth/version`. `service_cerver`
starts, in a thread of pytest, a web cerver whose routes are registered with
percepthor and whose AuthService points to that auth-service. Every test mints its
JWT with the private key and writes the token, role and permission keys that the
other services write in production. The tier is serial: one auth-service, one cerver.

Without MongoDB or Redis every test is skipped with its reason.
"""

from bson import ObjectId
from bson import json_util
import http.client
import json
import jwt
import os
import pytest
import redis
import signal
import socket
import subprocess
import threading
import time
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cerver import CERVER_HANDLER_TYPE_THREADS
from cerver import cerver_create_web
from cerver import cerver_set_handler_type
from cerver import cerver_set_reusable_address_flags
from cerver import cerver_set_thpool_n_threads
from cerver import cerver_shutdown
from cerver import cerver_start
from cerver import cerver_teardown
from cerver.http import HTTP_STATUS_OK
from cerver.http import HTTP_STATUS_UNAUTHORIZED
from cerver.http import REQUEST_METHOD_GET
from cerver.http import REQUEST_METHOD_POST
from cerver.http import http_cerver_get
from cerver.http import http_cerver_set_custom_data
from cerver.http import http_request_get_custom_data
from cerver.http import http_request_get_param_at_idx
from cerver.http import http_response_json_custom_reference_send
from cerver.http import http_response_json_key_value_send

from percepthor import PERMISSIONS_TYPE_ORGANIZATION
from percepthor import PERMISSIONS_TYPE_PROJECT
from percepthor import auth_service_create
from percepthor import auth_service_delete
from percepthor import percepthor_auth_get_admin
from percepthor import percepthor_auth_get_mask
from percepthor import percepthor_auth_get_permissions
from percepthor import percepthor_auth_get_resource
from percepthor import percepthor_auth_get_token_id
from percepthor import percepthor_auth_get_token_organization
from percepthor import percepthor_auth_get_token_role
from percepthor import percepthor_auth_get_token_user
from percepthor import percepthor_auth_permissions_iter_get_next
from percepthor import percepthor_auth_permissions_iter_start
from percepthor import percepthor_group_create
from percepthor import percepthor_route
from percepthor import percepthor_single_authentication
from percepthor import permissions_get_resource

MONGO_TEST_HOST = os.environ.get ("MONGO_TEST_HOST", "localhost")
MONGO_TEST_PORT = int (os.environ.get ("MONGO_TEST_PORT", "27022"))

REDIS_TEST_HOST = os.environ.get ("REDIS_TEST_HOST", "localhost")
REDIS_TEST_PORT = int (os.environ.get ("REDIS_TEST_PORT", "6396"))

E2E_SKIP_REASON = (
	"the e2e tier needs packages-test-mongo and packages-test-redis: ./run.sh mongo && ./run.sh redis"
)

AUTH_SERVICE_ROOT = Path ("/home/auth")

AUTH_DATABASE = "pypercepthor_e2e"
AUTH_INSTANCE = "auth-e2e"
# fixed, the tests import them from this module and pytest imports it on its own
AUTH_INSTANCE_REFERENCE = "6560a1b2c3d4e5f6a7b8c901"
AUTH_SERVICE_REFERENCE = "6560a1b2c3d4e5f6a7b8c902"
AUTH_LOGS_EXPIRATION = 60

AUTH_ADDRESS = "127.0.0.1"
AUTH_PORT = 5020
AUTH_CHECK_URL = f"http://{AUTH_ADDRESS}:{AUTH_PORT}/api/auth/check"

AUTH_BOOT_TIMEOUT_SECONDS = 60
AUTH_POLL_SECONDS = 0.25
AUTH_STOP_TIMEOUT_SECONDS = 10

AUTH_LOG_NAME = "auth-e2e.log"

SERVICE_NAME = "pypercepthor-e2e"
SERVICE_REFERENCE = "6560a1b2c3d4e5f6a7b8c903"
SERVICE_PORT = 5097
SERVICE_THREADS = 8
SERVICE_CONNECTION_QUEUE = 16

CONNECT_TIMEOUT_SECONDS = 2
REQUEST_TIMEOUT_SECONDS = 40

KEY_SIZE = 2048
KEY_EXPONENT = 65537

ACTION_READ = "e2e.read"
ROLE_NAME = "e2e-role"

TOKEN_STATUS_AVAILABLE = 1
TOKEN_STATUS_REVOKED = 4

TOKEN_TYPE_NORMAL = 1
TOKEN_TYPE_USER = 4

TOKEN_PERMISSIONS_SCOPE_ALL = 7
TOKEN_PERMISSIONS_SCOPE_SERVICES = 2

def _port_is_open (host: str, port: int) -> bool:
	with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as connection:
		connection.settimeout (CONNECT_TIMEOUT_SECONDS)
		return connection.connect_ex ((host, port)) == 0

def pytest_collection_modifyitems (config, items):
	if (not (_port_is_open (MONGO_TEST_HOST, MONGO_TEST_PORT) and _port_is_open (REDIS_TEST_HOST, REDIS_TEST_PORT))):
		for item in items:
			if ("/e2e/" in str (item.fspath)):
				item.add_marker (pytest.mark.skip (reason=E2E_SKIP_REASON))

	for item in items:
		if ("/e2e/" in str (item.fspath)):
			item.add_marker (pytest.mark.e2e)

@pytest.fixture (scope="session")
def redis_client ():
	client = redis.Redis (host=REDIS_TEST_HOST, port=REDIS_TEST_PORT, db=0, decode_responses=True)
	client.flushdb ()

	yield client

	client.flushdb ()
	client.close ()

@pytest.fixture (scope="session")
def keys (tmp_path_factory) -> dict:
	"""The RSA pair of the session: auth-service verifies with the public key, the tests sign with the private one."""
	private_key = rsa.generate_private_key (public_exponent=KEY_EXPONENT, key_size=KEY_SIZE)

	directory = tmp_path_factory.mktemp ("keys")
	public_path = directory / "key.pub"
	public_path.write_bytes (private_key.public_key ().public_bytes (
		serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
	))

	other_key = rsa.generate_private_key (public_exponent=KEY_EXPONENT, key_size=KEY_SIZE)

	return {
		"private": private_key.private_bytes (
			serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption ()
		),
		"other": other_key.private_bytes (
			serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption ()
		),
		"public_path": str (public_path)
	}

def _auth_boot_keys (client):
	"""The identity of the instance, written in production by controller-service."""
	client.set (f"service:instance:{AUTH_INSTANCE}:reference", AUTH_INSTANCE_REFERENCE)
	client.set (f"service:instance:{AUTH_INSTANCE_REFERENCE}:info", json.dumps ({"service": AUTH_SERVICE_REFERENCE}))
	client.set (f"service:instance:{AUTH_INSTANCE_REFERENCE}:configuration", json.dumps ({"logs_exp": AUTH_LOGS_EXPIRATION}))

def _auth_environment (keys: dict) -> dict:
	environment = dict (os.environ)
	environment.update ({
		"RUNTIME": "test",
		"PORT": str (AUTH_PORT),
		"CERVER_RECEIVE_BUFFER_SIZE": "4096",
		"CERVER_POOL_THREADS": "8",
		"CERVER_CONNECTION_QUEUE": "16",
		"SERVICE_INSTANCE": AUTH_INSTANCE,
		"MONGO_APP_NAME": AUTH_INSTANCE,
		"MONGO_DB": AUTH_DATABASE,
		"MONGO_URI": f"mongodb://{MONGO_TEST_HOST}:{MONGO_TEST_PORT}/{AUTH_DATABASE}",
		"CACHE_HOSTNAME": REDIS_TEST_HOST,
		"CACHE_PORT": str (REDIS_TEST_PORT),
		"PUB_KEY": keys["public_path"]
	})

	return environment

def _auth_ready () -> bool:
	try:
		connection = http.client.HTTPConnection (AUTH_ADDRESS, AUTH_PORT, timeout=CONNECT_TIMEOUT_SECONDS)
		connection.request ("GET", "/api/auth/version")
		status = connection.getresponse ().status
		connection.close ()

		return status == HTTP_STATUS_OK

	except OSError:
		return False

@pytest.fixture (scope="session")
def auth_service (redis_client, keys, tmp_path_factory):
	_auth_boot_keys (redis_client)

	log_path = tmp_path_factory.mktemp ("logs") / AUTH_LOG_NAME
	log_file = open (log_path, "w")

	process = subprocess.Popen (
		["python3", "-u", "service/main.py"],
		cwd=AUTH_SERVICE_ROOT, env=_auth_environment (keys),
		stdout=log_file, stderr=subprocess.STDOUT
	)

	deadline = time.monotonic () + AUTH_BOOT_TIMEOUT_SECONDS
	while ((time.monotonic () < deadline) and (process.poll () is None) and (not _auth_ready ())):
		time.sleep (AUTH_POLL_SECONDS)

	if (not _auth_ready ()):
		process.kill ()
		log_file.close ()
		pytest.fail (f"auth-service did not start:\n{log_path.read_text ()[-4000:]}")

	yield process

	process.send_signal (signal.SIGINT)

	try:
		process.wait (timeout=AUTH_STOP_TIMEOUT_SECONDS)

	except subprocess.TimeoutExpired:
		process.kill ()

	log_file.close ()

def _auth_values (request) -> dict:
	"""The values that libauth set as the custom data of the request."""
	auth = http_request_get_custom_data (request)

	resources = list ()
	if (percepthor_auth_permissions_iter_start (auth)):
		permissions = percepthor_auth_permissions_iter_get_next (auth)
		while (permissions):
			resources.append (permissions_get_resource (permissions).decode ("utf-8"))
			permissions = percepthor_auth_permissions_iter_get_next (auth)

	return {
		"token": (percepthor_auth_get_token_id (auth) or b"").decode ("utf-8"),
		"organization": (percepthor_auth_get_token_organization (auth) or b"").decode ("utf-8"),
		"user": (percepthor_auth_get_token_user (auth) or b"").decode ("utf-8"),
		"role": (percepthor_auth_get_token_role (auth) or b"").decode ("utf-8"),
		"mask": percepthor_auth_get_mask (auth),
		"admin": percepthor_auth_get_admin (auth),
		"resource": (percepthor_auth_get_resource (auth) or b"").decode ("utf-8"),
		"resources": resources
	}

def _send_auth_values (http_receive, request):
	body = json.dumps (_auth_values (request)).encode ("utf-8")

	http_response_json_custom_reference_send (http_receive, HTTP_STATUS_OK, body, len (body))

def e2e_handler (http_receive, request):
	_send_auth_values (http_receive, request)

def e2e_public_handler (http_receive, request):
	http_response_json_key_value_send (http_receive, HTTP_STATUS_OK, b"public", b"true")

# GET /api/e2e/single/:id authenticates itself with the resource of its path
def e2e_single_handler (http_receive, request):
	resource = http_request_get_param_at_idx (request, 0)

	if (not percepthor_single_authentication (http_receive, request, resource.contents.str)):
		_send_auth_values (http_receive, request)

	else:
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_UNAUTHORIZED, b"error", b"Failed authentication!"
		)

def _service_routes (http_cerver):
	api = percepthor_group_create (http_cerver, "api/e2e")

	percepthor_route (api, REQUEST_METHOD_GET, "token", e2e_handler)
	percepthor_route (api, REQUEST_METHOD_POST, "action", e2e_handler, action=ACTION_READ)
	percepthor_route (api, REQUEST_METHOD_GET, "role", e2e_handler, role=ROLE_NAME)
	percepthor_route (api, REQUEST_METHOD_GET, "role/action", e2e_handler, role=ROLE_NAME, action=ACTION_READ)
	percepthor_route (api, REQUEST_METHOD_GET, "service", e2e_handler, service=True)
	percepthor_route (api, REQUEST_METHOD_GET, "management", e2e_handler, management=PERMISSIONS_TYPE_PROJECT, action=ACTION_READ)
	percepthor_route (api, REQUEST_METHOD_GET, "single/:id", e2e_single_handler, single=PERMISSIONS_TYPE_ORGANIZATION, action=ACTION_READ)
	percepthor_route (api, REQUEST_METHOD_GET, "public", e2e_public_handler, public=True)

@pytest.fixture (scope="session")
def service_cerver (auth_service):
	cerver = cerver_create_web (SERVICE_NAME.encode ("utf-8"), SERVICE_PORT, SERVICE_CONNECTION_QUEUE)
	cerver_set_handler_type (cerver, CERVER_HANDLER_TYPE_THREADS)
	cerver_set_thpool_n_threads (cerver, SERVICE_THREADS)
	cerver_set_reusable_address_flags (cerver, True)

	http_cerver = http_cerver_get (cerver)

	auth_service_reference = auth_service_create (
		SERVICE_REFERENCE.encode ("utf-8"), SERVICE_NAME.encode ("utf-8"), AUTH_CHECK_URL.encode ("utf-8")
	)

	http_cerver_set_custom_data (http_cerver, auth_service_reference)

	_service_routes (http_cerver)

	thread = threading.Thread (target=cerver_start, args=(cerver,), daemon=True)
	thread.start ()

	deadline = time.monotonic () + AUTH_BOOT_TIMEOUT_SECONDS
	while ((time.monotonic () < deadline) and (not _port_is_open (AUTH_ADDRESS, SERVICE_PORT))):
		time.sleep (AUTH_POLL_SECONDS)

	yield cerver

	cerver_shutdown (cerver)
	thread.join (timeout=AUTH_STOP_TIMEOUT_SECONDS)

	http_cerver_set_custom_data (http_cerver, None)
	cerver_teardown (cerver)

	auth_service_delete (auth_service_reference)

class E2EResponse:

	def __init__ (self, status: int, body: dict | None):
		self.status = status
		self.body = body

def e2e_get (path: str, token: str | None = None, method: str = "GET") -> E2EResponse:
	"""A request to the cerver of percepthor, with the token as a bearer when there is one."""
	headers = dict ()
	if (token):
		headers["Authorization"] = f"Bearer {token}"

	connection = http.client.HTTPConnection (AUTH_ADDRESS, SERVICE_PORT, timeout=REQUEST_TIMEOUT_SECONDS)
	connection.request (method, path, headers=headers)

	response = connection.getresponse ()
	raw = response.read ()
	connection.close ()

	body = None
	try:
		body = json.loads (raw)

	except ValueError:
		pass

	return E2EResponse (response.status, body)

def e2e_auth_check (body: dict, token: str) -> int:
	"""A POST to /api/auth/check of auth-service, like libauth or a direct caller sends it, returns its status."""
	connection = http.client.HTTPConnection (AUTH_ADDRESS, AUTH_PORT, timeout=REQUEST_TIMEOUT_SECONDS)
	connection.request (
		"POST", "/api/auth/check", body=json.dumps (body),
		headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
	)

	response = connection.getresponse ()
	response.read ()
	connection.close ()

	return response.status

class E2EIdentity:
	"""The ids of a token and the keys of Redis behind it, written like the other services do."""

	def __init__ (self, client, keys: dict, token_type: int = TOKEN_TYPE_USER):
		self.client = client
		self.keys = keys

		self.token = str (ObjectId ())
		self.organization = str (ObjectId ())
		self.role = str (ObjectId ())
		self.user = str (ObjectId ())
		self.token_type = token_type

	def claims (self) -> dict:
		claims = {
			"iat": int (time.time ()),
			"id": self.token,
			"organization": self.organization,
			"t_type": self.token_type,
			"user": self.user
		}

		if (self.token_type == TOKEN_TYPE_USER):
			claims["role"] = self.role
			claims["username"] = "e2e"

		else:
			claims["permissions"] = str (ObjectId ())

		return claims

	def jwt (self, key: str = "private") -> str:
		return jwt.encode (self.claims (), self.keys[key], algorithm="RS256")

	def token_data (self, status: int = TOKEN_STATUS_AVAILABLE):
		self.client.set (f"token:{self.token}:data", json_util.dumps ({"_id": ObjectId (self.token), "status": status}))

	def token_permissions (self, scope: int = TOKEN_PERMISSIONS_SCOPE_ALL, service_actions: list | None = None):
		self.client.set (f"token:{self.token}:permissions", json_util.dumps ({
			"scope": scope,
			"role": ObjectId (self.role),
			"user": ObjectId (self.user),
			"service_actions": service_actions or list ()
		}))

	def role_actions (self, *actions):
		self.client.sadd (f"roles:{self.role}:actions", *actions)

	def role_name (self, name: str):
		self.client.set (f"roles:{self.role}:name", name)

	def admin (self):
		self.client.sadd ("roles:admin", self.role)

	def user_service_permissions (self, service: str, mask: int):
		self.client.set (
			f"user:{self.user}:service:permissions",
			json.dumps ({"matches": [{"service": service, "actions_mask": mask}]})
		)

	def organization_service_mask (self, service: str, mask: int):
		self.client.set (f"organization:{self.organization}:service:{service}:mask", str (mask))

	def resource_actions (self, resource: str, permissions_type: int, *actions):
		key = f"user:{self.user}:auth:resource:{resource}:{permissions_type}:permissions"
		self.client.sadd (key, *actions)
		self.client.sadd (f"user:{self.user}:auth:resource:permissions", key)

@pytest.fixture
def identity (redis_client, keys, service_cerver):
	return E2EIdentity (redis_client, keys)

@pytest.fixture
def api_key (redis_client, keys, service_cerver):
	return E2EIdentity (redis_client, keys, TOKEN_TYPE_NORMAL)
