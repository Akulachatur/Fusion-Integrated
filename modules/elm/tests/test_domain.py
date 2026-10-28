from datetime import date
from modules.elm.domain.counting import calculate_leave_days, is_weekend, is_holiday
from modules.elm.domain.state_machine import LeaveStatus, get_valid_transitions


def test_is_weekend():
    saturday = date(2023, 10, 14)
    sunday = date(2023, 10, 15)
    monday = date(2023, 10, 16)
    assert is_weekend(saturday) is True
    assert is_weekend(sunday) is True
    assert is_weekend(monday) is False


def test_is_holiday():
    republic_day = date(2023, 1, 26)
    regular_day = date(2023, 1, 27)
    assert is_holiday(republic_day) is True
    assert is_holiday(regular_day) is False


def test_cl_half_day_counting():
    # Half day CL is 0.5 days
    days = calculate_leave_days("2023-10-17", "2023-10-17", "CL", is_half_day=True)
    assert days == 0.5


def test_el_continuous_counting_includes_weekends():
    # Friday 2023-10-13 to Monday 2023-10-16 is 4 days total including Sat + Sun
    days = calculate_leave_days("2023-10-13", "2023-10-16", "EL")
    assert days == 4.0


def test_cl_excludes_weekends():
    # Friday 2023-10-13 to Monday 2023-10-16 (excluding Sat, Sun, and 2023-10-16 holiday)
    days = calculate_leave_days("2023-10-13", "2023-10-16", "CL")
    assert days == 1.0


def test_state_machine_unit_head_approval():
    unit_head_perms = {"leave_management.unit_head.review"}
    transitions = get_valid_transitions(LeaveStatus.AWAITING_UNIT_HEAD, unit_head_perms)
    to_statuses = [t.to_status for t in transitions]
    assert LeaveStatus.APPROVED in to_statuses
    assert LeaveStatus.REJECTED in to_statuses

