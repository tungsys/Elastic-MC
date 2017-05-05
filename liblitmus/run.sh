#!/bin/bash
sudo ./setsched EDFVD
sudo ./rtspin -Z 2 -w 10 20 17 15 20 20 10 &
sudo ./rtspin -w 5 50 50 10 &

