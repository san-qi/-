import requests
import re
from json import load
from bs4 import BeautifulSoup
from aes_crypt import MyAes


def solve(name, passwd):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/80.0.3987.149 Safari/537.36'
    }
    s = requests.Session()
    s.cookies.set('org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE', 'zh_CN')
    s.headers = headers
    index_url = 'https://app.nwu.edu.cn/ncov/wap/default/index'
    login_page = s.get(index_url)
    data = {'username': name,
            'password': passwd,
            }
    soup = BeautifulSoup(login_page.text, 'html.parser')
    for tag in soup.select('#casLoginForm > input[type=hidden]'):
        data[tag['name']] = tag['value']
    result = re.search(r'var pwdDefaultEncryptSalt = "(\S*)"', login_page.text)
    key = result.group(1)
    aes = MyAes(key)
    data['password'] = aes.encrypt(data['password'])
    s.post(index_url, data=data)
    login_url = 'http://authserver.nwu.edu.cn' + soup.select_one('#casLoginForm')['action']
    s.post(login_url, data=data)
    headers['X-Requested-With'] = 'XMLHttpRequest'
    with open(r'C:\Users\ASUS\Code\nwu_report\s.json', encoding='utf8') as file:
        report_data = load(file)
    r = s.post('https://app.nwu.edu.cn/ncov/wap/default/save', headers=headers, data=report_data)
    print('\t', r.text)
    s.close()


if __name__ == '__main__':
    solve('2018117197', 'hi_world')
