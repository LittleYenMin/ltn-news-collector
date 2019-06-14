import time
import ltn.search
import ltn.content
import data

topic = '地震'
headers = ['主題', '摘要', '日期', '連結']


def run():
    datas = []
    stack = [ltn.search.by_keyword(topic)]
    file_name = data.create(topic, headers)
    while stack:
        print('進行中!!!!')
        result = stack.pop()
        for row in result.rows:
            report = ltn.content.get_report(row.link)
            print(report.title)
            datas.append([report.title, report.description, report.date, row.link])
        if result.has_next():
            stack.append(result.next())
        if len(datas) > 10:
            data.store(file_name, datas)
            datas = []
        time.sleep(3)


run()
