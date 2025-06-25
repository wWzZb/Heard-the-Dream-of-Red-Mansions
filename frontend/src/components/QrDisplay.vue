<template>
    <div class="qr-display">
      <div class="image-container">
        <img src="@/assets/hhh.jpg" alt="AI Image" class="image" />
      </div>
      <div class="text-container">
        <h1>世界很大，AI无限</h1>
        <p>了解人工智能创作坊最新资讯。</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "QrDisplay",
  };
  </script>
  
  <style scoped>
  .qr-display {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px;  /* 减小内边距 */
    max-width: 600px;  /* 限制最大宽度 */
    height: 40px;
    margin: 0 auto;  /* 居中显示 */
    background-color: transparent;  /* 透明背景 */
  }
  
  .image-container {
    flex: 1;

    text-align: center;
    overflow: hidden;  /* 控制图片缩放不超出容器 */
  }
  
  .image {
    max-width: 90%;  /* 减小图片最大宽度 */
    height: auto;
    border: 3px solid #ddd;  /* 减小边框宽度 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* 减淡阴影 */
    transition: transform 0.3s ease;  /* 添加过渡效果 */
  }
  
  .image:hover {
    transform: scale(1.1);  /* 鼠标悬停时放大1.1倍 */
  }
  
  .text-container {
    flex: 4;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 15px;  /* 减小内边距 */
    color: #333;
  }
  
  .text-container h1 {
    font-size: 1.6em;  /* 减小标题字体 */
    margin-bottom: 8px;
  }
  
  .text-container p {
    font-size: 1em;  /* 减小正文字体 */
  }
  </style>