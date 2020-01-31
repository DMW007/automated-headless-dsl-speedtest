#!/bin/bash
if [ -z ${INTERVAL_MIN+x} ]; then
    echo "Required env variable INTERVAL_MIN is not set, exiting!"
    exit
fi

echo "Start cron with interval = ${INTERVAL_MIN} min"
while true
do
  python3 speedtest.py
  sleep ${INTERVAL_MIN}m
done