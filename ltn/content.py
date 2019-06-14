import requests
import lxml.html


class ContentReport(object):

    def __repr__(self):
        return '<ContentReport date "{}" title "{}" description "{}">'.format(
            self.date, self.title, self.description)

    def __init__(self, html: str):
        self.html = html

    @property
    def html(self) -> str:
        return self._html

    @html.setter
    def html(self, html: str):
        self._html = html
        self.tree = lxml.html.fromstring(self._html)
        self.description = self.__get_from_path(xpath='/html/head/meta[@name="description"]/@content')
        self.title = self.__get_from_path(xpath='/html/body//div[contains(@class,"articlebody")]/h1/text()')
        self.date = self.__get_from_path(xpath='/html/body//span[contains(@class, "viewtime")]/text()')

    def __get_from_path(self, xpath: str) -> str:
        results = self.tree.xpath(xpath)
        return results[0] if results is not None and len(results) > 0 else None


def get_report(url: str) -> ContentReport:
    response = requests.get('https://news.ltn.com.tw/'+url)
    return ContentReport(html=response.content.decode('utf-8'))
