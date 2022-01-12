import re

import requests
from lxml import etree


def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + 1: pos2]
    return ''


headers = {
    'pragma': 'no-cache',

    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
                  'YaBrowser/19.7.0.1635 Yowser/2.5 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
}
page = ''
bookid = ''
def content_downlaod():
    response = requests.get(f'https://fu44.pw/e/action/ShowInfo.php?classid={page}&id={bookid}', headers=headers)
    response.encoding = 'GBK'
    # 解析HTML文档，返回根节点对象
    html = etree.HTML(response.text)

    book_name = str_mid(html.xpath('/html/body/main/div/div[2]/div[1]/h2/text()')[0], '【', '】')
    content = html.xpath("/html/body/main/div/div[2]/div[1]/div[1]/text()")
    print(book_name)

    content_list = []
    for line in content:
        if book_name in line:
            continue
        if '作者' in line:
            author_name = re.sub('作者：', '', line)
            continue
        content_line = re.sub('「', '“', line)
        content_line = re.sub('」', '”\n　　', content_line)
        content_list.append(content_line + '\n')

    file = open(f'{book_name}.txt', 'a', encoding='utf-8')
    file.write(''.join(content_list))
