import os
import requests
import cv2
from cn2an import an2cn

# 从环境变量读取天行API key
TIAN_API_KEY = os.getenv("TIAN_API_KEY")
if not TIAN_API_KEY:
    raise Exception("未配置TIAN_API_KEY环境变量，请在Github Secrets添加")

# 获取每日一句+日期
def get_tian_info():
    url = f"https://api.tianapi.com/tianqi/index?key={TIAN_API_KEY}&city=北京"
    res = requests.get(url).json()
    return res

if __name__ == "__main__":
    print("脚本运行成功，示例：获取API数据")
    data = get_tian_info()
    print(data)
