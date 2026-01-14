FROM python:3.13-alpine AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# do not add dev dependencies here  
RUN apk update && apk upgrade && \
    apk add --no-cache \
        ca-certificates \
        nodejs \
        npm

COPY requirements.txt .

RUN uv pip install --system --upgrade pip && uv pip install --system -r requirements.txt

COPY . .


FROM base AS build

CMD ["tail", "-f", "/dev/null"]


FROM base AS dev

RUN apk update && apk add --no-cache \
        curl \
        openssh-client \
        git \
        bash \
        lsof \
        make \
        jq

CMD ["tail", "-f", "/dev/null"]