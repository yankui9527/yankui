import requests
import random
import datetime

# 配置信息
ran = random.randint(6000, 8000)  # 设置随机步数范围
name = '2826498343@qq.com'  # 账号
pwd = 'afeng1314520'  # 密码
num = None  # 需要刷的步数,如果为空则使用随机步数
p_token = '0f01b0769cc44560a5f942803a542526'  # 推送Token

# 确定步数
if not num:
    num = ran


# 构建HTML模板
def generate_html_content(status, steps=None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = "#28a745" if status == "success" else "#dc3545"
    title = "步数修改成功" if status == "success" else "步数修改失败"
    message = f"恭喜！您的步数已成功修改为 {steps} 步。" if status == "success" else "很遗憾，步数修改失败，请检查您的账号信息。"

    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: {color};
                color: white;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .status-icon {{
                font-size: 48px;
                margin-bottom: 10px;
            }}
            .info-item {{
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #eee;
            }}
            .info-label {{
                font-weight: bold;
                color: #666;
                display: block;
                margin-bottom: 5px;
            }}
            .info-value {{
                font-size: 18px;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 15px;
                text-align: center;
                color: #6c757d;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="status-icon">{f"✅" if status == "success" else "❌"}</div>
                <h2>{title}</h2>
            </div>
            <div class="content">
                <div class="info-item">
                    <span class="info-label">操作结果</span>
                    <span class="info-value">{message}</span>
                </div>
                {f"""<div class="info-item">
                    <span class="info-label">当前步数</span>
                    <span class="info-value">{steps}</span>
                </div>""" if status == "success" else ""}
                <div class="info-item">
                    <span class="info-label">操作时间</span>
                    <span class="info-value">{now}</span>
                </div>
            </div>
            <div class="footer">
                <p>步数助手 • 智能生活</p>
            </div>
        </div>
    </body>
    </html>
    """


# 发送请求修改步数
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://m.cqzz.top',
    'Referer': 'https://m.cqzz.top/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'phone': name,
    'pwd': pwd,
    'num': num,
}

re = requests.post('https://wzz.wangzouzou.com/motion/api/motion/Xiaomi', headers=headers, data=data).json()
tx_url = 'https://www.pushplus.plus/api/send'

# 处理结果并发送通知
if re['code'] == 200:
    print('步数修改成功')
    html_content = generate_html_content("success", num)
    data = {
        'channel': "wechat",
        'content': html_content,
        'template': "html",
        'title': '步数修改成功通知',
        'token': p_token
    }
else:
    print('步数修改失败')
    html_content = generate_html_content("failure")
    data = {
        'channel': "wechat",
        'content': html_content,
        'template': "html",
        'title': '步数修改失败通知',
        'token': p_token
    }

r_tx = requests.post(tx_url, data=data)
print(r_tx.text)