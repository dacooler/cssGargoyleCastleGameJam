#!/usr/bin/env bash

cd "$(dirname "$0")"
cargo watch -C . -w . -i index.html -s ./make.py
