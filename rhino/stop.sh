#!/bin/bash

ps -ef | grep gunicorn | grep rhino | awk '{print $ 2}' | xargs kill