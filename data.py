import csv
import datetime


def create(topic: str, headers: [str]):
    ts = datetime.datetime.now().timestamp()
    name = '{topic}-{timestamp}.csv'.format(topic=topic, timestamp=int(ts))
    with open(name, 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
    return name


def store(filename: str, rows: [[str]]):
    with open(filename, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        for row in rows:
            if len(row) <= 0:
                continue
            csv_writer.writerow(row)

