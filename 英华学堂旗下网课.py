import requests
import ddddocr
import os
from lxml import etree
import time

name='xxxxx'
pas='xxxxxx'



url = 'https://bwgl.yuruixxkj.com'

s=requests.session()#自动保存cookie等
dd=ddddocr.DdddOcr()

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://bwgl.zjxkeji.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://bwgl.zjxkeji.com/user/login',
    'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'token=sid.CXoucAn6yOoFvU1tdFXIaL2x4Bca5R; __root_domain_v=.zjxkeji.com; _qddaz=QD.689260958636510; _qdda=3-1.2rijjb; _qddab=3-ac08gy.mgz1b0sd',
}
#识别验证码
def get_ocr():
    ocr_url=f'{url}/service/code'
    img=s.get(ocr_url,headers=headers)
    with open('ocr.jpg','wb') as f:
        f.write(img.content)
    with open('ocr.jpg','rb') as f:
        img_bytes=f.read()
        code=dd.classification(img_bytes)
    os.remove('ocr.jpg')
    print(f"当前验证码是:{code}")
    return code


def get_dl():
    data = {
        'username': name,
        'password': pas,
        'code': get_ocr(),
    }

    response = s.post(f'{url}/user/login', headers=headers, data=data)
    print(response.json())


def get_kb():
    get_dl()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': f'{url}/user/index',
        'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
        # 'cookie': 'token=sid.CXoucAn6yOoFvU1tdFXIaL2x4Bca5R; __root_domain_v=.zjxkeji.com; _qddaz=QD.689260958636510; _qdda=3-1.2rijjb; _qddab=3-ac08gy.mgz1b0sd',
    }

    response = s.get(f'{url}/user/index', headers=headers)
    e=etree.HTML(response.text)
    kb_list=e.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[4]')
    kc_id_list=[]
    for i in kb_list:
        kb_title=i.xpath('./div/div/div[2]/div[1]/a/text()')
        kb_url=i.xpath('./div/div/div[2]/div[1]/a/@href')
        kb_jd=i.xpath('./div/div/div[2]/div[3]/div[3]/text()')
        for x,y,z in zip(kb_title,kb_url,kb_jd):
            if '100%' not in z:
                kc_id=y.split('Id=')[1]
                kc_id_list.append(kc_id)
                print(f'《{x}》未完成')
            # print(f'{kb_title[0]}:{kb_jd[0]} {kb_url[0]}')

    print(f'未完成课程ID:{kc_id_list}')
    return kc_id_list

def get_nodeId():
    kc_idlist=get_kb()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': f'{url}/user/course/announcement?courseId=1011541',
        'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
        # 'cookie': 'token=sid.CXoucAn6yOoFvU1tdFXIaL2x4Bca5R; __root_domain_v=.zjxkeji.com; _qddaz=QD.689260958636510; _qdda=3-1.2rijjb; _qddab=3-ac08gy.mgz1b0sd',
    }
    nodeIdlist = []
    for kc_id in kc_idlist:
        params = {
            'courseId': kc_id,
        }

        re = s.get(f'{url}/user/course/chapter', params=params,
                                headers=headers)
        e=etree.HTML(re.text)

        ztext=e.xpath('//div[@class="tit"]//a/text()')
        ztext_url=e.xpath('//div[@class="tit"]//a/@href')
        for i in ztext_url:
            nodeId=i.split('nodeId=')[1]
            nodeIdlist.append(nodeId)
    print(f'课程的nodeId为{nodeIdlist}')
    return nodeIdlist


def get_token():
    data = {
        'username': name,
        'password': pas,
    }

    response = s.post(f'{url}/api/login', data=data)
    # print(response.json())
    token=response.json()['result']['data']['token']
    return token

def dq_time(nodeId):
    data = {
        'token': token,
        'nodeId': nodeId
    }
    re3 = s.post(f'{url}/api/node/video', data=data).json()
    # print(re3)
    print(f"课程id:{nodeId},总时长为:{re3['result']['data']['videoDuration']}")
    if re3['result']['data']['study_total'] != []:
        kc_time = re3['result']['data']['study_total']['duration']
    else:
        kc_time = 0
    return [kc_time,re3['result']['data']['videoDuration']]

def Shua_kc():
    nodeIdlist=get_nodeId()

    kc_list={}
    for nodeId in nodeIdlist:
        data = {
            'token': token,
            'nodeId': nodeId
        }
        re3 = s.post(f'{url}/api/node/video', data=data).json()
        # print(re3)
        print(f"课程id:{nodeId},总时长为:{re3['result']['data']['videoDuration']}")
        if re3['result']['data']['study_total']!=[]:
            print(f"课程id{nodeId}已观看时长为:{re3['result']['data']['study_total']['duration']}")
            kc_time=re3['result']['data']['study_total']['duration']
        else:
            print(f"课程id{nodeId}已观看时长为:0")
            kc_time=0
        if int(re3['result']['data']['videoDuration'])>=int(kc_time):
            kc_list[nodeId]=[re3['result']['data']['videoDuration'],kc_time]#课程id，课程总时长，已观看时长
    print(kc_list)

    for nodeId,kc_time in kc_list.items():
        sta_time=kc_time[1]
        studyId=0
        studyTime=1
        data2 = {
            'token': token,
            'nodeId': nodeId,
            'studyTime': studyTime,
            'studyId': studyId
        }
        re_sk=s.post(f'{url}/api/node/study', data=data2).json()
        studyId=re_sk['result']['data']['studyId']
        while True:
            studyTime+=1
            data = {
                'token': token,
                'nodeId': nodeId,
                'studyTime': studyTime,
                'studyId': studyId
            }
            re_sk=s.post(f'{url}/api/node/study', data=data).json()
            studyId=re_sk['result']['data']['studyId']
            if re_sk['msg']=='提交学时成功!':
                a,b=dq_time(nodeId)
                print(f'课程id:{nodeId},提交学时成功!当前进度{a}/{b}')
            else:
                print(f'课程id:{nodeId},提交学时失败！')
            time.sleep(1)
            if int(a)==int(b):
                break



if __name__ == '__main__':
    token=get_token()
    Shua_kc()
