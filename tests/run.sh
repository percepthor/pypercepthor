#!/bin/bash
# Runs the pypercepthor test suite inside the test container.
#
# The package, pycerver and auth-service are bind-mounted from their working trees and
# go first in PYTHONPATH, so edits take effect on the next run with no rebuild. Rebuild
# (./build.sh) when cerver, libauth, requirements.txt or tests/Dockerfile change.
#
# unit and integration need nothing but the image. The e2e tier runs auth-service
# against the MongoDB and the Redis of tests/docker-compose.test.yml
# (./run.sh mongo, ./run.sh redis), the packages-test-* containers of the
# packages-tests compose project, shared with the suite of py-cerver. Without them the
# e2e tests skip with an explicit reason.

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

IMAGE_NAME="itpercepthor/pypercepthor:tests"
ASAN_IMAGE_NAME="itpercepthor/pypercepthor:tests-address-undefined"

# TESTS_CONTAINER_NAME overrides the container name, to run two sessions of the suite at once
CONTAINER_NAME="${TESTS_CONTAINER_NAME:-pypercepthor-tests}"

PACKAGE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PYCERVER_DIR="${PYCERVER_DIR:-/Users/ermiry/Documents/py-cerver}"
AUTH_SERVICE_DIR="${AUTH_SERVICE_DIR:-/Users/ermiry/Documents/Work/percepthor-backend/auth-service}"

TESTS_COMPOSE="${PACKAGE_ROOT}/tests/docker-compose.test.yml"

MONGO_CONTAINER="packages-test-mongo"
MONGO_SERVICE="mongo-test"
MONGO_TEST_PORT="${MONGO_TEST_PORT:-27022}"

REDIS_CONTAINER="packages-test-redis"
REDIS_SERVICE="redis-test"
REDIS_TEST_PORT="${REDIS_TEST_PORT:-6396}"

# the profile of hypothesis: ci (the default runs) or nightly (./run.sh fuzz)
HYPOTHESIS_PROFILE="${HYPOTHESIS_PROFILE:-ci}"

DOCKER_RUN_ARGS=(
	--rm
	--name "${CONTAINER_NAME}"
	--add-host=host.docker.internal:host-gateway
	-e MONGO_TEST_HOST=host.docker.internal
	-e MONGO_TEST_PORT="${MONGO_TEST_PORT}"
	-e REDIS_TEST_HOST=host.docker.internal
	-e REDIS_TEST_PORT="${REDIS_TEST_PORT}"
	-e HYPOTHESIS_PROFILE="${HYPOTHESIS_PROFILE}"
	-v "${PACKAGE_ROOT}:/home/pypercepthor"
	-v "${PYCERVER_DIR}:/home/pycerver:ro"
	-v "${AUTH_SERVICE_DIR}:/home/auth:ro"
)

# MongoDB and Redis lifecycle does not need the test image
case "$1" in
	"mongo")
		if docker ps --format '{{.Names}}' | grep -qx "${MONGO_CONTAINER}"; then
			echo -e "${GREEN}Test MongoDB already running (shared by the package suites)${NC}"
			exit 0
		fi

		echo -e "${YELLOW}Starting test MongoDB...${NC}"
		docker compose -f "${TESTS_COMPOSE}" up -d --wait "${MONGO_SERVICE}"
		exit $?
		;;
	"redis")
		if docker ps --format '{{.Names}}' | grep -qx "${REDIS_CONTAINER}"; then
			echo -e "${GREEN}Test Redis already running (shared by the package suites)${NC}"
			exit 0
		fi

		echo -e "${YELLOW}Starting test Redis...${NC}"
		docker compose -f "${TESTS_COMPOSE}" up -d "${REDIS_SERVICE}"
		exit $?
		;;
	"mongo-down")
		echo -e "${YELLOW}Stopping the test MongoDB and Redis (the other package suites use them too)...${NC}"
		docker compose -f "${TESTS_COMPOSE}" down
		exit $?
		;;
	"redis-down")
		echo -e "${YELLOW}Stopping test Redis (the other package suites use it too)...${NC}"
		docker compose -f "${TESTS_COMPOSE}" rm --stop --force "${REDIS_SERVICE}"
		exit $?
		;;
esac

RUN_IMAGE="${IMAGE_NAME}"
if [ "$1" == "asan" ]; then
	RUN_IMAGE="${ASAN_IMAGE_NAME}"
fi

# TESTS_IMAGE runs another tag, the one that build.sh built with it
RUN_IMAGE="${TESTS_IMAGE:-${RUN_IMAGE}}"

if ! docker image inspect "${RUN_IMAGE}" > /dev/null 2>&1; then
	echo -e "${RED}✗ Test image not found: ${RUN_IMAGE}${NC}"
	echo -e "${YELLOW}Run ./build.sh first (SANITIZER=address,undefined ./build.sh for asan)${NC}"
	exit 1
fi

echo -e "${GREEN}=== Running pypercepthor Tests in Docker ===${NC}"

# Arguments passed to pytest inside the container, relative to tests/.
# A tier keyword forwards whatever follows it: ./run.sh unit -k validation
PYTEST_ARGS=()
RUN_COMMAND=()

case "$1" in
	"")
		echo -e "${YELLOW}Running unit and integration tests...${NC}"
		;;
	"unit")
		PYTEST_ARGS=(unit/ "${@:2}")
		;;
	"integration")
		PYTEST_ARGS=(integration/ "${@:2}")
		;;
	"e2e")
		# serial: one auth-service and one cerver for the whole tier
		PYTEST_ARGS=(e2e/ "${@:2}")
		;;
	"coverage")
		PYTEST_ARGS=(
			--cov=/home/pypercepthor/percepthor
			--cov-report=term
			--cov-report=html:/home/pypercepthor/tests/htmlcov
			unit/ integration/ e2e/
		)
		;;
	"fast")
		PYTEST_ARGS=(-n auto unit/ "${@:2}")
		;;
	"asan")
		# the python interpreter is not instrumented: the runtime of the sanitizers is preloaded,
		# and the leaks are not checked because CPython does not release its memory at exit
		echo -e "${YELLOW}Running unit and integration tests with address and undefined sanitizers...${NC}"
		DOCKER_RUN_ARGS+=(
			-e LD_PRELOAD="/opt/gcc/lib64/libasan.so.8:/opt/gcc/lib64/libubsan.so.1"
			-e ASAN_OPTIONS="detect_leaks=0:abort_on_error=1:halt_on_error=1"
			-e UBSAN_OPTIONS="print_stacktrace=1:halt_on_error=1"
		)
		PYTEST_ARGS=(-p no:cacheprovider unit/ integration/ "${@:2}")
		;;
	"fuzz")
		echo -e "${YELLOW}Running the fuzz tests with the nightly profile...${NC}"
		DOCKER_RUN_ARGS+=(-e HYPOTHESIS_PROFILE=nightly)
		PYTEST_ARGS=(-m fuzz unit/ "${@:2}")
		;;
	"repeat")
		# ./run.sh repeat <test> [count]: stops at the first failure, to find a flaky test
		TARGET="$2"
		COUNT="${3:-100}"
		if [ -z "${TARGET}" ]; then
			echo -e "${RED}usage: ./run.sh repeat <test> [count]${NC}"
			exit 2
		fi

		RUN_COMMAND=(bash -c "for run in \$(seq 1 ${COUNT}); do pytest -q -p no:cacheprovider '${TARGET}' > /tmp/repeat.log 2>&1 || { tail -n 64 /tmp/repeat.log; echo 'failed in run '\$run' of ${COUNT}'; exit 1; }; done; echo 'passed ${COUNT} runs'")
		;;
	"shell")
		docker run -it "${DOCKER_RUN_ARGS[@]}" "${RUN_IMAGE}" /bin/bash
		exit $?
		;;
	*)
		PYTEST_ARGS=("$@")
		;;
esac

if [ ${#RUN_COMMAND[@]} -gt 0 ]; then
	docker run "${DOCKER_RUN_ARGS[@]}" "${RUN_IMAGE}" "${RUN_COMMAND[@]}"
else
	docker run "${DOCKER_RUN_ARGS[@]}" "${RUN_IMAGE}" pytest "${PYTEST_ARGS[@]}"
fi

exit_code=$?

if [ $exit_code -eq 0 ]; then
	echo -e "${GREEN}✓ All tests passed!${NC}"
else
	echo -e "${RED}✗ Some tests failed${NC}"
fi

exit $exit_code
