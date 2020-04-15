from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, ctime
import sys
import requests
import json
import re


per_details = [
	('2018117197', '1234567'),
	('2018117240', '1234567'),
]

def get_data(html):
	old_dict, new_dict = get_raw_data(html)
	PICK_PROPS = ('id', 'uid', 'date', 'created',)
	for prop in PICK_PROPS:
		val = new_dict.get(prop, ...)
		if val is ...:
			raise RuntimeError(f'从网页上提取的 new data 中缺少属性 {prop}，可能网页已经改版。')
			old_dict[prop] = val

	return old_dict


def get_raw_data(html):
	new_data = match_re_group1(r'var def = (\{.+\});', html)
	old_data = match_re_group1(r'oldInfo: (\{.+\}),', html)
	old_dict, new_dict = json.loads(old_data), json.loads(new_data)

	return old_dict, new_dict


def match_re_group1(re_str, text):
	match = re.search(re_str, text) 
	if match is None: 
		raise ValueError(f'在文本中匹配 {re_str} 失败，没找到任何东西。')
	return match.group(1)


def prog(US_NAME, US_PASSWD):
	options = webdriver.ChromeOptions()
	options.add_argument('blink-settings=imagesEnabled=false')
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	browser = webdriver.Chrome(options=options)
	browser.get('https://app.nwu.edu.cn/ncov/wap/default/index')
	wait = WebDriverWait(browser, 5)
	form = wait.until(EC.presence_of_element_located((By.ID, 'casLoginForm')))
	user_input = form.find_element_by_id('username')
	user_input.send_keys(US_NAME)
	pw_input = form.find_element_by_id('password')
	pw_input.send_keys(US_PASSWD)
	sleep(5)
	form.find_element_by_class_name('auth_login_btn').click()
	s = requests.Session()
	for cookie in browser.get_cookies():
		s.cookies.set(cookie['name'],cookie['value'])
	headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest'
	}
	data = get_data(browser.page_source)
	r = s.post('https://app.nwu.edu.cn/ncov/wap/default/save', headers=headers, data=data)
	print('\t', r.text)
	browser.close()
	s.close()
	check(r.text)

def check(response):
	response = json.loads(response)
	result = response.get('m', ...)
	if(result=="操作成功" or result=="今天已经填报了"):
		...
	else:
		raise ValueError('填报信息验证错误，用户密码不对应或网站已变更')

def solve(*pram):
	try:
		prog(*pram)
	except ValueError as e:
		print(e, file=sys.stderr)
		print('%s is ignore'%pram[0], file=sys.stderr)


if __name__ == '__main__':
	for per in per_details:
		print('start', per[0])
		solve(*per)
	print('report over in %s\n\n' % ctime())
