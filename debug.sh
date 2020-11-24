#!/usr/bin/env bash

# shellcheck disable=SC1091

[[ -d "venv" ]] || python3.8 -m venv ./venv
source venv/bin/activate
pip install -U -r requirements.txt
cp example.env .env
#python3 -m hades
gunicorn hades:app -b 0.0.0.0:5500
