// 获取页面元素
const centralBox = document.querySelector('.central-box');
const startBtn = document.querySelector('.start-button');
const photo = document.querySelector('.photo');

// 状态锁：防止连续重复点击触发多次请求
let isRequesting = false;

// 绑定开始按钮点击事件
startBtn.addEventListener('click', () => {
    if (isRequesting) return;
    isRequesting = true;

    // 1. 触发卡片交换动画
    centralBox.classList.add('swapped');

    // 2. 等待 2 秒后，自动发送随机图片请求
    setTimeout(async () => {
        try {
            // 发送请求，加时间戳防止浏览器缓存
            const response = await fetch(`/photos?t=${Date.now()}`);

            // 后端异常时可能返回 200 + JSON 错误体，先按响应头判断是不是图片
            const contentType = response.headers.get('content-type') || '';
            if (!response.ok || !contentType.startsWith('image/')) {
                const err = await response.json();
                throw new Error(err.error || err.msg || '后端未返回图片文件');
            }

            // 关键：把响应体读成二进制文件对象（Blob），这才是真正拿到图片文件
            const photoBlob = await response.blob();
            console.log('随机图片请求成功，已拿到图片文件');
            console.log('响应状态：', response.status);
            console.log('文件类型：', photoBlob.type);
            console.log('文件大小：', photoBlob.size, 'bytes');

            // 3. 把图片文件交给卡片显示：整张卡片铺满
            photo.src = URL.createObjectURL(photoBlob);
            photo.classList.add('show');

            // 图片出现后，Waiting 和三个点同步淡出，避免和图片叠在一起
            const waitingEl = document.querySelector('.waiting');
            waitingEl.style.transition = 'opacity 0.4s ease';
            waitingEl.style.opacity = '0';
            document.querySelectorAll('.dots i').forEach((dot) => {
                dot.style.animation = 'none';
                dot.style.transition = 'opacity 0.3s ease';
                dot.style.opacity = '0';
            });

        } catch (error) {
            console.error('请求出错：', error.message);
        }
    }, 2000);
});
