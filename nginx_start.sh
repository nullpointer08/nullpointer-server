#!/bin/sh
uwsgi --socket /tmp/hisra_server.sock --module hisra_server.wsgi --chmod-socket=664
