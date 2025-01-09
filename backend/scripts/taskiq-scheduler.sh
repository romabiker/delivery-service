#! /usr/bin/env bash

set -e
set -x

taskiq scheduler app.tkq:scheduler app.tasks.delivery
