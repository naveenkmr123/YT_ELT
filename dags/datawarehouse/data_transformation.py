from datetime import timedelta, datetime

SHORTS_MAX_DURATION = 60

def parse_duration(duration_str):

    duration_str = duration_str.replace('P', '').replace('T', '')

    components = ['D', 'H', 'M', 'S']
    values = {'D': 0, 'H': 0, 'M': 0, 'S': 0}

    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)
    
    total_duration = timedelta(days=values['D'],
                               hours=values['H'],
                               minutes=values['M'],
                               seconds=values['S'])

    return total_duration.total_seconds()

def transformed_data(row):

    transformed_row = row.copy()
    duration_seconds = parse_duration(transformed_row['duration'])

    transformed_row['duration'] = duration_seconds


    transformed_row['video_type'] = "Shorts" if duration_seconds <= SHORTS_MAX_DURATION else "Normal"

    return transformed_row



