import requests
from PIL import Image, ImageDraw, ImageFont
import base64

TIAN_API_KEY = "6c3682ccc08984c603332eba6ec1f82b"
WECHAT_WEBHOOK = ""

# 获取每日简报
def get_bulletin():
    url = f"https://apis.tianapi.com/bulletin/index?key={TIAN_API_KEY}"
    res = requests.get(url).json()
    print("API返回：", res)
    if res["code"] != 200:
        raise Exception(f"接口错误：{res['msg']}")
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

# 推送到企微机器人
def send_wechat(img_path):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "msgtype": "image",
        "image": {"base64": b64, "md5": ""}
    }
    requests.post(WECHAT_WEBHOOK, json=payload)

if __name__ == "__main__":
    news = get_bulletin()
    img_file = draw_news(news)
    # send_wechat(img_file)
