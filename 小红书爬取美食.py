from DrissionPage import Chromium

#pip install DrissionPage  安装库


url='https://www.xiaohongshu.com/explore'

data={}

web=Chromium().latest_tab
web.get(url)

web('x://*[@id="search-input"]').input('南宁美食推荐')
web.wait(1.5)
web('x://*[@id="global"]/div[1]/header/div[1]/div[1]/div[2]').click()
# web.wait.eles_loaded('x://*[@id="global"]/div[2]/div[2]/div/div/div[3]/div[1]/section[1]')
web.wait(1)
web('x://*[@id="image"]').click()
web.wait.eles_loaded('x://*[@id="global"]/div[2]/div[2]/div/div/div[3]/div[1]/section[1]')
web.scroll.down(100)
for cs in range(1):
    web.wait(2)
    web.scroll.down(400)
    web.wait.eles_loaded('x://*[@id="global"]/div[2]/div[2]/div/div/div[3]/div[1]/section')
    meis_list = web.eles('x:/html/body/div[2]//section')
    if meis_list != []:
        for mei in meis_list:
            tit = mei('x:./div//span')
            if '大家都在搜' in tit.text:
                continue
            tit.click()
            web.wait.eles_loaded('x:/html/body/div[5]/div[1]/div[4]/div[2]/div[1]/div[2]/span/span[1]/text()')
            neir=web.ele('x://*[@id="detail-desc"]/span').text

            print(f'当前标题：《{tit.text}》\n当前内容：{neir}\n')
            data[tit.text]=neir
            web('x:/html/body/div[5]/div[2]/div').click()
            web.wait(1)
    else:
        web.scroll.down(400)

print(data)