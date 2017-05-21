#!/bin/bash
cd /var/tmp/open-pager-url/
export FLASK_APP=index.py
flask run --host=0.0.0.0 --port=5001
