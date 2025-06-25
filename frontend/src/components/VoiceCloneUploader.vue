<template>
  <div class="upload-container">
    <!-- 色斑背景 -->
    <div class="spot spot1"></div>
    <div class="spot spot2"></div>
    <div class="spot spot3"></div>
    <!-- 建议阅读文本区域 -->
    <div class="reading-suggestion">
      <div class="suggestion-title">
        <span>建议朗读文本</span>
      </div>
      <div class="poem-content">
        <p class="poem-title">《静夜思》</p>
        <p class="poem-text">床前明月光，</p>
        <p class="poem-text">疑是地上霜。</p>
        <p class="poem-text">举头望明月，</p>
        <p class="poem-text">低头思故乡。</p>
      </div>
      <div class="suggestion-tip">
        提示：请清晰地朗读上述文本，语速适中，语气自然。
      </div>
    </div>
    <!-- 操作按钮区域 -->
    <div class="action-buttons">
      <!-- 文件上传按钮 -->
      <div>
        <input type="file" id="file-input" @change="handleFileChange" accept="audio/*" />
        <label for="file-input" class="icon-button">
          <span>上传</span>
        </label>
      </div>

      <!-- 录音按钮 -->
      <button class="icon-button" :class="{ 'recording': isRecording }" @click="toggleRecording">
        <span>{{ isRecording ? '停止' : '录音' }}</span>
      </button>
    </div>

    <!-- 录音时长显示 -->
    <p v-if="isRecording" class="recording-duration">
      录音时长: {{ recordingDuration }}秒
    </p>

    <!-- 音频预览区域 -->
    <div v-if="file" class="audio-preview-container">
      <div class="audio-player">
        <audio :src="audioUrl" controls @loadedmetadata="handleAudioLoad"></audio>
        <div class="button-group">
          <button class="upload-btn" @click="submitFile" :disabled="isUploading">
            {{ isUploading ? '上传中...' : '上传音频' }}
          </button>
          <button class="delete-btn" @click="deleteFile">删除</button>
        </div>
      </div>
    </div>

    <!-- 时长提示区域 -->
    <div class="duration-section">
      <div class="duration-progress">
        <div class="progress-bar">
          <div class="progress-fill"
            :style="{ width: progressWidth + '%' }"
            :class="{ 
              'warning': audioDuration < 10 || audioDuration > 50,
              'success': audioDuration >= 10 && audioDuration <= 50 
            }">
          </div>
        </div>
        <div class="duration-marks">
          <span>0s</span>
          <span>10s</span>
          <span>30s</span>
          <span>50s</span>
        </div>

        <div class="tips">
          <p>注意：最小 10 秒，最大 30 秒，推荐 15 秒。</p>
          <p>为获得最佳效果，请确保声音清晰且没有背景噪音。</p>
        </div>
      </div>
      

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import WavEncoder from 'wav-encoder';

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export default {
  data() {
    return {
      file: null,
      uploadStatus: '',
      isRecording: false,
      audioContext: null,
      mediaStream: null,
      recordingDuration: 0,  // 添加录音时长
      recordingTimer: null,  // 添加计时器
      audioBufferChunks: [],
      audioUrl: null,
      audioDuration: 0,
      isUploading: false,
    };
  },
  computed: {
    progressWidth() {
      // 修改为最大 50 秒，并调整计算逻辑
      const maxDuration = 30;
      if (this.audioDuration <= 0) return 0;
      // 将当前时长映射到0-100的范围
      return Math.min((this.audioDuration / maxDuration) * 100, 100);
    }
  },
  methods: {
    handleFileChange(event) {
      this.resetRecording();
      this.file = event.target.files[0];
      this.audioUrl = URL.createObjectURL(this.file);
      // 创建一个临时的 audio 元素来获取音频时长
      const audio = new Audio(this.audioUrl);
      audio.addEventListener('loadedmetadata', () => {
        this.audioDuration = audio.duration;
      });
    },

    async submitFile() {
      if (!this.file) {
        alert('请先选择或录制一个音频文件');
        return;
      }
    
      if (this.audioDuration < 10 || this.audioDuration > 30) {
        alert('音频时长需要在10-30秒之间');
        return;
      }
    
      this.isUploading = true;
    
      try {
        const uploadId = window.location.pathname.split('/').pop();
        if (!uploadId) {
          throw new Error('无效的 upload_id');
        }
      
        const formData = new FormData();
        formData.append('audio', this.file);
        formData.append('upload_id', uploadId);
      
        const response = await axios.post(`${backendUrl}/upload_audio/${uploadId}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'ngrok-skip-browser-warning': 'true',
          },
        });
      
        if (response.data.success) {
          this.uploadStatus = 'success';
          alert('上传成功');
        } else {
          throw new Error(response.data.message || '上传失败');
        }
      } catch (error) {
        console.error('上传失败:', error);
        alert('上传失败: ' + (error.message || '请检查网络连接'));
        this.uploadStatus = 'error';
      } finally {
        this.isUploading = false;
      }
    },

    async toggleRecording() {
      if (this.isRecording) {
        this.stopRecording();
      } else {
        this.resetRecording(); // 清除旧内容
        await this.startRecording();
      }
    },

    async startRecording() {
      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = this.audioContext.createMediaStreamSource(this.mediaStream);
        this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
        
        this.processor.onaudioprocess = (e) => {
          const input = e.inputBuffer.getChannelData(0);
          this.audioBufferChunks.push(new Float32Array(input));
        };

        source.connect(this.processor);
        this.processor.connect(this.audioContext.destination);

        this.isRecording = true;
        this.recordingDuration = 0;
        
        // 开始计时
        this.recordingTimer = setInterval(() => {
          this.recordingDuration++;
        }, 1000);
      } catch (err) {
        console.error('麦克风权限错误', err);
        alert('无法访问麦克风，请检查权限设置');
      }
    },

    async stopRecording() {
      this.processor.disconnect();
      this.mediaStream.getTracks().forEach((track) => track.stop());
      
      // 停止计时
      clearInterval(this.recordingTimer);
      this.isRecording = false;

      // 合并音频数据
      const length = this.audioBufferChunks.reduce((sum, chunk) => sum + chunk.length, 0);
      const mergedBuffer = new Float32Array(length);
      let offset = 0;
      for (const chunk of this.audioBufferChunks) {
        mergedBuffer.set(chunk, offset);
        offset += chunk.length;
      }

      const wavBuffer = await WavEncoder.encode({
        sampleRate: this.audioContext.sampleRate,
        channelData: [mergedBuffer],
      });

      const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });
      this.file = new File([wavBlob], 'recorded_audio.wav', { type: 'audio/wav' });
      this.audioUrl = URL.createObjectURL(this.file);

      alert('录音完成，已转换为 WAV');
      const audio = new Audio(this.audioUrl);
      audio.addEventListener('loadedmetadata', () => {
        this.audioDuration = audio.duration;
      });
    },

    deleteFile() {
      if (confirm('确定要删除当前文件吗？')) {
        // 释放之前创建的 URL
        if (this.audioUrl) {
          URL.revokeObjectURL(this.audioUrl);
        }

        // 重置所有相关状态
        this.file = null;
        this.audioUrl = null;
        this.audioDuration = 0;
        this.uploadStatus = '';

        // 清空文件输入框
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
          fileInput.value = '';
        }
      }
    },

    resetRecording() {
      if (this.audioUrl) URL.revokeObjectURL(this.audioUrl);
      this.file = null;
      this.audioUrl = null;
      this.audioBufferChunks = [];
      this.recordingDuration = 0;
      clearInterval(this.recordingTimer);
      if (this.isRecording) this.stopRecording();
    },
  },
};
</script>

<style scoped>

.reading-suggestion {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 20px;
  margin: 20px auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.suggestion-title {
  color: #d32f2f;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
}

.poem-content {
  background: rgba(255, 255, 255, 0.5);
  padding: 15px;
  border-radius: 8px;
  margin: 10px 0;
}

.poem-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.poem-text {
  font-size: 16px;
  line-height: 2;
  color: #444;
  margin: 5px 0;
}

.suggestion-tip {
  font-size: 14px;
  color: #666;
  margin-top: 15px;
  font-style: italic;
}
.upload-container {
  position: relative;
  min-height: 100vh;
  padding: 20px;
  background: #f0eded;
  overflow: hidden;
}

/* 色斑样式 */
.spot {
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #d32f2f, #ee9b9b, #f0eded);
  border-radius: 50%;
  opacity: 0.6;
  filter: blur(50px);
  z-index: 1;
  animation: float 10s ease-in-out infinite alternate;
}

.spot1 { top: 5%; left: -10%; }
.spot2 { top: 40%; right: -10%; }
.spot3 { bottom: 5%; left: 20%; }

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -20px) scale(1.1); }
  100% { transform: translate(-20px, 30px) scale(1); }
}

/* 按钮区域样式 */
.action-buttons {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: center;
  gap: 30px; /* 增加按钮间距 */
  margin: 30px 0;
}

.icon-button {
  width: 80px;  /* 增加按钮尺寸 */
  height: 80px; /* 增加按钮尺寸 */
  border-radius: 50%;
  background: white;
  color: #d32f2f;
  border: 2px solid #d32f2f;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold; /* 加粗文字 */
}

.icon-button span {
  font-size: 16px; /* 增加文字大小 */
  margin-top: 4px;
}

/* 隐藏原始文件输入 */
#file-input {
  display: none;
}

/* 录音时长显示 */
.recording-duration {
  text-align: center;
  color: #d32f2f;
  font-weight: bold;
  margin: 10px 0;
}

/* 音频预览容器 */
.audio-preview-container {
  position: relative;
  z-index: 2;
  margin: 20px auto;
  padding: 15px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 100%;
}

.audio-player {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.audio-player audio {
  width: 100%;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.upload-btn {
  padding: 8px 16px;
  background: #d32f2f;
  color: white;
  border: 1px solid #d32f2f;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-btn:hover {
  background: #b71c1c;
}

.upload-btn:disabled {
  background: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}

.delete-btn {
  align-self: flex-end;
  padding: 8px 16px;
  background: white;
  color: #ff4444;
  border: 1px solid #ff4444;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background: #ff4444;
  color: white;
}

/* 时长提示区域 */
.duration-section {
  position: relative;
  z-index: 2;
  margin-top: auto;
}

.duration-progress {
  background: rgba(255, 255, 255, 0.3);
  padding: 20px 20px 5px 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 0; /* 移除底部边距 */
}

.tips {
  background: rgba(255, 255, 255, 0); /* 修改背景色 */
  margin-top: 30px;
  font-size: 14px;
  color: #666;
  line-height: 1;
}

/* 进度条样式保持不变 */
.progress-bar {
  width: 100%;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.progress-fill.success {
  background: #4CAF50;
}

.progress-fill.warning {
  background: #ff4444;
}

.duration-marks {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 12px;
  color: #666;
}



/* 移动端适配 */
@media (max-width: 768px) {
  .upload-container {
    padding: 15px;
  }
  
  .icon-button {
    width: 100px;
    height: 100px;
  }
  
  .duration-section {
    padding: 15px;
  }
    .reading-suggestion {
    padding: 15px;
    margin: 15px auto;
  }
  
  .poem-text {
    font-size: 15px;
    line-height: 1.8;
  }
}

</style>
