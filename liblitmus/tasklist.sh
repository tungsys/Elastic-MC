#!/bin/sh

# Task release list.
./rtspin -w 10 100 100 40 &
./rtspin -w 10 100 100 40 &
./rtspin -w 10 100 100 40 &
./rtspin -w 10 100 100 40 &
./rtspin -w 10 100 100 40 &
./rtspin -w 10 100 100 40 &
sleep 15
echo "Releasing tasks.."
./release_ts
wait
