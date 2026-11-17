#!/bin/sh
set -eu

: "${API_TOKEN:?Set the API_TOKEN secret on the staging environment}"
: "${GITHUB_REPOSITORY_ID:?Missing stable repository ID}"
: "${GITHUB_SHA:?Missing commit SHA}"
: "${STAGING_PORT:?Missing local staging port}"
: "${STAGING_URL:?Missing staging URL}"

container="seminar-shop-${GITHUB_REPOSITORY_ID}"
backup="${container}-previous"
image="${container}:${GITHUB_SHA}"

docker build --tag "$image" .
if docker container inspect "$backup" >/dev/null 2>&1; then
    printf 'Previous deployment needs attention: %s\n' "$backup" >&2
    exit 1
fi
if docker container inspect "$container" >/dev/null 2>&1; then
    docker rename "$container" "$backup"
    docker stop "$backup" >/dev/null
fi

if docker run --detach --restart unless-stopped --name "$container" \
    --publish "127.0.0.1:${STAGING_PORT}:8080" "$image" >/dev/null &&
    curl --fail --silent --show-error --max-time 5 --retry 8 --retry-all-errors \
        --retry-delay 1 "${STAGING_URL%/}/health"; then
    if docker container inspect "$backup" >/dev/null 2>&1; then
        docker rm "$backup" >/dev/null
    fi
else
    if docker container inspect "$container" >/dev/null 2>&1; then
        docker rm --force "$container" >/dev/null
    fi
    if docker container inspect "$backup" >/dev/null 2>&1; then
        docker rename "$backup" "$container"
        docker start "$container" >/dev/null
    fi
    exit 1
fi
