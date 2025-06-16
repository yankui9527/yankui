import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
from random import randint

def yankui():
    x=randint(0,2)
    yankui1 = r'''
+-----------------------------+
 _ _  ___  _ _  _ __ _ _  _ 
| | || . || \ || / /| | || |
\   /|   ||   ||  \ | ' || |
 |_| |_|_||_\_||_\_\`___'|_|                    

作者：言愧       V:YK7871
+-----------------------------+
'''

    yankui2=r'''
+----------------------------------------------------+
 ██    ██     ██     ████     ██ ██   ██ ██     ██ ██
░░██  ██     ████   ░██░██   ░██░██  ██ ░██    ░██░██
 ░░████     ██░░██  ░██░░██  ░██░██ ██  ░██    ░██░██
  ░░██     ██  ░░██ ░██ ░░██ ░██░████   ░██    ░██░██
   ░██    ██████████░██  ░░██░██░██░██  ░██    ░██░██
   ░██   ░██░░░░░░██░██   ░░████░██░░██ ░██    ░██░██
   ░██   ░██     ░██░██    ░░███░██ ░░██░░███████ ░██
   ░░    ░░      ░░ ░░      ░░░ ░░   ░░  ░░░░░░░  ░░ 
         作者：言愧       V:YK7871
+----------------------------------------------------+
'''
    yankui3=r'''
+--------------------------------------------------------------+
  ___    ___ ________  ________   ___  __    ___  ___  ___     
 |\  \  /  /|\   __  \|\   ___  \|\  \|\  \ |\  \|\  \|\  \    
 \ \  \/  / | \  \|\  \ \  \\ \  \ \  \/  /|\ \  \\\  \ \  \   
  \ \    / / \ \   __  \ \  \\ \  \ \   ___  \ \  \\\  \ \  \  
   \/  /  /   \ \  \ \  \ \  \\ \  \ \  \\ \  \ \  \\\  \ \  \ 
 __/  / /      \ \__\ \__\ \__\\ \__\ \__\\ \__\ \_______\ \__\
|\___/ /        \|__|\|__|\|__| \|__|\|__| \|__|\|_______|\|__|
\|___|/                                                        
              作者：言愧       V:YK7871
+--------------------------------------------------------------+
'''
    yankui_list=[yankui1,yankui2,yankui3]
    print(yankui_list[x])
yankui()
print('注意：该脚本需Edge浏览器，请自行检查电脑是否已安装')
zh=str(input('请输入学号（回车确定）：'))
mm=str(input('请输入密码（回车确定）：'))
print('正在启动脚本.....')
url='http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/kscj/cjcx_list'
wz=webdriver.Edge()
wz.get(url)
wz.implicitly_wait(5)
# yzm=input('请输入登录的验证码(回车确定):')
wz.find_element(By.XPATH,'//*[@id="userAccount"]').send_keys(zh)
wz.find_element(By.XPATH,'//*[@id="userPassword"]').send_keys(mm)
wz.find_element(By.XPATH,'//*[@id="btnSubmit"]').click()
print('已经点击登录')
wz.implicitly_wait(3)
try:
    wz.find_element(By.XPATH,'/html/body/div[5]/a[2]/div/div[1]/static').click()
    print('已经点击学生评教')
except:
     input('登录失败，请重试,输入任意键退出：')
     wz.quit()
wz.implicitly_wait(3)
wz.find_element(By.XPATH,'//*[@id="Form1"]/table/tbody/tr[2]/td[7]/a').click()
print('已经进入到评教')
pjnr=wz.page_source
et=etree.HTML(pjnr)
kec=et.xpath('//*[@id="dataList"]/tbody/tr/td[3]/text()')
sfpj=et.xpath('//*[@id="dataList"]/tbody/tr/td[7]/text()')
zid={}
pj_cz=2
for x,y in zip(kec,sfpj):
    print(f'获取到课程:《{x}》，是否已评教：{y}')
    zid[x]=[x,y,f'//*[@id="dataList"]/tbody/tr[{pj_cz}]/td[9]/a']
    pj_cz+=1
for x in zid:
    if zid[x][1]=='否':
        wz.find_element(By.XPATH, zid[x][2]).click()
        wz.implicitly_wait(3)
        for c in range(3,21):
            if c==7 or c==12 or c==17:
                continue
            wz.find_element(By.XPATH, f'//form/table[1]/tbody/tr[{c}]/td[2]/input[1]').click()
        wz.find_element(By.XPATH, '//*[@id="tj"]').click()
        wz.switch_to.alert.accept()
        time.sleep(0.3)
        wz.switch_to.alert.accept()
        print(f'已经提交课程《{x}》评教')
    else:
        print(f'课程《{x}》已评教')


input('输入任意键后退出：')
wz.quit()




