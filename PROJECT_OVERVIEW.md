# Project Overview: Pool Cleaning Operations Report

## Purpose

This project looks at service jobs from a fictional company that cleans swimming pools. The company has branches in London, Barrie, Kelowna, and Red Deer. It is meant to help a manager quickly see how the branches are doing.

## Problem

A business can have messy service records, like missing branch names, invalid dates, and incorrect prices. Those mistakes can affect sales reports. The program checks each row first and only uses valid, completed jobs for sales calculations.

## Data

The program starts with a CSV file of fictional pool cleaning appointments. The data includes branch IDs, dates, customer plans, how many services were sold, revenue, costs, province, and job status. Some entries intentionally contain mistakes so the program can show how errors are handled.

## How it works

1. `main.py` loads the CSV into a list of dictionaries.
2. `validator.py` checks each dictionary and makes a `TransactionRecord` object for valid rows.
3. `transformer.py` uses `filter()` and `map()` to produce new data for completed work. The original data stays unchanged.
4. `reporter.py` uses a second class called `BranchLedger` to calculate branch totals, then prints a summary.
5. The tests check important parts of the program automatically.

## Why it is useful

The final report shows gross sales, estimated profit, tax totals, record retention, top-performing branch, and customer plan breakdowns. This helps someone notice data quality problems and compare service locations.

## How someone can build and run it

This project uses standard Python and a CSV file, so no outside packages are required. Instructions are in `README.md`. The files are separated so each part of the program has its own job.

## Who completed which parts

Complete this section with the **actual contributions** of each person before submitting. Include any AI assistance according to the course rules.

- Student(s) and their contributions: **[Fill in]**
- AI assistance, if used: **[Fill in accurately]**

## Limits

This is a demonstration with fictional data. Service costs are estimates, and the tax rates are simplified sample settings, not a tool for actual tax reporting. A future version could use actual business exports and show monthly trends.
