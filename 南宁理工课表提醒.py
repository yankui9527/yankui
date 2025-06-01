import requests
import execjs
from lxml import etree
import datetime

s = requests.session()

zdata='2025-3-3@22060738@AAAbbb123!'
def nnlg_fg(zdata):
    zhdata=zdata.split('@')
    return zhdata
def nnlg_jm(xh,mm):
    js="""
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    function encodeInp(input) {
        var output = "";
        var chr1, chr2, chr3 = "";
        var enc1, enc2, enc3, enc4 = "";
        var i = 0;
        do {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);
            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;
            if (isNaN(chr2)) {
                enc3 = enc4 = 64
            } else if (isNaN(chr3)) {
                enc4 = 64
            }
            output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) + keyStr.charAt(enc3) + keyStr.charAt(enc4);
            chr1 = chr2 = chr3 = "";
            enc1 = enc2 = enc3 = enc4 = ""
        } while (i < input.length);
        return output
    }
    """
    ex=execjs.compile(js)
    jm_zh=ex.call('encodeInp', str(xh))
    jm_mm=ex.call('encodeInp', str(mm))
    jmdata=jm_zh+'%%%'+jm_mm
    return jmdata

def get_xnxq():
    nnlg_xnxq='http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/xskb/xskb_list.do'
    xnxq=s.post(nnlg_xnxq)
    e=etree.HTML(xnxq.text)
    get_xnxq=e.xpath('//*[@id="xnxq01id"]/option[1]/text()')
    return get_xnxq

def nnlg_hqzs(start_date_str, target_date_str=None):
    """
    计算从开学日期到目标日期的周数

    参数:
        start_date_str (str): 开学日期，格式为"YYYY-MM-DD"
        target_date_str (str, optional): 目标日期，格式为"YYYY-MM-DD"。默认使用今天的日期。

    返回:
        dict: 包含周数和本周日期范围的字典
    """
    try:
        # 转换开学日期
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()

        # 转换目标日期，如果未提供则使用今天
        if target_date_str:
            target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").date()
        else:
            target_date = datetime.date.today()

        # 验证日期逻辑
        if target_date < start_date:
            raise ValueError(f"目标日期 {target_date} 在开学日期 {start_date} 之前")

        # 计算周数
        delta = target_date - start_date
        weeks = (delta.days // 7) + (1 if delta.days % 7 > 0 else 0)

        # 计算本周的日期范围
        days_into_week = delta.days % 7
        week_start = target_date - datetime.timedelta(days=days_into_week)
        week_end = week_start + datetime.timedelta(days=6)

        # 获取星期几的名称
        weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday = weekday_names[target_date.weekday()]

        return {
            "start_date": start_date,
            "target_date": target_date,
            "week_number": max(weeks, 1),  # 至少是第1周
            "week_start": week_start,
            "week_end": week_end,
            "weekday": weekday
        }
    except ValueError as ve:
        print(f"日期格式错误: {ve}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None
def huoqu_kc():
    url = 'http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/xk/LoginToXk'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://bwgljw.yinghuaonline.com',
        'Referer': 'http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        # 'Cookie': 'JSESSIONID=926958552521CEC28B17C6655AA34BFF',
    }
    data = {
        'encoded': nnlg_jm(nnlg_fg(zdata)[1],nnlg_fg(zdata)[2]),
    }
    re=s.post(url,headers=headers,data=data)
    result = nnlg_hqzs(nnlg_fg(zdata)[0])
    data = [
        ('zc', '12'),
        # ('zc', result['week_number']),
        ('xnxq01id', get_xnxq()),
        ('sfFD', '1'),
    ]
    get_kccj=s.post('http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/xskb/xskb_list.do',headers=headers,data=data)
    return get_kccj.text,result

def nnlg_tuisong():
    sour=huoqu_kc()[0]
    dqrq=huoqu_kc()[1]['target_date']
    dqzs=huoqu_kc()[1]['weekday']
    djz=huoqu_kc()[1]['week_number']
    zdict={
        '周一':1,
        '周二':2,
        '周三':3,
        '周四':4,
        '周五':5,
        '周六':6,
        '周日':7,
    }

    e=etree.HTML(sour)
    djkc={}
    for j in range(1,8):
        zongkc = []
        for i in range(2,8):
            a=e.xpath(f'//tr[{i}]/td[{j}]/*[@class="kbcontent"]//text()')
            a=[x.strip() for x in a]
            # print(a)
            zongkc.append(a)
        djkc[j]=zongkc
    # print(djkc[zdict[dqzs]])
    pus_tit=f'{dqrq} ({dqzs})的课表'
    pus_content=f'星期一的课表\n\n第一节：{djkc[1][0]}\n\n第二节：{djkc[1][1]}\n\n第三节：{djkc[1][2]}\n\n第四节：{djkc[1][3]}\n\n第五节：{djkc[1][4]}\n\n第六节：{djkc[1][5]}'
    tx_url = 'https://www.pushplus.plus/api/send'
    data = {
        'channel': "wechat",
        'content': pus_content,
        'template': "txt",
        'title': pus_tit,
        'token': "0f01b0769cc44560a5f942803a542526"
    }
    r_tx = requests.post(tx_url, data=data)
    print(r_tx.text)
if __name__ == '__main__':
    nnlg_tuisong()

