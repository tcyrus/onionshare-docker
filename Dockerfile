# Using 3.12 because it's the latest version supported by Onionshare (python = ">=3.10,<3.13")
# Using slim to simplify install of tor (Debian)
ARG BASE_IMAGE=docker.io/library/python:3.12-slim

FROM ${BASE_IMAGE}

ARG ONIONSHARE_VERSION=2.6.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    tor

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Using venvs to make the container independent of runtime user
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install onionshare-cli==$ONIONSHARE_VERSION

# See onionshare/onionshare#943
ENV XDG_CONFIG_HOME="/tmp"

ENTRYPOINT ["onionshare-cli"]
CMD ["-v", "--persistent", "/etc/onionshare/onionshare.json"]
