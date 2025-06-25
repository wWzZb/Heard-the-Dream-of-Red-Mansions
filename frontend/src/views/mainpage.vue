<template>
    <div class="main-page">
        <!-- 色斑们，必须放在 main-page 里面，跟内容同级 -->
        <div class="spot spot1"></div>
        <div class="spot spot2"></div>
        <div class="spot spot3"></div>
        <div class="spot spot4"></div>
        <div class="spot spot5"></div>

        <!-- 头部 -->
        <header class="header">
            <h1>在线语音生成器<br/>生成逼真的 AI 语音</h1>
            <p style="font-size: smaller; color: black;">使用我们强大的 AI 语音生成器，2分钟内即可创建逼真的语音和即时语音克隆。使用您最喜欢的语音和音色。现在就试试吧！</p>
        </header>

        <!-- 内容 -->
        <main class="content">
            <div class="form-section">
                <CloneForm @audioGenerated="handleAudioGenerated" />
            </div>
            <div class="video-section">
                <VideoPlay :audioData="audioData" />
            </div>
        </main>

        <!-- 底部 -->
        <footer class="footer">
            <p>© 2025 由 人工智能创作坊 驱动.</p>
        </footer>
    </div>
</template>

<script>
import CloneForm from '@/components/CloneFrom.vue';
import VideoPlay from '@/components/VideoPlay.vue';

export default {
    name: 'MainPage',
    components: {
        CloneForm,
        VideoPlay,
    },
    data() {
        return {
            audioData: null,
        };
    },
    methods: {
        handleAudioGenerated(audio_infos) {
            if (audio_infos && audio_infos.length > 0) {
                this.audioData = audio_infos; 
            }
        },
    },
};
</script>

<style scoped>
/* 整体布局 */
.main-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100vw;
    margin: 0;
    padding: 0;
    overflow: hidden;
    box-sizing: border-box;
    position: relative;
    background: #f0eded;
}

/* 色斑 */
.spot {
    position: absolute;
    width: 600px;
    height: 500px;
    background: radial-gradient(circle, #d32f2f, #ee9b9b, #f0eded);
    border-radius: 50%;
    opacity: 0.6;
    filter: blur(50px);
    z-index: 1; /* 色斑在最底层 */
    animation: float 10s ease-in-out infinite alternate;
}

/* 色斑位置 */
.spot1 { top: 8%; left: 12%; }
.spot2 { top: 10%; left: 65%; }
.spot3 { top: 58%; left: 22%; }
.spot4 { top: 82%; left: 75%; }
.spot5 { top: 68%; left: 5%; }
@keyframes float {
    0% {
        transform: translate(0px, 0px) scale(1) rotate(0deg);
    }
    50% {
        transform: translate(80px, -60px) scale(1.1) rotate(15deg);
    }
    100% {
        transform: translate(-60px, 80px) scale(1) rotate(0deg);
    }
}


/* 头部样式 */
.header {
    position: relative;
    z-index: 2; /* 让内容在色斑上方 */
    background-color: rgba(255, 255, 255, 0);
    color: #333;
    
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    flex-shrink: 0;
    
}

/* 标题样式：红色动态渐变 */
.header h1 {
    font-size: 39px; /* 标题更大 */
    font-weight: bold;
    background: linear-gradient(
        90deg,
        #ff4b2b,
        #ff416c,
        #1fddff,
        #24fe41
    ); /* 多彩渐变 */
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    text-align: center;
    margin: 0;
}


/* 段落文字样式：灰色 */
.header p {
    font-size: small;
    color: gray; /* 设置文字为灰色 */
    margin-bottom: 20px;
}
/* 内容区域样式 */
.content {
    position: relative;
    z-index: 2;
    flex: 1;
    display: flex;
    flex-direction: row;
    gap: 10px;
    background-color: rgba(255, 255, 255, 0);
    overflow: hidden;
    padding: 10px;
    border-radius: 8px;
}

/* 表单区域样式 */
.form-section {
    flex: 2;
    background-color: rgba(255, 255, 255, 0.6);
    padding: 10px;
    border-radius: 30px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow-y: auto;
    max-height: 100%;
    scrollbar-gutter: stable; /* 保持滚动条空间稳定 */
    
    /* 美化滚动条 */
    &::-webkit-scrollbar {
        width: 8px;     /* 滚动条宽度更细 */
        
    }

    &::-webkit-scrollbar-track {
        background: rgba(255, 235, 238, 0.9); /* 更浅更淡的红色背景 */
        border-radius: 4px;
        margin: 20px 0; /* <<< 重点！轨道缩短！ */
    }

    &::-webkit-scrollbar-thumb {
        background-color: rgba(244, 67, 54, 0.7); /* 淡红色且带点透明 */
        border-radius: 4px;
    }

    &::-webkit-scrollbar-thumb:hover {
        background-color: rgba(244, 67, 54, 1); /* 鼠标悬停时变成稍深的红色 */
    }
}

/* 视频播放区域样式 */
.video-section {
    flex: 1;
    background-color: rgba(255, 255, 255, 0.6);
    padding: 10px;
    border-radius: 30px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    overflow-y: auto;
    max-height: 100%;
    scrollbar-gutter: stable; /* 保持滚动条空间稳定 */
    
    /* 美化滚动条 */
    &::-webkit-scrollbar {
        width: 8px;     /* 滚动条宽度更细 */
        
    }

    &::-webkit-scrollbar-track {
        background: rgba(255, 235, 238, 0.9); /* 更浅更淡的红色背景 */
        border-radius: 4px;
        margin: 20px 0; /* <<< 重点！轨道缩短！ */
    }

    &::-webkit-scrollbar-thumb {
        background-color: rgba(244, 67, 54, 0.7); /* 淡红色且带点透明 */
        border-radius: 4px;
    }

    &::-webkit-scrollbar-thumb:hover {
        background-color: rgba(244, 67, 54, 1); /* 鼠标悬停时变成稍深的红色 */
    }
}

/* 底部样式 */
.footer {
    position: relative;
    z-index: 2;
    background-color: rgba(255, 255, 255, 0);
    color: #333;
    text-align: center;
    padding: 5px;
    font-size: 12px;
    flex-shrink: 0;
}
</style>
