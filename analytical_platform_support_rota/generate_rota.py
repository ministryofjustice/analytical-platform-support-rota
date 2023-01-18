# Standard library
import json
import random
from datetime import timedelta
from math import ceil

# Third-party
from google_calendar_api import (
    create_service,
    delete_calendar_event,
    get_list_events_response,
    write_calendar_event,
)
from settings import date_range, google_calendar_api, support_team
from utils import (
    generate_report,
    get_workday_dates,
    repeat_and_shuffle_without_consecutive_elements,
    string_to_datetime,
)


def generate_lead_list(group: list[str], n_cycles: int) -> list:
    """A helper function that repeats the list, group, for n_cycles and shuffles each
    repitition.
    """
    random.shuffle(group)
    repeat_and_shuffle = []

    for _ in range(n_cycles):
        random.shuffle(group)
        repeat_and_shuffle.extend(group)

    return repeat_and_shuffle


def generate_assist_list(group_a: list[str], group_b: list[str], n_cycles: int) -> list:
    """A helper function that takes group_a and repeats it the number of times required
    such that it's length is at least as long as the length of group_b * n_cycles. Each
    repitition is shuffled whilst ensuring no two consequtive elements are the same.
    Finally the repeated and shuffled group_a list is sliced to the exact length of
    group_b * n_cycles.
    """
    group_a_length = len(group_a)
    group_b_length = len(group_b)

    if group_a_length == group_b_length:
        return repeat_and_shuffle_without_consecutive_elements(group_a, n_cycles)

    else:
        return repeat_and_shuffle_without_consecutive_elements(
            group_a, ceil((group_b_length * n_cycles) / group_a_length)
        )[: group_b_length * n_cycles]


def generate_support_pairs(
    group_1: list[str], group_2: list[str], n_cycles: int
) -> list[tuple]:
    """Generates a list of 2-tuples containing a leading and assisting pair to work
    support.
    """
    group_1_lead = generate_lead_list(group_1, n_cycles)
    group_2_assist = generate_assist_list(group_2, group_1, n_cycles)

    group_2_lead = generate_lead_list(group_2, n_cycles)
    group_1_assist = generate_assist_list(group_1, group_2, n_cycles)

    support_pairs = []
    group_1_lead_index = 0
    group_2_lead_index = 0

    for i in range(n_cycles):
        for j in range(len(group_1)):
            support_pairs.append(
                (group_1_lead[group_1_lead_index], group_2_assist[group_1_lead_index])
            )
            group_1_lead_index += 1

        for k in range(len(group_2)):
            support_pairs.append(
                (group_2_lead[group_2_lead_index], group_1_assist[group_2_lead_index])
            )
            group_2_lead_index += 1

    return support_pairs


def main():
    if support_team["start_cycle_with"] not in ["list_1", "list_2"]:
        raise ValueError(
            f"{support_team['start_cycle_with']} is an invalid group name."
        )

    service = create_service(
        google_calendar_api["client_secret_file"],
        google_calendar_api["api_name"],
        google_calendar_api["api_version"],
        google_calendar_api["scopes"],
    )
    calendar_id = google_calendar_api["calendar_ids"][google_calendar_api["calendar"]]

    list_1 = support_team["list_1"]
    list_2 = support_team["list_2"]

    start_date = string_to_datetime(date_range["start_date"])
    n_cycles = date_range["n_cycles"]
    n_days = n_cycles * (len(list_1) + len(list_2))
    workday_dates = get_workday_dates(start_date, n_days)

    if support_team["start_cycle_with"] == "list_1":
        support_pairs = generate_support_pairs(
            group_1=list_1, group_2=list_2, n_cycles=n_cycles
        )
    else:
        support_pairs = generate_support_pairs(
            group_1=list_2, group_2=list_1, n_cycles=n_cycles
        )

    print(f"Deleting all calendar events from {date_range['start_date']} onwards...")
    page_token = None
    while True:
        response = get_list_events_response(
            service, calendar_id, page_token, date_range["start_date"]
        )
        events = response.get("items", [])

        for event in events:
            delete_calendar_event(service, calendar_id, event["id"])
        page_token = response.get("nextPageToken", None)

        if not page_token:
            break

    lead_workdays = []
    assist_workdays = []
    event_body = {}
    print("Writing rota to calendar...")
    for i in range(n_days):
        event_body["summary"] = (
            f"{support_pairs[i][0]} is on support today with {support_pairs[i][1]} "
            "assisting"
        )
        event_body["start"] = {"date": str(workday_dates[i])}
        event_body["end"] = {"date": str(workday_dates[i] + timedelta(1))}

        write_calendar_event(service, calendar_id, event_body)

        lead_workdays.append((support_pairs[i][0], workday_dates[i].weekday()))
        assist_workdays.append((support_pairs[i][1], workday_dates[i].weekday()))

    days_worked_report, config_report = generate_report(
        list_1,
        list_2,
        lead_workdays,
        assist_workdays,
        workday_dates,
        n_cycles,
        n_days,
        google_calendar_api["calendar"],
        google_calendar_api["calendar_ids"][google_calendar_api["calendar"]],
    )

    with open("../docs/days_worked_report.json", "w") as file:
        json.dump(days_worked_report, file)
    with open("../docs/config_report.json", "w") as file:
        json.dump(config_report, file)

    print(f"\nIn {n_days} working days:")
    for individual in days_worked_report.items():
        name = individual[0]
        lead_count = individual[1]["totals"][0][1]
        assist_count = individual[1]["totals"][1][1]
        print(
            f"{name} has been scheduled to lead support {lead_count} times and assist "
            f"{assist_count} times."
        )


if __name__ == "__main__":
    main()
