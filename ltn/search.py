import requests
import lxml.html

xpath_formats = {'next_url': "//a[contains(@class, 'p_next')]", 'dates': "//ul[@id='newslistul']/li/span/text()", 'atags': "//ul[@id='newslistul']//a[contains(@class, 'tit')]"}


class Row(object):

    def __repr__(self):
        return '<Row date "{}" title "{}" link "{}">'.format(
            self.date, self.title, self.link)

    def __init__(self, date: str, title: str, link: str):
        self.date = date
        self.title = title
        self.link = link


class Result(object):

    def __repr__(self):
        return '<Result next_url "{}" rows "{}">'.format(
            self.next_url, self.rows)

    def __init__(self, html: str):
        self.rows = []
        self.tree = html

    def has_next(self) -> bool:
        return self.next_url is not None and self.next_url != ''

    def next(self):
        if self.has_next():
            url = 'https:'+self.next_url.attrib['href']
            response = requests.get(url)
            return Result(html=response.content.decode('utf-8'))
        raise ValueError("It's already the last.")

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, html: str):
        self._tree = lxml.html.fromstring(html)
        next_atags = self.tree.xpath(xpath_formats['next_url'])
        dates = self.tree.xpath(xpath_formats['dates'])
        atags = self.tree.xpath(xpath_formats['atags'])
        for next_atag in next_atags:
            self.next_url = next_atag
        for atag, date in zip(atags, dates):
            self.rows.append(Row(date=date, title=atag.text_content(), link=atag.attrib['href']))


def by_keyword(keyword: str) -> Result:
    url = 'https://news.ltn.com.tw/search?keyword={}'.format(keyword)
    response = requests.get(url)
    return Result(html=response.content.decode('utf-8'))
