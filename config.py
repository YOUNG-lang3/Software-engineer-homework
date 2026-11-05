import os

#获取当前文件所在目录——项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#图片存放完整路径
IMAGE_DIR = os.path.join(BASE_DIR, 'images')

#允许返回的图片扩展名
ALLOWED_IMAGE_EXT = ['.jpg', '.jpeg', '.png', '.gif']

#服务器配置
HOST = "0.0.0.0"
PORT = 8000