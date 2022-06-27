#!/bin/bash

. "${0%/*}/env_functions"

sort "$1" --random-source=<(get_fixed_random 42) -R | head -"$2"
