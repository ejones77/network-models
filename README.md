# network-models
Submitted Assignment for Northwestern MSDS-460

## Overview 

This project optimizes the project completion time for a software development plan to implenent a data pipeline and front-end product for ingesting Yelp reviews and making sense of them. 

Each task and the roles needed for the job are pre-defined in `project-plan-v003.xlsx` 
    - Estimated hours to complete each task and the roles needed for each task were inputted to update the spreadsheet.

PuLP is used to optimize project completion time under the expected, best, and worst case scenarios. 


## Setup
- python version -- 3.11.9
- in the respository directory, create and activate a virtual environment (assuming powershell)
    - ` py -m venv .venv`
    - `./.venv/scripts/activate`
- install dependencies with
    - `py -m pip install --upgrade pip`
    - `pip install pulp`

- execute the main program
    - `py software_plan.py`