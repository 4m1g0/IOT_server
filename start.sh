#!/bin/bash

python3 IOTServer/Main.py 8080 8081 &
python3 pricingServer/main.py &
python3 APIServer/main.py &

sleep 10s
/bin/bash

