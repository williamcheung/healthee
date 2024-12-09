# Health Equity Explorer

Explore health equity by state, race, gender, and age. Based on the dataset `Lokahi_Innovation_in_Healthcare_Hackathon.zip`.

## Approach

The dataset consists of 907,464 members (not 450,000) and their associated enrollment and services data. Processing the entire dataset using Pandas and Dask on my hardware, a Dell Inspiron laptop with 16 GB RAM and 4 cores, was not possible, causing memory allocation and out of disk space errors after minutes of processing.

As a result, I decided to split the member dataset into groups of 100,000, in order of parquet file name in the original dataset. I called each group a "cohort". This resulted in 10 cohorts, the first 9 having 100,000 rows, and the 10th having the remaining 7,464 rows.

I then analyzed each cohort separately and generated separate HTML reports for state (x1), race (x2), gender (x1), and age (x1) comparisons, for a total of 5 reports per cohort. The analysis for each cohort takes several minutes but at least could run on my laptop to completion without crashing.

With all 10x5 = 50 reports generated from the analysis, I wrote a web UI to display the reports. The user can select a specific cohort by number (from 1 to 10) or can expand all 10 cohorts to see their corresponding reports.

## Splitter script - split_rows.py

The `split_rows.py` script is located in directory `dataset/Claims_Member`. To run it first follow the `README.txt` in each `dataset` folder, which tells you to put the contents of the corresponding folder from the provided dataset.

Then run `python split_rows.py`. It creates subfolders `split_Claims_Member_1` to `split_Claims_Member_10`. Each subfolder contains a parquet file and a CSV file. The CSV is for reference; the analysis only uses the parquet file. These generated files are included in this repo.

Note this script only needs the original dataset files for `Claims_Member`. However, you should also provide the other requested original dataset files because they are needed by the analysis script, described next.

## The .env file

A `.env_sample` file is provided in this repo. Copy it to a new `.env` file which you can edit as specified below.

## Analysis script - analyze.py

To run `analyze.py`, first edit the `.env` file and update `MEMBERS_PATH` to which cohort you want to analyze. For example for the 3rd cohort, use `split_Claims_Member_3`. Then run `python analyze.py` which will generate the 5 HTML reports for the cohort in project folder `html_files`. These generated files are included in this repo. Please be patient running this script. I ran it for all 10 cohorts by editing the `.env` file before each run.

## Web app - ui.py

The web app is a FastAPI app that lets you select a specific cohort to see the 5 HTML reports for it. There are 10 dropdowns for selecting cohorts to allow you to see the reports for all 10 cohorts on the same page if you wish. To make it convenient for you to see all reports for all cohorts, there is an `Expand all` button at the top you can click to expand all 10 cohorts at once. If you use this feature, please wait for all the reports to render, and note that the order of rendering is not necessarily from top to bottom or left to right.

The web app is launched using `uvicorn` in the code itself, so to start the app simply run `python ui.py`. The app will start on port 8000.

## Deployment

A Docker file is provided for deployment. I used it to build a Docker image which I successfully deployed to my cloud instance: https://health-equity-explorer.williamcheung.click
