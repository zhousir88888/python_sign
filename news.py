import os
import requests
from PIL import Image, ImageDraw, ImageFont

# 读取环境变量
TIAN_API_KEY = os.getenv("TIAN_API_KEY")
WECHAT_WEBHOOK = os.getenv("QYWX_WEBHOOK")

# 获取每日简报
def get_bulletin():
    url = f"https://apis.tianapi.com/bulletin/index?key={TIAN_API_KEY}"
    res = requests.get(url).json()
    print("API返回：", res)
    if res["code"] != 200:
        raise Exception(f"接口错误: {res['msg']}")
    return res["result"]["list"]

# 绘制图片
def draw_news(news_list):
    img = Image.open("base.jpg")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("WenQuanYi Zen Hei", 24)
    except:
        font = ImageFont.load_default()
    y = 40
    for item in news_list[:8]:
        text = f"• {item['title']}"
        draw.text((30, y), text, font=font, fill="#222222")
        y += 42
    img.save("news_out.jpg")
    return "news_out.jpg"

# ========== 改用【企微markdown图文消息】，不再上传素材，规避40084报错 ==========
def send_wechat_markdown(news_list):
    content = "## 📰 每日新闻简报\n"
    for idx, item in enumerate(news_list[:8], 1):
        content += f"{idx}. {item['title']}\n\n"

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    resp = requests.post(WECHAT_WEBHOOK, json=payload)
    print("markdown消息返回：", resp.json())

if __name__ == "__main__":
    news_list = get_bulletin()
    draw_news(news_list)
    send_wechat_markdown(news_list)
    print("✅ 任务完成，已推送文字版简报到企微")
