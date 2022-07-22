#!/bin/bash
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

IMAGE_TAG="tournament-scraper:latest"
SRC_PATH=/workdir

MOUNT_PATHS=(
-v "$APP_DIR:$SRC_PATH"
-v ~/.ssh:/root/.ssh
-v ~/.gitconfig:/root/.gitconfig
)

touch .env

set -x
# shellcheck disable=SC2068
docker run --env-file .env -ti --rm ${MOUNT_PATHS[@]} --workdir "$SRC_PATH" "$IMAGE_TAG" bash