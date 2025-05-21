# Using 3.12 because it's the latest version supported by Onionshare (python = ">=3.10,<3.13")
ARG PYTHON_VERSION=3.12
# Using slim to simplify install of tor (Debian)
ARG BASE_IMAGE=docker.io/library/python:${PYTHON_VERSION}-slim

FROM ${BASE_IMAGE}

ARG ONIONSHARE_VERSION=2.6.3

# Installing tor (system dependency for onionshare)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends tor

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
#ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser

# Using venvs to make the container independent of runtime user
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install onionshare-cli==$ONIONSHARE_VERSION

# Switch to the non-privileged user to run the application.
#USER appuser

# XDG_CONFIG_HOME needs to be set if the user doesn't have a homedir
# in the docker image (onionshare/onionshare#943)
ENV XDG_CONFIG_HOME="/tmp"

ENTRYPOINT ["onionshare-cli"]
CMD ["-v", "--persistent", "/etc/onionshare/onionshare.json"]
