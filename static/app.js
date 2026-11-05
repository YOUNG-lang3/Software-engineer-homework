// 获取页面元素
const centralBox = document.querySelector('.central-box');
const startBtn = document.querySelector('.start-button');

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

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.msg || '请求失败');
            }

            // 请求成功，这里只打印结果，不渲染图片到页面
            console.log('随机图片请求发送成功');
            console.log('响应状态：', response.status);

        } catch (error) {
            console.error('请求出错：', error.message);
        }
    }, 2000);
});
