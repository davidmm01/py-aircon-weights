# py-aircon-weights

## Set up

It is recommended you create a virtual environment to run the program.  

`python3 -m venv venv`

`. ./venv/bin/activate`

`pip3 install -rrequirements.txt`

## Run The Program

TODO!

## Run The Tests

Given you have set up your enviornment, simply run:

`pytest --isort --flake8`

## Updating Requirements

This project makes use of pip-tools' `pip-compile` for managing its requirements.  
To update the project requirements, make your changes in requirements.in, then run:

`pip-compile`

Now install the requirements in the usual way:

`pip3 install -rrequirements.txt`
