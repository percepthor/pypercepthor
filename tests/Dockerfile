# syntax=docker/dockerfile:1
# the test image of pypercepthor: cerver and libauth compiled from their local sources,
# with the sanitizer of the variant; pycerver, pypercepthor and auth-service are mounted
# by run.sh and put first in PYTHONPATH, so the suite always tests the working trees
# build with --build-context cerver=<path> --build-context auth=<path>
# --build-context authservice=<path> (see build.sh)

ARG SANITIZER=''

ARG RUNTIME_DEPS='libssl3t64 libcurl4t64 libbrotli1 zlib1g'

ARG PYMONGO_VERSION=3.12.2
ARG PYMONGOOSE_VERSION=1.3.8

FROM gcc:16.2 AS builder

ARG SANITIZER

RUN apt-get update && apt-get install -y libssl-dev libcurl4-openssl-dev zlib1g-dev && apt-get clean

# cerver
COPY --from=cerver . /opt/cerver
RUN cd /opt/cerver \
	&& make clean \
	&& make TYPE=test SANITIZER=${SANITIZER} ZLIB=1 -j4 \
	&& make TYPE=test SANITIZER=${SANITIZER} ZLIB=1 install \
	&& make clean

# libauth
COPY --from=auth . /opt/auth
RUN cd /opt/auth \
	&& make clean \
	&& make TYPE=test SANITIZER=${SANITIZER} -j4 \
	&& make TYPE=test SANITIZER=${SANITIZER} install \
	&& make clean

COPY tests/probe /opt/probe
RUN gcc -Wall -I /usr/local/include /opt/probe/probe.c -o /opt/probe/probe

############
FROM python:3.14.10-slim-trixie

ARG RUNTIME_DEPS
RUN apt-get update && apt-get install -y ${RUNTIME_DEPS} && apt-get clean

# the runtime of the sanitizers, loaded with LD_PRELOAD by run.sh asan
COPY --from=builder /usr/local/lib64 /opt/gcc/lib64

COPY --from=builder /usr/local/lib/libcerver.so /usr/local/lib/
COPY --from=builder /usr/local/include/cerver /usr/local/include/cerver
COPY --from=builder /usr/local/lib/libauth.so /usr/local/lib/
COPY --from=builder /usr/local/include/auth /usr/local/include/auth
COPY --from=builder /opt/probe/probe /opt/percepthor/probe

RUN echo "/opt/gcc/lib64" > /etc/ld.so.conf.d/gcc.conf && ldconfig

ARG PYMONGO_VERSION
ARG PYMONGOOSE_VERSION
RUN pip install --no-cache-dir pymongo==${PYMONGO_VERSION} pymongoose==${PYMONGOOSE_VERSION}

WORKDIR /home/pypercepthor

# the dependencies of auth-service, that the e2e tier runs (--build-context authservice=<path>)
COPY --from=authservice requirements.txt /opt/auth-service/requirements.txt
RUN pip install --no-cache-dir -r /opt/auth-service/requirements.txt

COPY tests/requirements.txt tests/requirements.txt
RUN pip install --no-cache-dir -r tests/requirements.txt

ENV PYTHONPATH=/home/pypercepthor:/home/pycerver
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /home/pypercepthor/tests

CMD ["pytest"]
