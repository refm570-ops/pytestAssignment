**1. Automated Monitoring**

Daily checks that run after each pipeline completion - row count anomalies (>20% drop), null rate thresholds, negative values,comparing counts between raw and analytics to make sure nothing got lost. Failures alert to Slack with the query results attached. I would also add a freshness check - if collision_alerts hasn't been updated in N hours, that's an alert on its own.

The pytest tests from Part 3 can report results directly to Qase using the qase-pytest reporter, so every pipeline run automatically shows up as a test run in Qase with pass/fail status - no need to track results separately.

**2. Preventing Silent Failures**

Data gets written to a staging table first, where the quality tests run. If anything fails - row drop, null spike, or schema change - the pipeline stops and the bad data doesn't reach the final collision_alerts table. This way Operations never sees broken numbers.

**3. CI/CD Integration**

Any PR that changes pipeline logic or SQL triggers the test suite against a test environment with sample data. If any check fails, the merge is blocked. Since the team uses Qase with Jira integration, a failed test run can automatically open a linked Jira bug - so issues like the date-shift from Part 4 get tracked without someone needing to create the ticket manually.
