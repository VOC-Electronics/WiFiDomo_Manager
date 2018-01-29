#!/usr/bin/env bash

LOGGER=$(which logger)

if [ -z "$1" ] ; then
 echo "Please parse data to log"
 exit 0
else
  DATA="$1"
  $LOGGER -p local0.notice ${DATA}
fi
