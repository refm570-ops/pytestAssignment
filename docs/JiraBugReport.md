## Title
[BUG] Collision alerts shifted by -1 day - dashboard shows wrong date

## Environment
* **Data Warehouse:** Snowflake <env name>
* **BI Tool:** Operations Dashboard <link to dashboard>

## Steps to Reproduce
1. Query `raw_events` for vessel `V-101` - find 3 collision_alert events on `2026-01-30` (10:00, 12:15, 17:42)
2. Query `collision_alerts` for the same vessel - the 3 alerts are recorded under `2026-01-29` instead of `2026-01-30`
3. Open Operations Dashboard → filter V-101 , Jan 29 shows 0, Jan 30 shows nothing

## Expected Result vs Actual Result
**Expected Result:** Events from Jan 30 should appear under alert_date = 2026-01-30 in collision_alerts, and the dashboard should show 3 alerts for V-101 on that date.

**Actual Result:** The 3 events are bucketed under 2026-01-29 instead. Dashboard shows 0 for Jan 29 and nothing for Jan 30 - both dates are wrong.

## Priority
depends on environment - Critical if its in production(assuming that if operations use this dashboard, its in production), otherwise would be less.

## Evidence
1. SQL output comparing raw_events dates vs collision_alerts dates (queries above)
2. Dashboard screenshot showing 0 for V-101 on Jan 29
3. Pipeline job logs from the aggregation run on 2026-01-30
