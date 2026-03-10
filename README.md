
## Structure
- `data_quality_ci.yml` — CI pipeline for running tests on PR
- `JiraBugReport.md` — Bug report for the date-shift issue
- `MonitoringStrategyBonus.md` — Monitoring & CI/CD strategy
- `RCAInvestigation.md` — Root cause analysis
- `test_data_quality.py` — Pytest suite for automated data quality checks
- `sql_queries.sql` — SQL validation tests

## Running the tests
```bash
pip install pytest pandas
pytest tests/test_data_quality.py -v
```

## Notes
- Python tests use Pandas mocks. In production, we'll swap fixtures with Snowflake connection.
- The test plan spreadsheet should be maintained separately in Qase.
