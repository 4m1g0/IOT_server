#!/bin/bash

python3 Main.py 8080 8081 &
python3 pricingServer/main.py &

sleep 10s
/bin/bash

