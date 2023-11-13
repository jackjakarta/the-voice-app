#!/bin/bash

echo ""
echo "Hello, $(whoami)! App is starting..."

. env/bin/activate

sleep 1

python3 main.py
