#!/bin/sh
ip=0.0.0.0
port=42069
gunicorn -w 4 -b $ip:$port main:public