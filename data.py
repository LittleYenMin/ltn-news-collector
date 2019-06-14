import csv
import datetime


def create(topic: str, headers: [str]):
    ts = datetime.datetime.now().timestamp()
    name = '{topic}-{timestamp}.csv'.format(topic=topic, timestamp=int(ts))
    with open(name, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
    return name


def store(filename: str, rows: [[str]]):
    with open(filename, 'a') as f:
        csv_writer = csv.writer(f)
        for row in rows:
            csv_writer.writerow(row)

