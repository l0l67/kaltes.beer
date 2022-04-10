#!/bin/sh
port=42069
gunicorn -w 4 -b 0.0.0.0:$port main:public