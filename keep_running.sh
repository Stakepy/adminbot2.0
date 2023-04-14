#!/bin/bash
until python main.py
do
   echo--- "Restarting"
   sleep 2
done
