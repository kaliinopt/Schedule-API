from app.core.utils import check_time_overlap, calculate_recurring_dates
from datetime import date


def test_check_time_overlap():
    assert check_time_overlap("12:00", "14:00", "15:00", "16:00") is False


def test_check_time_overlap_incorrect():
    assert check_time_overlap("12:00", "16:00", "15:00", "16:00") is True


def test_calculate_recurring_dates():
    start_date = date.fromisoformat("2025-04-01")
    repeat_until = date.fromisoformat("2026-04-01")
    check_from = date.fromisoformat("2025-04-01")
    check_to = date.fromisoformat("2026-04-01")

    result = calculate_recurring_dates(
        start_date, "daily", repeat_until, check_from, check_to
    )
    print(result)
    assert isinstance(result, list)
    assert date(2026, 4, 1) in result


def test_calculate_recurring_dates_incorrect():
    start_date = date.fromisoformat("2027-04-01")
    repeat_until = date.fromisoformat("2026-04-01")
    check_from = date.fromisoformat("2021-04-01")
    check_to = date.fromisoformat("2020-04-01")

    result = calculate_recurring_dates(
        start_date, "daily", repeat_until, check_from, check_to
    )
    print(result)
    assert result == []
