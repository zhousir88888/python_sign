import os
import requests
import base64
import hashlib
from PIL import Image, ImageDraw, ImageFont

# 读取环境变量
TIAN_API_KEY = os.getenv("TIAN_API_KEY")
QYWX_WEBHOOK = os.getenv("QYWX_WEBHOOK")
if not TIAN_API_KEY:
    raise Exception("TIAN_API_KEY未配置，请在Github Secrets添加")
if not QYWX_WEBHOOK:
    raise Exception("QYWX_WEBHOOK企微机器人地址未配置")

# 获取每日简报新闻
def get_bulletin():
    url = f"https://apis.tianapi.com/bulletin/index?key={TIAN_API_KEY}"
    res = requests.get(url).json()
    print("天行API返回完整数据：", res)
    return res

# 企业微信机器人发送图片
def send_img(img_path, webhook):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        f.seek(0)
        md5 = hashlib.md5(f.read()).hexdigest()
    payload = {
        "msgtype": "image",
        "image": {"base64": b64, "md5": md5}
    }
    requests.post(webhook, json=payload)

if __name__ == "__main__":
    data = get_bulletin()
    news_list = data["result"]["list"]
    date_str = data["result"]["date"]
    week_str = data["result"]["week"]

    # 加载背景图base.jpg
    img = Image.open("base.jpg")
    draw = ImageDraw.Draw(img)
    # 加载黑体，github action会预装文泉驿黑体
    try:
        font_title = ImageFont.truetype("WenQuanYi Zen Hei", 60)
        font_news = ImageFont.truetype("WenQuanYi Zen Hei", 26)
    except:
        font_title = ImageFont.load_default(size=60)
        font_news = ImageFont.load_default(size=26)

    # 绘制顶部星期、日期
    draw.text((450, 80), week_str, font=font_title, fill=(0,180,255))
    draw.text((720, 100), date_str, font=font_news, fill=(80,80,80))

    # 循环绘制新闻条目
    y_pos = 360
    for idx, news in enumerate(news_list):
        text = f"{idx+1}、{news['title']}"
        draw.text((80, y_pos), text, font=font_news, fill=(20,20,20))
        y_pos += 48

    # 保存成品图片
    out_file = "daily_news.jpg"
    img.save(out_file)
    print(f"图片生成成功：{out_file}")
    # 推送图片到企微机器人，微信可收到
    send_img(out_file, QYWX_WEBHOOK)
