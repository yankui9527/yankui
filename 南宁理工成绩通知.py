import requests
import execjs
from bs4 import BeautifulSoup
import re

name = '22060738'  # 登录的学号
pas = 'AAbbcc11!'  # 密码
kksj = '2024-2025-2'  # 开学日期

s = requests.Session()


def nnlg_jm(zm):
    js = """
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
    ex = execjs.compile(js)
    jm_zh = ex.call('encodeInp', str(zm))
    return jm_zh


def nnlg_dl():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://bwgljw.yinghuaonline.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/xk/LoginToXk',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    }

    data = {
        'encoded': f'{nnlg_jm(name)}%%%{nnlg_jm(pas)}',
    }

    re = s.post(
        'http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/xk/LoginToXk',
        headers=headers,
        data=data,
        verify=False,
    )

    cj_data = {
        'kksj': kksj,
        'kcxz': '',
        'kcmc': '',
        'xsfs': 'all',
    }

    re2 = s.post(
        'http://bwgljw.yinghuaonline.com/gllgdxbwglxy_jsxsd/kscj/cjcx_list',
        headers=headers,
        data=cj_data,
        verify=False,
    )
    return re2.text


def extract_scores(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'dataList'})

    if not table:
        return "未找到成绩表格"

    scores = []
    rows = table.find_all('tr')[1:]  # 跳过表头

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 11:  # 确保有足够的列
            semester = cols[1].get_text(strip=True)
            course_id = cols[2].get_text(strip=True)
            course_name = cols[3].get_text(strip=True)
            score = cols[4].get_text(strip=True)
            credit = cols[6].get_text(strip=True)

            scores.append({
                '学期': semester,
                '课程编号': course_id,
                '课程名称': course_name,
                '成绩': score,
                '学分': credit
            })

    return scores


def format_html_content(scores, kksj):
    if not scores:
        return "<h3>本学期暂无成绩数据</h3>"

    # 创建HTML内容
    html_content = f"""
    <div style="font-family: 'Microsoft YaHei', sans-serif; max-width: 600px; margin: 0 auto; background-color: #f8f9fa; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px;">南宁理工学院成绩通知</h2>
        <p style="font-size: 16px; color: #7f8c8d; text-align: center;">学期: <strong style="color: #e74c3c;">{kksj}</strong></p>

        <div style="margin-top: 20px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 5px rgba(0,0,0,0.05);">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #3498db; color: white;">
                        <th style="padding: 12px 8px; text-align: left;">课程名称</th>
                        <th style="padding: 12px 8px; text-align: center;">成绩</th>
                        <th style="padding: 12px 8px; text-align: center;">学分</th>
                    </tr>
                </thead>
                <tbody>
    """

    # 添加成绩行
    for i, score in enumerate(scores):
        bg_color = "#f2f2f2" if i % 2 == 0 else "#ffffff"
        html_content += f"""
                    <tr style="border-bottom: 1px solid #eee; background-color: {bg_color};">
                        <td style="padding: 12px 8px; border-bottom: 1px solid #eee;">
                            <div style="font-weight: bold;">{score['课程名称']}</div>
                            <div style="font-size: 12px; color: #7f8c8d;">{score['课程编号']} | {score['学期']}</div>
                        </td>
                        <td style="padding: 12px 8px; text-align: center; border-bottom: 1px solid #eee; font-weight: bold; color: #e74c3c;">{score['成绩']}</td>
                        <td style="padding: 12px 8px; text-align: center; border-bottom: 1px solid #eee;">{score['学分']}</td>
                    </tr>
        """

    html_content += """
                </tbody>
            </table>
        </div>

        <div style="margin-top: 20px; text-align: center; color: #95a5a6; font-size: 14px;">
            <p>© 南宁理工学院成绩查询系统 | 自动推送</p>
        </div>
    </div>
    """

    return html_content


def nnlg_ts():
    html_content = nnlg_dl()
    scores = extract_scores(html_content)
    formatted_content = format_html_content(scores, kksj)

    tx_url = 'https://www.pushplus.plus/api/send'
    data = {
        'channel': "wechat",
        'content': formatted_content,
        'template': "html",
        'title': f'南宁理工成绩通知 - {kksj}学期',
        'token': "0f01b0769cc44560a5f942803a542526"
    }

    r_tx = requests.post(tx_url, data=data)
    print(f"推送结果: {r_tx.json()}")


if __name__ == '__main__':
    nnlg_ts()