import os
import requests
from queue import Queue
from concurrent.futures import ThreadPoolExecutor  #多线程
from lxml import etree
class MP3:
    url = 'https://www.myfreemp3.com.cn/'
    hea = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'

    }
    shuju_neir=Queue()
    gequ_lj=Queue()
    def shuju(self,name,page):
        for i in range(1,page+1):
            data = {
                'input': name,
                'filter': 'name',
                'page': i,
                'type': 'netease'
            }

            re=requests.post(self.url,headers=self.hea,data=data).json()['data']['list']
            self.shuju_neir.put((re,name))
    def sjfx(self):
        while True:
            try:
                re,name=self.shuju_neir.get(timeout=5)
            except:
                break
            gswj = f'音乐/{name}'
            if not os.path.exists(f'音乐'):
                os.mkdir(f'音乐')
                print('已经创建音乐文件夹')
            if not os.path.exists(f'{gswj}'):
                os.mkdir(f'{gswj}')
                print(f'已创建"{gswj}"文件夹')
            for x in re:
                gq_lj=x['url']
                gq_title=x['title']
                self.gequ_lj.put((gq_lj,gq_title,gswj))


    def gqxz(self):
        while True:
            try:
                gq_lj,gq_title,gswj=self.gequ_lj.get(timeout=5)
            except:
                break
            gq=requests.get(gq_lj)
            gqwj=f'{gswj}/{gq_title}.mp3'
            if not os.path.exists(gqwj):
                with open(gqwj,'wb') as f:
                    f.write(gq.content)
                    print(f"已经下载歌曲《{gq_title}》")
            else:
                print(f'歌曲《{gq_title}》已存在')


yankui='''
+-----------------------------+
 _ _  ___  _ _  _ __ _ _  _ 
| | || . || \ || / /| | || |
\   /|   ||   ||  \ | ' || |
 |_| |_|_||_\_||_\_\`___'|_|                    
          
作者：言愧       V:YK7871
+-----------------------------+
'''
print(yankui)
a='''
+-----------------------------+
1.关键字批量下载音乐(网易云)
2.关键字查找歌曲下载地址(全网盘)
3.输入其它退出
+-----------------------------+
'''
print(a)
xuhao=int(input('填入上列的输入执行相应程序序号：'))
while True:
    if xuhao==1:
        print('+-------------言愧提醒您当前是批量下载模式-------------+')
        print('注意：如果播放失败，请切换查找下载地址模式手动下载')
        name=input('请输入要批量下载的关键字：')
        page=int(input('请输入要下载的页数(每页最多20首歌，参考网易云列表)：'))
        mp3=MP3()
        with ThreadPoolExecutor(max_workers=5) as tp:
            tp.submit(mp3.shuju,name,page)
            tp.submit(mp3.sjfx)
            tp.submit(mp3.gqxz)
            tp.submit(mp3.gqxz)
            tp.submit(mp3.gqxz)
        break
    elif xuhao==2:
        print('+-----------言愧提醒您当前是网盘查找歌曲下载地址模式-----------+')
        class XZDZ:
            url = 'https://www.kkwpss.com'
            hea = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            }
            dqys = 1
            gq_shuji_list = Queue()
            gq_chuli_list = Queue()

            def gq_dz(self):
                gq_name = input('请输入要搜索歌曲的关键字：')
                print('爬取速度和网络有关，如获取过久请换网络或重试,正在获取中......')
                re = requests.get(f'{self.url}/so/?wd={gq_name}', headers=self.hea)
                re.encoding = 'UTF-8'
                e = etree.HTML(re.text)
                tit = e.xpath('//div[2]/p/text()')
                lj = e.xpath('//div[2]/a/@href')
                if_kong = e.xpath('/html/body/div[3]/div[3]/text()')
                yeshu = e.xpath('/html/body/div[3]/div[3]/a/@href')[:-1]
                zong_yeshu = e.xpath('/html/body/div[3]/div[3]/a/text()')[:-1]
                if yeshu != []:
                    print(f'已经爬取第[{self.dqys}]页....共[{zong_yeshu[-1]}]页')
                    self.gq_shuji_list.put((tit, lj, yeshu, e, zong_yeshu))
                else:
                    yeshu = [f'/so/?wd={gq_name}']
                    zong_yeshu = ['1']
                    print(f'已经获取完第[1]页，正在数据处理...')
                    self.gq_shuji_list.put((tit, lj, yeshu, e, zong_yeshu))

            def xyy_sj(self):
                while True:
                    try:
                        tit, lj, yeshu, e, zong_yeshu = self.gq_shuji_list.get(timeout=5)
                    except:
                        break
                    for ys in yeshu:
                        re2 = requests.get(self.url + ys, headers=self.hea)
                        re2.encoding = 'utf-8'
                        e2 = etree.HTML(re2.text)
                        tit2 = e2.xpath('//div[2]/p/text()')
                        lj2 = e2.xpath('//div[2]/a/@href')
                        tit = tit + tit2
                        lj = lj + lj2
                        self.gq_chuli_list.put((tit, lj))
                        self.dqys += 1
                        if zong_yeshu != ['1']:
                            print(f'已经获取完第[{self.dqys}]页....共[{zong_yeshu[-1]}]页')

            def gq_cl(self):
                while True:
                    try:
                        tit, lj = self.gq_chuli_list.get(timeout=10)
                    except:
                        break
                    gequ = []
                    xuhao = 1
                    for x, y in zip(tit, lj):
                        if xuhao == 1:
                            print('获取到以下歌曲：')
                        gequ.append((x, y))
                        print(f'{xuhao}.{x}')
                        xuhao = xuhao + 1
                    while True:
                        gq_xh = int(input('请输入歌曲序号获取链接：'))
                        print('正在获取网盘地址...')
                        re3 = requests.get(self.url + gequ[gq_xh - 1][1], headers=self.hea)
                        e3 = etree.HTML(re3.text)
                        e3 = e3.xpath('//div[1]/div[2]/p/a/@href')
                        print(f'歌曲《{gequ[gq_xh - 1][0]}》，网盘下载地址为：{e3}')
        xzdz = XZDZ()
        xzdz.gq_dz()
        xzdz.xyy_sj()
        xzdz.gq_cl()
    else:
        break
