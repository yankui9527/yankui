from DrissionPage import Chromium
import random

print(fr"""
+----------------------------------------------------------+
 ██    ██     ██     ████     ██ ██   ██ ██     ██ ██
░░██  ██     ████   ░██░██   ░██░██  ██ ░██    ░██░██
 ░░████     ██░░██  ░██░░██  ░██░██ ██  ░██    ░██░██
  ░░██     ██  ░░██ ░██ ░░██ ░██░████   ░██    ░██░██
   ░██    ██████████░██  ░░██░██░██░██  ░██    ░██░██
   ░██   ░██░░░░░░██░██   ░░████░██░░██ ░██    ░██░██
   ░██   ░██     ░██░██    ░░███░██ ░░██░░███████ ░██
   ░░    ░░      ░░ ░░      ░░░ ░░   ░░  ░░░░░░░  ░░           

    作者：言愧    V:YK7871   GitHub:YanKui9527
+----------------------------------------------------------+
""")

url='https://www.zhipin.com/'

web=Chromium().latest_tab
web.get(url)
isdl=web('x://*[@id="header"]/div[1]').text
if '登录' and '注册' in isdl:
    web('x://*[@id="header"]/div[1]/div[4]/div/a').click()
    input('请手动登录后按任意键继续：')

web.wait.eles_loaded('x://*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input')
web('x://*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input').input('python爬虫')
web('x://*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/button').click()

web.wait.eles_loaded('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/span')
web('x://*[@id="wrap"]/div[2]/div[2]/div/div[1]/span').click()
# web.wait.eles_loaded('/html/body/div[4]/div[2]/div[2]/div/ul[2]/li[1]')
web.wait(0.5)
web('x:/html/body/div[4]/div[2]/div[2]/div/ul[2]/li[1]').click()
web.wait(1)
for i in range(20):
    web.scroll.to_bottom()
    web.wait(1)
web.scroll.to_top()

zplb=web.eles('x://*[@id="wrap"]/div[2]/div[3]/div/div/div[1]/ul/div')
for x in zplb:
    print(x.text)
    zp=x.ele('x:./div')
    zp.scroll.to_see().click()
    web('x://*[@id="wrap"]/div[2]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/a[2]').click()
    web.wait(0.5)
    web('x:/html/body/div[10]/div[2]/div[3]/a[1]').click()
    web.wait(random.randint(4, 6))