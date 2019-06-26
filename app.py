import time
import ltn.search
import ltn.content
import data

headers = ['主題', '摘要', '日期', '連結']


def is_data_valid(row: [str]):
    valid_flag = True
    for s in row:
        if s is None or s == '':
            valid_flag = False
    return valid_flag


def run(topic: str, on_mission_completed, on_page_completed):
    count = 0
    datas = []
    stack = [ltn.search.by_keyword(topic)]
    file_name = data.create(topic, headers)
    while stack:
        print('第 {} 頁資料爬取開始 ...'.format(count+1))
        result = stack.pop()
        for row in result.rows:
            report = ltn.content.get_report(row.link)
            report_data = [report.title, report.description, report.date, row.link]
            if is_data_valid(report_data):
                datas.append(report_data)
        if result.has_next():
            stack.append(result.next())
        if len(datas) > 10:
            data.store(file_name, datas)
            datas = []
        count+=1
        on_page_completed(topic, count)
        time.sleep(1)
    on_mission_completed()


def on_page_completed(topic: str, page: int):
    print('主題: {} 第 {} 頁資料爬取完成 ...'.format(topic, page))


def on_mission_completed():
    print('任務完成')


run(topic='海嘯', on_mission_completed=on_mission_completed, on_page_completed=on_page_completed)
