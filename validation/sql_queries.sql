

//*Test 1: Duplicate event check *//
/*
Goal: Ensure ingestion isn't creating duplicate events, which inflates downstream counts.
Expected outcome: 0 rows returned.
*/
SELECT 
    event_id, 
    COUNT(*) AS occurrence_count
FROM raw_events
WHERE CAST(event_time AS DATE) = CURRENT_DATE - 1
GROUP BY event_id
HAVING COUNT(*) > 1;

//*Test 2: Null Check for Vessel ID *//
/*
Goal: Ensure critical identifiers aren't missing before we aggregate.
Expected outcome: 0 rows returned (or below acceptable threshold).
*/
SELECT 
    event_id,
    event_time
FROM raw_events 
WHERE vessel_id IS NULL 
  AND CAST(event_time AS DATE) = CURRENT_DATE - 1;

//* Test 3: KPI logic boundaries*//
/*
Goal: Validate that the alert_count metric contains only logical values.
Expected outcome: 0 rows returned.
*/
SELECT 
    vessel_id, 
    alert_date, 
    alert_count
FROM collision_alerts 
WHERE alert_count < 0;

//*Test 4: Data accuracy *//
/*
Goal: Verify the aggregated count in the analytics table perfectly matches the raw events count.
Expected outcome: 0 rows returned (meaning no mismatches found).
*/
WITH raw_counts AS (
    SELECT 
        vessel_id, 
        CAST(event_time AS DATE) AS event_date, 
        COUNT(*) AS raw_alert_count
    FROM raw_events
    WHERE event_type = 'collision_alert'
    GROUP BY vessel_id, CAST(event_time AS DATE)
)
SELECT 
    r.vessel_id,
    r.event_date,
    r.raw_alert_count,
    a.alert_count
FROM raw_counts r
JOIN collision_alerts a 
  ON r.vessel_id = a.vessel_id AND r.event_date = a.alert_date
WHERE r.raw_alert_count != a.alert_count;

//*Test 5: Invalid Data in raw events *//

/*
Goal: Detect records in the analytics table that do not have corresponding raw telemetry events for that day.
Expected outcome: 0 rows returned.
*/
SELECT 
    a.vessel_id, 
    a.alert_date,
    a.alert_count
FROM collision_alerts a
LEFT JOIN raw_events r 
  ON a.vessel_id = r.vessel_id 
  AND a.alert_date = CAST(r.event_time AS DATE)
  AND r.event_type = 'collision_alert'
WHERE r.event_id IS NULL;