# Pool Cleaning Operations Report

A small Python program for a fictional pool cleaning company with four service branches. It reads job records from a CSV file, checks the data, and prints out a report showing sales, estimated profit, customer plans, and which branch had the highest sales.

## What you need

- Python 3.10 or later
- A terminal (VS Code works)
- No extra Python packages

## How to run it

1. Download this project and open the `pool_cleaning_pipeline` folder in VS Code.
2. Open **Terminal > New Terminal**.
3. Optional: make a virtual environment with `py -m venv .venv` on Windows.
4. Run the main program:

   ```powershell
   py main.py
   ```

5. Run the unit tests:

   ```powershell
   py -m unittest discover -s tests -v
   ```

On macOS/Linux, replace `py` with `python3`. If you created a virtual environment, you can also run `.venv\Scripts\python.exe main.py` on Windows.

## Where the data goes

The fictional starting records are in `data/service_visits.csv`. Each row includes:

- Branch ID and service date
- Customer plan (`Basic`, `Plus`, or `Commercial`)
- Number of services
- Revenue and estimated cost before tax
- Province and status (`completed` or `cancelled`)

You can edit this CSV to add jobs. Keep the column headings unchanged. The program lists rows with problems instead of including them in its sales totals. Cancelled but otherwise valid jobs are included in the clean-record count, not completed sales.

## Files in the project

| File | What it does |
| --- | --- |
| `main.py` | Opens the CSV and runs the program |
| `pipeline/schema.py` | Defines the `TransactionRecord` class |
| `pipeline/validator.py` | Converts text, checks dates, and rejects bad rows |
| `pipeline/transformer.py` | Filters completed work and calculates tax and profit |
| `pipeline/reporter.py` | Uses the `BranchLedger` class and prints a report |
| `tests/test_pipeline.py` | Contains ten unit tests |
| `PROJECT_OVERVIEW.md` | Explains the idea and responsibilities |
| `Executive_Summary_Report.pdf` | One-page executive report |

## Notes

The company, transactions, estimated costs, and tax values are examples made for this assignment. It is not connected to a real pool business. The program uses ordinary Python classes, functions, loops, list comprehension, `map()`, `filter()`, and error handling.
