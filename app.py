import time
import ltn.search
import ltn.content
import data

topic = '土石流'
headers = ['主題', '摘要', '日期', '連結']


def run():
    count = 0
    datas = []
    stack = [ltn.search.by_keyword(topic)]
    file_name = data.create(topic, headers)
    while stack:
        print('進行中!!!!')
        result = stack.pop()
        for row in result.rows:
            report = ltn.content.get_report(row.link)
            datas.append([report.title, report.description, report.date, row.link])
        if result.has_next():
            stack.append(result.next())
        if len(datas) > 10:
            data.store(file_name, datas)
            datas = []
        count+=1
        print('本頁完成! 已完成: {}頁, 下頁即將開始...'.format(count))
        time.sleep(3)
    print('任務完成!!!')


run()
