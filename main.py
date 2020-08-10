import argparse
import gcal
import datetime
import pytz
import sys


def print_schedule(events,from_datetime,to_datetime):
    events = [e for e in events if e["from"] >= from_datetime and e["to"] <= to_datetime]
    for event in events:
        print(f'{event["name"]}: {event["from"]} - {event["to"]}')
    return events

def events_from_google():
    event_filters = [
        "Eng Hold: Cut production branch",
        "[Optional] Daily Dose of Team Time (DDOTT)"
    ]
    mapped_events = [
        {
            "name": event["summary"],
            "from": datetime.datetime.fromisoformat(event["start"]["dateTime"]),
            "to": datetime.datetime.fromisoformat(event["end"]["dateTime"])
        } for event in gcal.all_events()
    ]
    return [e for e in mapped_events if e["name"] not in event_filters]

def today_full_range():
    today = datetime.datetime.today()
    day_begin = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0, tzinfo=pytz.timezone('EST'))
    day_end = day_begin.replace(hour=23, minute=59, second=59, microsecond=999999)
    return (day_begin, day_end)

def today_remaining_range():
    today = datetime.datetime.today()
    day_begin = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0, tzinfo=pytz.timezone('America/New_York'))
    now = datetime.datetime.now(pytz.timezone('America/New_York'))
    day_end = day_begin.replace(hour=23, minute=59, second=59, microsecond=999999)
    bedtime = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=22, second=0, tzinfo=pytz.timezone('America/New_York'))
    return (now, bedtime)

def hours_remaining(range_start, range_end, events, unscheduled_blocks=[]):
    print(f"Day end: {range_end}")
    total = range_end - range_start
    scheduled_blocks = [e['to'] - e['from'] for e in events]
    total_scheduled = sum(scheduled_blocks, datetime.timedelta())
    print(f"Total scheduled: {total_scheduled}")
    total_remaining = total - total_scheduled
    print(f"Remaining: {total_remaining}")
    pomodoro_size = datetime.timedelta(minutes=30)
    print(f"Number of pomodoros: {total_remaining / pomodoro_size}")

def add_event():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get time info.')
    subparsers = parser.add_subparsers(help='commands')

    event_parser = subparsers.add_parser('events', help='List contents')
    event_parser.add_argument('-l', '--ls', action='store_true', help='List events')
    event_parser.add_argument('-n', '--new', action='store', help='New Event')
    event_parser.add_argument('-t', '--type', action='store', help='Event Type')


    parser.add_argument('-r', '--range', help="time range. i.e: today, week", dest='range')

    args = parser.parse_args()

    if args.new:
        if args.type:
            print("wohoo")

    if args.ls:
        # Defaults to today
        start, end = today_remaining_range()
        print_schedule(events_from_google(), start, end)
        sys.exit(0)

    events = [
        {
            "name": "Take care of bills",
            "from": datetime.datetime(2020, 8, 9, 12, 59, tzinfo=pytz.timezone('America/New_York')),
            "to": datetime.datetime(2020, 8, 9, 13, 0, tzinfo=pytz.timezone('America/New_York')),
        },
        {
            "name": "Gather all trash",
            "from": datetime.datetime(2020, 8, 9, 15, tzinfo=pytz.timezone('America/New_York')),
            "to": datetime.datetime(2020, 8, 9, 17, tzinfo=pytz.timezone('America/New_York'))
        },
        {
            "name": "Eat bananas",
            "from": datetime.datetime(2020, 8, 12, 15, tzinfo=pytz.timezone('America/New_York')),
            "to": datetime.datetime(2020, 8, 12, 17, tzinfo=pytz.timezone('America/New_York'))
        }

    ]

    # events.extend(gevents)

    start, end = today_remaining_range()
    scheduled_events = print_schedule(events, start, end)
    hours_remaining(start, end, scheduled_events)
