#!/bin/sh -e
set -x
ruff check app scripts --select I --fix
ruff format app scripts
