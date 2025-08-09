import requests
from datetime import datetime


def get_weather():
    url = "https://v2.xxapi.cn/api/weather?city=河池巴马"
    headers = {'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                return data['data']
        return None
    except:
        return None


def get_dog_diary():
    url = "https://v2.xxapi.cn/api/dog"
    headers = {'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                return data['data']
        return "今天没有舔狗日记，可能狗狗去追蝴蝶了~"
    except:
        return "舔狗日记获取失败，但我的心永远属于你❤️"


def get_beauty_pic():
    url = "https://v2.xxapi.cn/api/meinvpic"
    headers = {'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                return data['data']
        return "https://via.placeholder.com/600x400?text=Image+Not+Available"
    except:
        return "https://via.placeholder.com/600x400?text=Image+Error"


def generate_html_content():
    # 获取当前日期
    today = datetime.now().strftime("%Y年%m月%d日")

    # 获取数据
    weather_data = get_weather()
    diary = get_dog_diary()
    pic_url = get_beauty_pic()

    # 构建HTML内容
    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .card {{ background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 20px; margin-bottom: 20px; }}
        .header {{ text-align: center; color: #333; border-bottom: 1px solid #eee; padding-bottom: 15px; }}
        .weather-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }}
        .weather-day {{ text-align: center; padding: 10px; border-radius: 8px; background: #f9f9f9; }}
        .diary {{ font-style: italic; line-height: 1.8; color: #555; padding: 15px; background: #fffaf0; border-radius: 8px; }}
        .pic-container {{ text-align: center; margin: 20px 0; }}
        .beauty-pic {{ max-width: 100%; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
        .air-quality {{ display: inline-block; padding: 2px 8px; border-radius: 4px; margin-top: 5px; }}
        .aqi-good {{ background: #e8f5e9; color: #2e7d32; }}
        .aqi-moderate {{ background: #fff8e1; color: #f57f17; }}
    </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>📅 {today} 每日简报</h2>
            </div>
        </div>

        <!-- 天气预报 -->
        <div class="card">
            <h3>🌤️ {weather_data['city']}天气预报</h3>
            <div class="weather-grid">
    """

    # 添加天气预报
    for day in weather_data['data'][:3]:  # 只显示最近3天
        aqi_class = "aqi-good" if "良" in day['air_quality'] else "aqi-moderate"
        html += f"""
        <div class="weather-day">
            <div><strong>{day['date']}</strong></div>
            <div>{day['weather']}</div>
            <div>{day['temperature']}</div>
            <div class="air-quality {aqi_class}">{day['air_quality']}</div>
        </div>
        """

    html += """
            </div>
        </div>

        <!-- 舔狗日记 -->
        <div class="card">
            <h3>🐶 舔狗日记</h3>
            <div class="diary">
                "{}"
            </div>
        </div>

        <!-- 小姐姐图片 -->
        <div class="card">
            <h3>🌸 每日美图</h3>
            <div class="pic-container">
                <img src="{}" alt="小姐姐" class="beauty-pic">
            </div>
        </div>

        <div class="footer">
            <p>💌 每日推送 | 美好生活从清晨开始</p>
        </div>
    </body>
    </html>
    """.format(diary, pic_url)

    return html


# 推送消息
def send_pushplus(content):
    url = 'https://www.pushplus.plus/api/send'
    data = {
        'channel': "wechat",
        'content': content,
        'template': "html",
        'title': "📬 您的每日简报已送达",
        'token': "0f01b0769cc44560a5f942803a542526"  # 请替换为您的真实token
    }
    response = requests.post(url, data=data)
    print("推送状态:", response.text)


# 主程序
if __name__ == "__main__":
    html_content = generate_html_content()
    send_pushplus(html_content)
    print("推送已发送！")