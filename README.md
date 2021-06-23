# Sensor simulation

## Setup
- Install python3 if not installed already
- Clone the repository using: `git clone https://github.com/princemathur4/sensor_simulation`
- cd into the project root folder
- Create a Python3 virtual env using: `python3 -m venv ./virtualenv`
- Activate the virtual env for your command line,

For Windows:
`.\virtualenv\Scripts\activate`

For Linux:
`source ./virtualenv/bin/activate`
- install packages using requirement.txt file `pip install -r requirements.txt`
 
## Run
- cd into the project root folder
- Activate virtual env like mentioned above
- Run using command: `python simulate.py`

## Description
After running the code the input and output will be dumped in the project directory. A sample of which is already provided in the project. The files will be as follows:

- input.json: This file would contain second-wise data for simulated sensor.
- output.csv: This file would contain stats for every 15-min derived from the input data
- hourly_stats.csv: This file would contain stats for every hour derived from the output.csv i.e. 15-min stats data
