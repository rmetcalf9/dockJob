#!/bin/bash

# sudo -H pip install nose-timer 
#https://github.com/mahmoudimus/nose-timer

nosetests --rednose --timer-top-n 10 ./test
