# 导入
from wxauto import WeChat
import time
import requests


from openai import OpenAI
def ai(hua):
    client = OpenAI(api_key="sk-387afe10ae574bffb101ba01f3b3f5aa", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个温柔的女友形象，名字叫小丽，我们非常恩爱"},
            {"role": "user", "content": hua},
        ],
        stream=False
    )

    return(response.choices[0].message.content)

# 获取微信窗口对象
wx = WeChat()
# 输出 > 初始化成功，获取到已登录窗口：xxxx

# 设置监听列表
listen_list = [
    '言愧'
]
# 循环添加监听对象
for i in listen_list:
    wx.AddListenChat(who=i, savepic=True)

# 持续监听消息，并且收到消息后回复“收到”
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who  # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)  # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type  # 获取消息类型
            content = msg.content  # 获取消息内容，字符串类型的消息内容
            print(f'【{who}】：{content}')


            if msgtype == 'friend':
                chat.SendMsg(ai(content))
    time.sleep(wait)