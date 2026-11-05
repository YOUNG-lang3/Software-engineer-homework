from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from config import ALLOWED_IMAGE_EXT, BASE_DIR, HOST, IMAGE_DIR, PORT
import os
import random

app = FastAPI(title="随机图片服务", description="模拟拍照返回图片的HTTP服务")

# 静态目录用绝对路径定位，避免不同运行环境工作目录不一致导致找不到
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.isfile(index_path):
        return {"error": "前端页面缺失"}
    return FileResponse(index_path)

@app.get("/photos")
async def get_random_photo():
    #校验图片目录是否存在
    if not os.path.exists(IMAGE_DIR):
        return {"error": "图片目录不存在"}
    #遍历目录，筛选符合格式的图片文件
    image_list = [
        file for file in os.listdir(IMAGE_DIR)
        if file.lower().endswith(tuple(ALLOWED_IMAGE_EXT))
    ]
    #校验是否有可用图片
    if not image_list:
        return {"error": "没有可用的图片"}
    #随机选择一张图片
    random_img_name = random.choice(image_list)
    img_full_path = os.path.join(IMAGE_DIR, random_img_name)
    #返回图片的完整路径
    return FileResponse(img_full_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, reload=True)