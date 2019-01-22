#!/bin/bash

nohup gunicorn -b 0.0.0.0:18080 rhino.wsgi >> /var/log/rhino/rhino.log 2>&1 &