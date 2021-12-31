#!/bin/bash
(trap 'kill 0' SIGINT; python3 `pwd`/$1 & python3 `dirname $0`/server.py)