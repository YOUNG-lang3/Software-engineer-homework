from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from config import ALLOWED_IMAGE_EXT, HOST, IMAGE_DIR, PORT
import os
import random

app = FastAPI(title="随机图片服务", description="模拟拍照返回图片的HTTP服务")
#挂在前端静态资源目录
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

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