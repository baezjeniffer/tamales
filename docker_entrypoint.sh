#!/bin/bash

echo "Entrando al entrypoint sh"
echo $@
cron 
exec python "$@"