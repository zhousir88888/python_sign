import os
import requests
from PIL import Image, ImageDraw, ImageFont

# 从Github Actions的Secrets读取密钥
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

# 推送到企微机器人（修复40088报错版本）
def send_wechat(img_path):
    # 把webhook链接拆出key
    # webhook格式：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx
    key = WECHAT_WEBHOOK.split("key=")[1]
    upload_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=image"
    
    # 1.上传图片获取media_id
    with open(img_path, "rb") as f:
        upload_res = requests.post(upload_url, files={"media": f}).json()
    print("图片上传结果：", upload_res)
    if upload_res.get("errcode") != 0:
        raise Exception(f"图片上传失败：{upload_res}")
    media_id = upload_res["media_id"]

    # 2.发送图片消息
    send_data = {
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }
    send_res = requests.post(WECHAT_WEBHOOK, json=send_data).json()
    print("消息发送结果：", send_res)
    if send_res.get("errcode") != 0:
        raise Exception(f"消息发送失败：{send_res}")

# 程序入口，自动执行整套流程
if __name__ == "__main__":
    news_list = get_bulletin()
    img_file = draw_news(news_list)
    send_wechat(img_file)
    print("✅ 全部任务执行完成")
