import argparse
import gcal
import datetime
import pytz
import sys
import json

def setup():
    pass

def print_schedule(events,from_datetime,to_datetime):
    print(f"{'Calendar':=<60}")
    events = [e for e in events if e["from"] >= from_datetime and e["to"] <= to_datetime]
    for event in events:
        print(f'{event["name"]:<40}: {event["from"].strftime("%I:%M%p"):<8} - {event["to"].strftime("%I:%M%p"):<8}')
    print(f"{'':=<60}")
    td_seconds = sum_time_ranges(events)
    total_seconds = td_seconds.total_seconds()
    minutes = total_seconds / 60
    hours = total_seconds / 3600
    print(f"Total hours of scheduled events: {hours}")
    worktime_info = worktimes()
    workday_hours_abs = diff_times(worktime_info["from"], worktime_info["to"])
    print(f'{workday_hours_abs.total_seconds() / 3600} hr workday from {worktime_info["from"].strftime("%I:%M%p")} to {worktime_info["to"].strftime("%I:%M%p")}')
    datetime_now = datetime.datetime.now(pytz.timezone('America/New_York'))
    from_time = max(datetime.datetime.now(pytz.timezone('America/New_York')).time(), worktime_info["from"])
    total_work_time = diff_times(from_time, worktime_info["to"])
    available_time = total_work_time - td_seconds
    print(f'Available Hours: {available_time.total_seconds() / 3600}')
    if (datetime_now.time() < worktime_info["from"]):
        print(f'Hours Until Work: {diff_times(datetime_now.time(), worktime_info["from"]).total_seconds() / 3600}')
    return events

def sum_time_ranges(events):
    import functools
    return functools.reduce(lambda x, y: x + (y["to"] - y["from"]), events, datetime.timedelta())

def worktimes():
    return {
        "from": datetime.time(hour=10),
        "to": datetime.time(hour=17)
    }

def bar_chart(from_dt, to_dt, events):
    seconds = (to_dt - from_dt).total_seconds()
    minutes = seconds / 60
    min_blocks = minutes // 15
    min_block_symbol = " "
    print(f"{' ':<{min_blocks}}")

def diff_times(from_time, to_time):
    return datetime.datetime.combine(datetime.date.min, to_time) - datetime.datetime.combine(datetime.date.min, from_time)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get time info.')
    subparsers = parser.add_subparsers(help='commands')

    event_parser = subparsers.add_parser('events', help='List contents')
    event_parser.add_argument('-l', '--ls', action='store_true', help='List events')
    event_parser.add_argument('--local', action='store_true', help='List events')
    event_parser.add_argument('-n', '--new', action='store', help='New Event')
    event_parser.add_argument('-c', '--clear', action='store_true', help='Clear all events')
    event_parser.add_argument('-e', '--end', action='store', type=int, help='End Event')
    event_parser.add_argument('-t', '--type', action='store', help='Event Type')
    parser.add_argument('-r', '--range', help="time range. i.e: today, week", dest='range')
    args = parser.parse_args()

    if args.new:
        if args.type == "sw":
            import uuid
            with open("local-events.json", "r+") as f:
                curr = json.loads(f.read())
                curr.append({
                    "name": args.new,
                    "from": datetime.datetime.utcnow().isoformat(),
                    "to": ""
                })
                with open("local-events.json", "w+") as fwrite:
                    fwrite.write(json.dumps(curr))
        sys.exit()

    if args.end == 0 or args.end:
        print(f"Editing {args.end}")
        with open("local-events.json", "r+") as f:
            curr = json.loads(f.read())
            for index, event in enumerate(curr):
                if index == args.end:
                    event['to'] = datetime.datetime.utcnow().isoformat()
            with open("local-events.json", "w+") as fwrite:
                fwrite.write(json.dumps(curr))
        sys.exit()

    if args.clear:
        print("clearing events")
        sys.exit()

    if args.ls:
        if args.local:
            print("Listing local events only")
            with open("local-events.json", "r") as f:
                results = json.loads(f.read())
                for index, event in enumerate(results):
                    print(f'{index} - {event["name"]}: {event["from"]} - {event["to"]}')
        else:
            today = datetime.datetime.today()
            recurring_local_events = [
                {
                    "name": "Lunch",
                    "from": datetime.datetime(today.year, today.month, today.day, 12, tzinfo=pytz.timezone('America/New_York')),
                    "to": datetime.datetime(today.year, today.month, today.day, 13, tzinfo=pytz.timezone('America/New_York')),
                }
            ]
            start, end = today_remaining_range()
            all_events = recurring_local_events + events_from_google()
            all_events = sorted(all_events, key=lambda x: x["from"])
            print_schedule(all_events, start, end)
        sys.exit()