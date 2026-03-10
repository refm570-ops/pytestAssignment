**1. What seems wrong in the pipeline?**

The events in raw_events happened on 2026-01-30 (10:00, 12:15, 17:42), but collision_alerts shows them under 2026-01-29. So the count is right (3), but assigned to the wrong day. The dashboard then queries for Jan 29 and shows 0 - because it's either reading stale data or the "real" Jan 29 was overwritten by Jan 30 events.

**2. Where would you investigate first?**

I will check the airflow variables to see which date parameter was passed, could be a quick find.

If not, I will check the aggregation step that populates collision_alerts - specifically how event_time gets converted to alert_date. First thing I will check is the Snowflake session timezone. If it's not UTC, DATE(event_time) will interpret timestamps wrong and shift the date back. Quick way to confirm:

SELECT event_time, DATE(event_time) AS extracted_date
FROM raw_events
WHERE vessel_id = 'V-101' AND DATE(event_time) = '2026-01-30'
LIMIT 5;

If extracted_date shows Jan 29 for events clearly on Jan 30 - that's the issue.

**3. What kind of bug could cause a date shift?**

Most likely a timezone mismatch - if the Snowflake session runs in a timezone behind UTC, a timestamp like 2026-01-30 10:00 UTC gets cast to a local date that's still Jan 29. Another option: a wrong date offset in the batch window - something like CURRENT_DATE - 1 that pulls the wrong day's events.
