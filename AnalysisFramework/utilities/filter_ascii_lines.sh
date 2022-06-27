#!/bin/bash

head -n "$2" "$1" | perl -nle 'print if m{^[[:ascii:]]+$}'