#!/bin/bash

# Activate your virtual environment
source ./venv/bin/activate


./venv/bin/gunicorn main:app --bind 0.0.0.0:8000