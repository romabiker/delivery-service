#! /usr/bin/env bash

set -e
set -x

taskiq worker app.tkq:broker
