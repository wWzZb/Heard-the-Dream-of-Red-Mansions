<template>
    <link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&display=swap" rel="stylesheet">

    <div class="main-page">
        <!-- 色斑们，必须放在 main-page 里面，跟内容同级 -->
        <div class="spot spot1"></div>
        <div class="spot spot2"></div>
        <div class="spot spot3"></div>
        <div class="spot spot4"></div>
        <div class="spot spot5"></div>

        <!-- 头部 -->
        <header class="header">
            <h1>听见</h1>
            <span class="dot">·</span>
            <p>红楼梦</p>
        
        </header>
            <!-- 移动端提示遮罩 -->
        <div v-if="isMobile" class="mobile-mask">
            <div class="mobile-alert">
                <h2>请使用电脑访问</h2>
                <p>为了获得最佳体验，请使用电脑端浏览器访问本网站。</p>
            </div>
        </div>
        <!-- 内容 -->
        <main v-else class="content">
            <div class="character-section">
                <CharacterInfo @character-selected="handleCharacterSelected" />
            </div>
            <div class="form-section">
                <CloneForm 
                    :selectedVoice="selectedVoice"
                    @audioGenerated="handleAudioGenerated" 
                />
            </div>
            <div class="player-section">
                <AudioPlay :audioData="audioData" />
            </div>
        </main>
    </div>
</template>

<script>

import CharacterInfo from '@/RedMansions_components/CharacterInfo.vue'
import CloneForm from '@/RedMansions_components/CloneForm.vue'
import AudioPlay from '@/RedMansions_components/AudioPlay.vue'

export default {
    name: 'RedMansions',
    components: {
        CharacterInfo,
        CloneForm,
        AudioPlay
    },
    data() {
        return {
            selectedVoice: '1',
            audioData: null,
            isMobile: false
        }
    },
    created() {
        this.checkDevice()
        // 监听窗口大小变化
        window.addEventListener('resize', this.checkDevice)
    },
    beforeUnmount() {
        // 清理事件监听
        window.removeEventListener('resize', this.checkDevice)
    },
    methods: {
        handleCharacterSelected(value) {
            this.selectedVoice = value
        },
        handleAudioGenerated(audioInfos) {
            this.audioData = audioInfos
        },
        checkDevice() {
            // 检测是否为移动设备
            this.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) 
                || window.innerWidth <= 768
        }
    }

}
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
    
    
    margin: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    
}

/* 标题样式：红色动态渐变 */
.header h1 {
    font-size: 26px; /* 标题更大 */
    text-align: center;
    color: #8B0000; /* 深红，更古典 */
    font-family: 'Ma Shan Zheng', cursive;
    margin: 0;
    
}


/* 段落文字样式：灰色 */
.header p {
    font-size: 32px;
    color: #8B0000; /* 深红，更古典 */
    font-weight: bold;
    text-align: center;
    font-family: 'Ma Shan Zheng', cursive;
    margin: 0;

}

.dot {
    font-size: 25px;
    color: #8B0000;
    
    margin: 0;  /* 调整左右间距 */
    font-family: 'Ma Shan Zheng', cursive;
}
/* 内容区域样式 */
.content {
    position: relative;
    z-index: 2;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 0px 20px 20px 20px;
    overflow: hidden;
}

.character-section {
    flex: 4; /* 占据1/2空间 */
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    overflow: hidden; /* 修改为 hidden，防止内容溢出 */
    display: flex; /* 添加弹性布局 */
    align-items: center; /* 垂直居中 */
    justify-content: space-around;
}

/* 表单区域样式 */
.form-section {
    flex: 3; /* 占据1/4空间 */
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    overflow: hidden; /* 修改为 hidden，防止滚动 */
    display: flex; /* 添加弹性布局 */
    align-items: center; /* 垂直居中 */
}
    


.player-section {
    overflow-y: auto;
    scrollbar-gutter: stable;
    flex: 1;
    width: 100%;
    height: 100%;

    
    &::-webkit-scrollbar {
        width: 8px;
    }

    &::-webkit-scrollbar-track {
        background: rgba(255, 235, 238, 0.9);
        border-radius: 4px;
        margin: 20px 0;
    }

    &::-webkit-scrollbar-thumb {
        background-color: rgba(244, 67, 54, 0.7);
        border-radius: 4px;
    }

    &::-webkit-scrollbar-thumb:hover {
        background-color: rgba(244, 67, 54, 1);
    }
}

/* 移动端遮罩样式 */
.mobile-mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #d32f2f, #ee9b9b);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

.mobile-alert {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    max-width: 80%;
}

.mobile-alert h2 {
    color: #d32f2f;
    font-family: 'Ma Shan Zheng', cursive;
    font-size: 24px;
    margin-bottom: 15px;
}

.mobile-alert p {
    color: #666;
    font-size: 16px;
    line-height: 1.6;
}

/* .qr-section {
    flex: 1; 
    background-color: rgba(255, 255, 255, 0.6);
    padding: 10px;
    border-radius: 30px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
} */

</style>
