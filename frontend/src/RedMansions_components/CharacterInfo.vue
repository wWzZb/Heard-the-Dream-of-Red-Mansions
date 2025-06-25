
<template>
    <div class="character-container">
        <div v-for="character in characters" 
             :key="character.id"
             class="bookmark-wrapper"
             :class="{ 'selected': selectedCharacter === character.id }"
             @click="selectCharacter(character)">
            
            <!-- 头像区域 -->
            <div class="portrait-section">
                <img :src="character.image" :alt="character.name" class="character-image"/>
                <div class="image-overlay"></div>
            </div>
            
            <!-- 描述区域 -->
            <div class="description-section">
                <div class="title-section">
                    <h3 class="character-name">{{ character.name }}</h3>
                </div>
                <div class="desc-section">
                    <p class="character-desc">{{ character.description }}</p>
                </div>
            </div>
            
            <!-- 试听按钮 -->
            <div class="audio-section">
                <button class="preview-button" @click="handlePlayAudio(character.audioUrl)">
                    试听音色
                </button>
            </div>
        </div>
    </div>
</template>

<script>

import axios from 'axios'
import daiyu from '@/assets/daiyu.png'
import baochai from '@/assets/薛宝钗.png'
import baoyu from '@/assets/贾宝玉.png'
import xifeng from '@/assets/王熙凤.png'

axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true'
const backendUrl = import.meta.env.VITE_BACKEND_URL // 从环境变量中读取后端地址
export default {
    name: 'CharacterInfo',

    data() {
        return {
            selectedCharacter: null,
            characters: [
                {
                    id: 4,
                    name: '林黛玉',
                    image: daiyu,
                    description: '金陵十二钗正册双首之一，西方灵河岸上三生石畔的绛珠仙草，地上临潇湘馆。',
                    audioUrl: `${backendUrl}/asset/daiyu.wav` // 拼接后端资源路径
                },
                {
                    id: 5,
                    name: '薛宝钗',
                    image: baochai,
                    description: '金陵十二钗正册双首之二，蒙祖母含养，父母疼爱，针线纺织，女工精巧。',
                    audioUrl: `${backendUrl}/asset/baochai.wav`
                },
                {
                    id: 6,
                    name: '贾宝玉',
                    image: baoyu,
                    description: '金陵十二钗正册之主，通灵宝玉所生，亲慕儿女，厌恶功名，钟情红颜',
                    audioUrl: `${backendUrl}/asset/baoyu.wav`
                },
                {
                    id: 7,
                    name: '王熙凤',
                    image: xifeng,
                    description: '金陵十二钗副册之首，贾府内外总管，机敏泼辣，才干卓绝，权谋过人。',
                    audioUrl: `${backendUrl}/asset/xifeng.wav`
                }
            ],
        }
    },
    methods: {
        selectCharacter(character) {
            this.selectedCharacter = character.id
            // 向父组件发送选中的音色值
            this.$emit('character-selected', character.id)
        },
        async handlePlayAudio(audioUrl) {
        try {
            // 使用 axios 发起 GET 请求，获取音频文件
            const response = await axios.get(audioUrl, {
              responseType: 'blob', // 确保返回的是二进制数据
            })

            // 将返回的 Blob 数据转换为音频 URL
            const audioBlob = new Blob([response.data], { type: 'audio/wav' })
            const audioObjectUrl = URL.createObjectURL(audioBlob)

            // 创建音频对象并播放
            const audio = new Audio(audioObjectUrl)
            await audio.play()

            console.log(`正在播放音频: ${audioUrl}`)
            } catch (error) {
            console.error('音频播放失败:', error)
            alert('音频播放失败，请检查网络连接或后端服务。')
            }
        }
    },
}
</script>

<style scoped>
.character-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 200px; /* 增加间距 */
    
    height: 100%;
}

/* 修改书签样式 */
.bookmark-wrapper {
    flex: 1;
    width: 210px; /* 限制最大宽度 */
    height: 350px; /* 增加最小高度 */
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #fff5f5 0%, #ffe4e1 100%);
    border-radius: 16px 16px ;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    
    &::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-top: 15px solid #ffe4e1;
    }
}

.bookmark-wrapper.selected {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(211, 47, 47, 0.3);
    border: 2px solid #d32f2f;
    
    &::after {
        border-top-color: #d32f2f;
    }
}

/* 调整头像区域高度 */
.portrait-section {
    height: 180px; /* 增加高度 */
    position: relative;
    overflow: hidden;
    margin-bottom: -30px;
    z-index: 1; /* 确保在最底层 */
}


.character-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.image-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 90px;
    background: linear-gradient(to bottom, transparent, #ffe4e1);
}

.description-section {
    padding: 15px;
    height: 180px; /* 增加高度以适应竖排文字 */
    width: 85%;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 15px;
    border-radius: 12px;
    z-index: 2;
    position: relative; /* 确保可以使用定位 */
    margin-bottom: -30px; /* 向下移动 */
}

.title-section {
    height: 60%;
    padding-right: 10px; /* 添加右侧间距 */
    border-right: 2px solid rgba(211, 47, 47, 0.2); /* 改为右侧边框 */
    display: flex;
    align-items: center;
}

.character-name {
    writing-mode: vertical-rl; /* 设置竖排 */
    text-orientation: upright;
    font-size: 20px;
    color: #d32f2f;
    font-weight: bold;
    margin: 0;
    letter-spacing: 4px; /* 增加字间距 */
}
.character-desc {
    margin: 0px;
}
.desc-section {
    flex: 1;
    width: 20%;
    height: 80%;
    writing-mode: vertical-lr;
    text-orientation: unset;
    justify-content: center;
    align-self: center;
    font-size: 14px;
    color: #666;
    line-height: 1.8;
    margin: 0px;
    letter-spacing: 2px;
}


.character-name {
    font-size: 20px;
    color: #d32f2f;
    font-weight: bold; /* 加粗突出名字 */
}



.audio-section {
    padding: 15px;
    display: flex;
    justify-content: center;
}

.preview-button {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(255, 65, 108, 0.4);
    }
}
</style>