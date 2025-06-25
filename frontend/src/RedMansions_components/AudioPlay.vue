<template>
    <div class="video-play">
        <div v-if="audioList.length > 0">
            <div v-for="(audio, index) in audioList" :key="index" class="audio-item">
                <div class="audio-content">
                    <div class="audio-player">
                        <audio :src="audio.src" controls autoplay></audio>
                    </div>
                    <div class="button-group">
                        <button @click="downloadAudio(audio.filename)">下载</button>
                        <button @click="generateDlCode(audio.filename)">扫码下载</button>
                    </div>
                </div>
            </div>
        </div>
        <p v-else>暂无音频数据。</p>

        <!-- 二维码弹窗 -->
        <div v-if="showQrModal" class="qr-modal">
            <div class="qr-modal-content">
                <div class="qr-modal-header">
                    <h3>下载到手机</h3>
                    <button class="close-button" @click="showQrModal = false">&times;</button>
                </div>
                <div class="qr-modal-body">
                    <qrcode-vue :value="currentQrCodeUrl" :size="200" />
                    <p>请使用手机扫描二维码下载音频</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import QrcodeVue from 'qrcode.vue';

axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true';
const backendUrl = import.meta.env.VITE_BACKEND_URL;

export default {
    name: 'VideoPlay',
    components: {
        QrcodeVue
    },
    props: {
        audioData: {
            type: Array,
            required: false,
            default: () => []
        }
    },
    data() {
        return {
            audioList: [{src: 'blob:https://159b-59-61-85-42.ngrok-free.app/aabd265d-bfbc-4cdc-880c-00687a6590e4', filename: 'None_20250426221213.wav'}],
            showQrModal: false,
            currentQrCodeUrl: '',
        };
    },
    watch: {
        audioData(newVal) {
            if (newVal && newVal.length > 0) {
                newVal.forEach(audio => {
                    if (audio?.url) {
                        this.addAudioToList(audio);
                    }
                });
            }
        },
    },
    methods: {
        getFullUrl(relativeUrl) {
            return `${backendUrl}/${relativeUrl}`;
        },
        async addAudioToList(audio) {
            const fullUrl = this.getFullUrl(audio.url);
            try {
                const response = await axios.get(fullUrl, {
                    responseType: 'blob'
                });
                const audioSrc = URL.createObjectURL(response.data);
                this.audioList.push({
                    src: audioSrc,
                    filename: audio.filename,
                });
            } catch (error) {
                console.error('获取音频失败:', error);
            }
        },
        async downloadAudio(filename) {
            const downloadUrl = this.getFullUrl(`download/${filename}`);
            try {
                const response = await axios.get(downloadUrl, {
                    responseType: 'blob'
                });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(response.data);
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } catch (error) {
                console.error('下载音频失败:', error);
            }
        },
        async generateDlCode(filename) {
            try {
                const response = await axios.post(`${backendUrl}/generate_download_code`, { filename });
                this.currentQrCodeUrl = response.data.qrCodeUrl;
                this.showQrModal = true;
            } catch (error) {
                console.error('生成二维码失败:', error);
            }
        },
    },
};
</script>

<style scoped>
.video-play {
   
    height: 15px;
}

.audio-item {
    position: relative;
    margin-bottom: 20px;
    padding: 15px;
    background-color: rgba(255, 235, 238, 0.8);
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    height: 50px;
}

.audio-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}

.audio-player {
    flex: 1;
}

.audio-player audio {
    width: 100%;
}

.button-group {
    display: flex;
    gap: 10px;
    flex-shrink: 0;
}

.button-group button {
    padding: 8px 16px;
    background-color: white;
    color: #d32f2f;
    border: 1px solid #d32f2f;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.button-group button:hover {
    background-color: #d32f2f;
    color: white;
}

/* 二维码弹窗样式 */
.qr-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.qr-modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    max-width: 90%;
    width: 300px;
}

.qr-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.qr-modal-header h3 {
    margin: 0;
    color: #d32f2f;
}

.close-button {
    background: none;
    border: none;
    font-size: 24px;
    color: #666;
    cursor: pointer;
    padding: 0;
    line-height: 1;
}

.close-button:hover {
    color: #d32f2f;
}

.qr-modal-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.qr-modal-body p {
    color: #666;
    margin: 0;
}

/* 音频播放器样式 */
audio::-webkit-media-controls-panel {
    background-color: #ffcdd2;
}

audio::-webkit-media-controls-current-time-display,
audio::-webkit-media-controls-time-remaining-display {
    color: #d32f2f;
}

audio::-webkit-media-controls-play-button {
    background-color: #d32f2f;
    border-radius: 50%;
}

/* 隐藏更多选项按钮和相关控件 */
audio::-webkit-media-controls-overflow-button,
audio::-webkit-media-controls-toggle-closed-captions-button,
audio::-webkit-media-controls-fullscreen-button {
    display: none;
}
</style>






