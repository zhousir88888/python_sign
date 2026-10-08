import os
import base64
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

# 图片转base64
def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 企微原生图片消息
def send_wechat_image(base64_str):
    payload = {
        "msgtype": "image",
        "image": {
            "base64": base64_str
        }
    }
    resp = requests.post(WECHAT_WEBHOOK, json=payload)
    print("图片消息返回：", resp.json())

# 文字简报
def send_wechat_text(news_list):
    content = "📰 每日新闻简报\n"
    for idx, item in enumerate(news_list[:8],1):
        content += f"{idx}. {item['title']}\n"
    payload = {
        "msgtype": "text",
        "text": {"content": content}
    }
    resp = requests.post(WECHAT_WEBHOOK, json=payload)
    print("文字消息返回：", resp.json())

if __name__ == "__main__":
    news_list = get_bulletin()
    img_file = draw_news(news_list)
    b64 = img_to_base64(img_file)
    send_wechat_image(b64)
    send_wechat_text(news_list)
    print("✅ 任务完成：图片+文字两条消息推送到企微")
