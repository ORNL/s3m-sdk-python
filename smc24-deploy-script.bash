#!/bin/bash

# Show OLCF_API_TOKEN
clear
echo "Verifying OLCF API token has been set @ `date`"
env | fgrep OLCF_API_TOKEN
echo
sleep 3

# Show demo help
cmd="python3 smc24-streaming-demo.py --help"
echo "Running: $cmd"
$cmd
sleep 27

# List available services
clear; date
cmd="python3 smc24-streaming-demo.py --avail"
echo "Running: $cmd"
$cmd
sleep 15

# Show deployed RabbitMQ services
clear; date
cmd="python3 smc24-streaming-demo.py rabbitmq"
echo "Running: $cmd"
$cmd
sleep 3

# Show deployed Redis services
echo
cmd="python3 smc24-streaming-demo.py redis"
echo "Running: $cmd"
$cmd
sleep 3

# Deployed new RabbitMQ service
clear; date
cmd="python3 smc24-streaming-demo.py --deploy rabbitmq smc24-rabbit"
echo "Running: $cmd"
$cmd
while true; do
    sleep 5
    echo "Checking for healthy cluster @ `date`"
    output=$(python3 smc24-streaming-demo.py rabbitmq)
    echo $output | fgrep 'healthy'
    [ $? -eq 0 ] && break
done
echo

# Get cluster info
clear; date
cmd="python3 smc24-streaming-demo.py --info rabbitmq smc24-rabbit"
echo "Running: $cmd"
$cmd