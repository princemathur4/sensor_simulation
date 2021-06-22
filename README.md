# Sensor simulation

## Setup
- Clone the repository using: `git clone https://github.com/princemathur4/sensor_simulation`
- cd into the project root folder
- Create a Python3.7 virtual env using: `python3.7 -m venv ./virtualenv`
- install packages using requirement.txt file `./virtualenv/bin/pip install -r requirements.txt`
 
## Run
- cd into the project root folder
- Run using command: `./virtualenv/bin/python simulate.py`

## Description
After running the code the input and output will be dumped in the project directory. A sample of which is already provided in the project. The files will be as follows:

- input.json: This file would contain second-wise data for simulated sensor.
- output.csv: This file would contain stats for every 15-min derived from the input data
- hourly_stats.csv: This file would contain stats for every hour derived from the output.csv i.e. 15-min stats data
