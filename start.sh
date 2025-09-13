#!/bin/bash

# Activate your virtual environment
source ./myenv/bin/activate


./myenv/bin/gunicorn main:app --bind 0.0.0.0:8000