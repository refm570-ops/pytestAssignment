import pytest
import pandas as pd

@pytest.fixture
def raw_events():
    #simulate realistic raw events
    return pd.DataFrame({
        "event_id": [f"evt_{i}" for i in range(100)],
        "vessel_id": ["V-101"] * 40 + ["V-202"] * 35 + [None] * 3 + ["V-303"] * 22,
        "event_time": pd.date_range("2026-01-29", periods=100, freq="15min"),
        "event_type": ["collision_alert"] * 30 + ["speed_change"] * 70,
        "payload": ['{"risk": 0.8}'] * 100,
    })

@pytest.fixture
def collision_alerts():
    # mock data
    return pd.DataFrame({
        "vessel_id": ["V-101", "V-202", "V-303"],
        "alert_date": pd.to_datetime(["2026-01-29"] * 3).date,
        "alert_count": [15, 10, 5],
    })

@pytest.fixture
def previous_day_count():
    return 100

# Test 1: Row count anomaly detection (>20% drop)
def test_row_count_anomaly(raw_events, previous_day_count):
    """
    If today's row count drops by more than 20% compared to
    the previous day, it indicates a pipeline failure.
    """
    current_count = len(raw_events)
    drop_pct = (previous_day_count - current_count) / previous_day_count * 100

    # We expect the drop to be less than or equal to 20%
    assert drop_pct <= 20, (
        f"Anomaly detected: Row count dropped by {drop_pct:.1f}% "
        f"(from {previous_day_count} to {current_count} rows)"
    )

# Test 2: Schema matches expected columns
def test_raw_events_schema(raw_events):
    #verify expected columns
    expected_columns = {"event_id", "vessel_id", "event_time", "event_type", "payload"}
    actual_columns = set(raw_events.columns)

    missing = expected_columns - actual_columns
    assert not missing, f"Schema mismatch! Missing expected columns: {missing}"

# Test 3: Null rate on vessel_id < 5%
def test_vessel_id_null_rate(raw_events):
   #vessel_id is essential for aggregation
    total = len(raw_events)
    null_count = raw_events["vessel_id"].isnull().sum()
    null_pct = (null_count / total) * 100

    assert null_pct < 5.0, (
        f"vessel_id null rate is too high: {null_pct:.2f}% "
        f"({null_count}/{total} rows are null)"
    )

# Test 4: alert_count is non-negative
def test_no_negative_alerts(collision_alerts):
    #alert_count cant be negative
    negatives = collision_alerts[collision_alerts["alert_count"] < 0]

    assert len(negatives) == 0, (
        f"Found {len(negatives)} rows with negative alert_count: "
        f"{negatives.to_dict(orient='records')}"
    )