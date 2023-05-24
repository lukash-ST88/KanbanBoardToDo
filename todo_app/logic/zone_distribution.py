from datetime import datetime


def get_distributed_entries(entries):
    todo_zone = []
    middle_zone = []
    done_zone = []
    for entry in entries:
        total_lifetime_hour: float = (entry.expiration_date - entry.creation_date).total_seconds() / 3600
        left_lifetime_hour: float = (entry.expiration_date - datetime.now()).total_seconds() / 3600
        time_left_percent: float = left_lifetime_hour / total_lifetime_hour * 100.0
        middle_zone_border_percent: float = 30.0
        cleaning_border_percent: float = -30.0
        if 100 > time_left_percent > middle_zone_border_percent and entry.completed is False:
            todo_zone.append(entry)
        elif middle_zone_border_percent > time_left_percent > 0 and entry.completed is False:
            middle_zone.append(entry)
        elif time_left_percent < cleaning_border_percent:
            continue
        else:
            done_zone.append(entry)
    #     print(time_left_percent, left_lifetime_hour, total_lifetime_hour)
    # print('fffffffffffffffffffffffffffff', todo_zone, middle_zone, done_zone)
    return {
        'todo_zone_entries': todo_zone,
        'middle_zone_entries': middle_zone,
        'done_zone_entries': done_zone
    }
