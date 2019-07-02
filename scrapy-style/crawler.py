from time import sleep

import requests
import lxml.html
from requests import Response

xpath_formats = {'next_url': "//a[contains(@class, 'p_next')]", 'dates': "//ul[@class='searchlist']/li/span/text()", 'atags': "//a[contains(@class, 'tit')]"}


def go(keyword: str):
    url = 'https://news.ltn.com.tw/topic/{}'.format(keyword)
    for content in run(requests.get(url)):
        sleep(1)
        yield content


def run(response: Response):
    tree = lxml.html.fromstring(response.content.decode('utf-8'))
    next_atags = tree.xpath(xpath_formats['next_url'])
    dates = tree.xpath(xpath_formats['dates'])
    atags = tree.xpath(xpath_formats['atags'])
    for atag, date in zip(atags, dates):
        href = atag.attrib['href']
        yield get_content(requests.get('https://news.ltn.com.tw/'+href))
    if next_atags:
        next_url = next_atags[0].attrib['href']
        if next_url:
            yield from run(requests.get('https:'+next_url))


def get_content(response: Response):
    tree = lxml.html.fromstring(response.content.decode('utf-8'))
    description = tree.xpath('/html/head/meta[@name="description"]/@content')
    title = tree.xpath('/html/body//div[contains(@class,"articlebody")]/h1/text()')
    date = tree.xpath('/html/body//span[contains(@class, "viewtime")]/text()')
    return {
        'url': response.url,
        'title': title[0] if title else None,
        'date': date[0] if date else None,
        'description': description[0] if description else None,
    }


for content in go('地震'):
    print(content)
