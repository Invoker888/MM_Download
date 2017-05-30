import urllib.request
import os
import random


def get_page(url):
    html = url_open(url).decode('utf-8')

    a = html.find('current-comment-page') + 23
    b = html.find(']', a)

    return html[a:b]


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')

    # 代理失败，拒绝访问
    # proxies = ['119.6.144.70:81', '111.1.36.9:80', '203.144.144.162:8080']
    # proxy = random.choice(proxies)
    #
    # proxy_support = urllib.request.ProxyHandler({'http': proxy})
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)

    response = urllib.request.urlopen(url)
    html = response.read()

    return html


def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []

    a = html.find('img src=')

    while a != -1:
        b = html.find('.jpg', a, a + 255)
        if b != -1:
            img_addrs.append(html[a + 9:b + 4])
        else:
            b = a + 9

        a = html.find('img src=', b)

    return img_addrs


def save_imgs(folder, img_addrs):
    for each in img_addrs:
        if each.find('http:'):
            each = 'http:' + each
        else:
            continue
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:
            img = url_open(each)
            f.write(img)
        # print(each)


def download_mm(folder='OOXX', pages=10):
    if not os.path.exists('OOXX'):
        os.mkdir(folder)
    os.chdir(folder)

    url = "http://jandan.net/ooxx/"
    page_num = int(get_page(url))

    pages = int(input('Enter the bunch number of download picture you want:'))
    for i in range(pages):
        page_num -= i
        page_url = url + 'page-' + str(page_num) + '#comments'
        img_addrs = find_imgs(page_url)
        save_imgs(folder, img_addrs)


if __name__ == '__main__':
    download_mm()
