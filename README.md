# python-test

Simple data pipeline example using pandas. This README explains requirements, installation, how to run the script, expected outputs, and key design decisions.

## Requirements
- Python 3.x
- pandas
- pyarrow or fastparquet (to write Parquet files)

## Installation (recommended: virtual environment)

Bash
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a minimal `requirements.txt`:
```bash
echo "pandas" > requirements.txt
echo "pyarrow" >> requirements.txt   # or fastparquet
```

## How to run

The script uses hardcoded paths in `main()` (see source). Ensure the three source files exist at those paths:

- crm_leads.csv
- web_activity.json
- transactions.txt

Run:
```bash
python data_pipeline.py
```

## Running tests / Debugging

Run pytest from the project root:
```bash
python -m pytest -v -s
```
- `-v` for verbose
- `-s` to show print() output

To debug a module or file in VS Code, use the Run and Debug configurations. Ensure `${workspaceFolder}` is on `PYTHONPATH` so package imports like `mypg.main` resolve.

## Output files

On success the pipeline writes:
- `customer_360.parquet` — Parquet file with merged transaction and web activity data
- `web_error_log.txt` — JSON web activity records where `user_uuid` is missing/null
- `transaction_error_log.txt` — Transaction records with negative amounts (includes transaction id)

## Key design decisions

1. Choice of libraries
   - Uses pandas for concise, efficient reading/writing and transformations.

2. Deduplication (CRM)
   - Deduplicate CRM leads by `email`. Keep the record with the latest `creation_date`:
     sort by `creation_date` descending, then `drop_duplicates(subset='email', keep='first')`.

3. Data integrity & error handling
   - Invalid records are separated and logged rather than raising exceptions:
     - Web activity with missing `user_uuid` → `web_error_log.txt`
     - Transactions with negative `amount` → `transaction_error_log.txt`
   - Use `pd.to_numeric(..., errors='coerce')` to avoid crashes on bad numeric data.

4. Merging & limitations
   - Transactions and web activity are merged on `user_uuid` (left join).
   - CRM leads are cleaned but not merged due to missing common key; consider fuzzy matching or ID mapping to integrate CRM.

## Deployment notes (AWS example)
- Store sources and outputs in S3.
- Use AWS Glue for ETL (recommended) or AWS Lambda for small jobs.
- Schedule via EventBridge or use Airflow for complex workflows.
- Send logs to CloudWatch.

## Contributing / Notes
- Put source files in the paths expected by `data_pipeline.py` or modify the script to accept configurable paths.
- Consider adding a `pyproject.toml` or `setup.cfg` if you want editable installs (`pip install -e .`) to help tests and imports resolve.