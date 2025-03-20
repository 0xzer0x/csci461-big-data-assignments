#!/usr/bin/env bash
set -euo pipefail

__SCRIPT_DIR="$(cd "$(dirname "$(realpath "${0}")")" && pwd)"
_TARGETDIR="${__SCRIPT_DIR}/bd-a1/service-result"
_CONTAINER_NAME="bd-a1"
_CONTAINER_ID="$(docker container ls -qf name="${_CONTAINER_NAME}" | head -n 1)"

_prepare-directory() {
  echo "-- creating directory ${_TARGETDIR}"
  mkdir -p "${_TARGETDIR}"
}

_copy-files() {
  if [ -z "${_CONTAINER_ID}" ]; then
    echo "-- no container with name ${_CONTAINER_NAME} found!"
    exit 1
  fi

  echo "-- copying script results from container"
  for resfile in loaded_data.csv res_dpre.csv eda-in-1.txt eda-in-2.txt eda-in-3.txt vis.png k.txt; do
    docker container cp "${_CONTAINER_ID}:/home/doc-bd-a1/${resfile}" "${_TARGETDIR}"
  done
}

_stop-container() {
  if [ -z "${_CONTAINER_ID}" ]; then
    echo "-- no container with name ${_CONTAINER_NAME} found!"
    exit 1
  fi

  docker container stop "${_CONTAINER_ID}"
}

_main() {
  _prepare-directory
  _copy-files
  _stop-container
}

_main
