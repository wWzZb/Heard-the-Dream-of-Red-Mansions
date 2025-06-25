<template>
  <form class="input-form" @submit.prevent="handleSubmit">
    <!-- 提示语输入 -->
    <label>提示语：</label>
    <div class="button-group">
      <p style="font-size: smaller">请尝试以下示例:</p>
      <button type="button" @click="addPromptText('使用粤语')">使用粤语</button>
      <button type="button" @click="addPromptText('使用四川话')">使用四川话</button>
      <button type="button" @click="addPromptText('使用难过的语气')">使用难过的语气</button>
      <button type="button" @click="addPromptText('使用兴奋的语气')">使用兴奋的语气</button>
    </div>
    <div class="input-with-buttons">
      <input type="text" v-model="promptText" placeholder="例如：使用粤语说这句话" required />
    </div>

    <!-- 生成文本输入 -->
    <label>生成文本：</label>
    <div class="button-group">
      <p style="font-size: smaller">请尝试以下示例:</p>
      <button
        type="button"
        @click="
          addText(
            '优雅与创新相得益彰。体验一款融合了风格和功能的产品，旨在提升您的生活方式。立即探索卓越。',
          )
        "
      >
        广告
      </button>
      <button
        type="button"
        @click="
          addText(
            '嘿，感谢您的收听。您即将听到一些特别的东西 - 引起共鸣的故事、鼓舞人心的见解以及您永远不会忘记的声音。',
          )
        "
      >
        播客
      </button>
      <button
        type="button"
        @click="
          addText(
            '几个世纪以来，这片土地见证了历史的展开——关于韧性、进步和变化的故事。加入我们，揭开塑造我们世界的不为人知的故事。',
          )
        "
    >
        配音
      </button>
    </div>
    <div class="input-with-buttons">
      <textarea v-model="text" placeholder="请输入你想让 AI 说的话..." @input="handleTextInput"></textarea>
    </div>

    <!-- 音色选择 -->
    <div class="voice-type-selector">
      <button
        type="button"
        class="voice-option"
        :class="{ selected: voiceType === 'preset' }"
        @click="voiceType = 'preset'"
        :disabled="isSubmitting"
      >
        使用预设音色
      </button>
      <button
        type="button"
        class="voice-option"
        :class="{ selected: voiceType === 'custom' }"
        @click="voiceType = 'custom'; onCustomVoiceSelected()"
        :disabled="isSubmitting"
      >
        使用自定义音色
      </button>
    </div>

    <!-- 预设音色选择 -->
    <div v-if="voiceType === 'preset'" class="voice-options">
      <div class="voice-item">
        <label><input type="radio" value="1" v-model="selectedVoice" /> <img src="D:\CosyVoice\frontend\src\assets\5179de2a-d326-4559-bbbe-19fc62664af0.png" alt="甜美女声" class="voice-icon" /><p>小蓝猫</p></label>
        <button type="button" @click="playAudio('yuebanmao.wav')">试听</button>
      </div>
      <div class="voice-item">
        <label><input type="radio" value="2" v-model="selectedVoice" /> <img src="D:\CosyVoice\frontend\src\assets\trump.png" alt="等待添加" class="voice-icon" /><p>特朗普</p></label>
        <button type="button" @click="playAudio('trump.wav')">试听</button>
      </div>
      <div class="voice-item">
        <label><input type="radio" value="3" v-model="selectedVoice" /> <img src="D:\CosyVoice\frontend\src\assets\gril.png" alt="等待添加" class="voice-icon" /><p>小女孩</p></label>
        <button type="button" @click="playAudio('xiaojiejie.wav')">试听</button>
      </div>
    </div>

    <!-- 自定义音色二维码 -->
    <div v-if="voiceType === 'custom'" class="qr-section">
      <p>请使用手机扫描二维码上传音色文件：</p>
      <qrcode-vue :value="qrCodeUrl" :size="200" />
      <p>链接：{{ qrCodeUrl }}</p>
      <p v-if="uploadStatus === 'waiting'">等待上传...</p>
      <p v-if="uploadStatus === 'success'">音频上传成功！</p>
      <p v-if="uploadStatus === 'timeout'">二维码已过期，请重新生成。</p>
    </div>

    <!-- 提交按钮 -->
    <div class="submit-section">
      <button type="submit" class="qr-button" :disabled="isSubmitting">
        <span v-if="isSubmitting" class="loading-spinner"></span>
        {{ isSubmitting ? '生成中...' : voiceType === 'preset' ? '开始生成' : '生成音频' }}
      </button>
      <div v-if="isSubmitting" class="generation-timer">
        <span>已生成 {{ generationTime }} 秒</span>
        <span class="timer-tip">生成时间大约为60秒</span>
      </div>
    </div>
  </form>
</template>

<script>
import axios from 'axios'
import QrcodeVue from 'qrcode.vue'
axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true'
const backendUrl = import.meta.env.VITE_BACKEND_URL // 从环境变量中读取后端地址

export default {
  components: {
    QrcodeVue, // ✅ 注册组件！
  },
  data() {
    return {
      promptText: '',
      text: '欢迎来到人工智能创作基地',
      selectedVoice: '1',
      voiceType: 'preset',
      customAudioFile: null, // 用于存储上传的音频文件路径
      qrCodeUrl: '', // 二维码 URL
      uploadStatus: '', 
      isSubmitting: false, // 是否正在提交
      pollTimeout: 80000, // 轮询超时时间（60秒）
      pollInterval: null, // 轮询定时器
      generationTimer: null,
      generationTime: 0,
    }
  },
  methods: {
    addPromptText(text) {
      this.promptText = text
    },
    addText(text) {
      this.text = text
    },
    handleTextInput(event) {
    // 这里可以添加文本输入的验证逻辑
      const value = event.target.value;
      this.text = value;
    },
    async playAudio(filename) {
      const audioUrl = `${backendUrl}/asset/${filename}` // 拼接后端资源路径
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
    },
    async onCustomVoiceSelected() {
      // 点击“自定义音色”时重新生成二维码
      this.uploadStatus = ''
      clearInterval(this.pollInterval) // 清除之前的轮询
      await this.generateQrCode()
    },
    async generateQrCode() {
      try {
        const response = await axios.get(`${backendUrl}/generate_upload_url`)
        console.log('生成的二维码 URL:', response.data.upload_url) // 调试输出
        this.qrCodeUrl = response.data.upload_url
        this.uploadStatus = 'waiting'
        this.startPolling(response.data.upload_id)
      } catch (error) {
        console.error('生成二维码失败:', error)
      }
    },
    startPolling(uploadId) {
      const startTime = Date.now()
      this.pollInterval = setInterval(async () => {
        try {
          const response = await axios.get(`${backendUrl}/upload_status/${uploadId}`)
          if (response.data.status === 'success') {
            clearInterval(this.pollInterval)
            this.uploadStatus = 'success'
            this.customAudioFile = response.data.file_path // 保存上传的文件路径
          } else if (Date.now() - startTime > this.pollTimeout) {
            clearInterval(this.pollInterval)
            this.uploadStatus = 'timeout' // 超时处理
          }
        } catch (error) {
          console.error('轮询上传状态失败:', error)
        }
      }, 3000) // 每 3 秒检查一次
    },
    async handleSubmit() {
      if (this.isSubmitting) return // 防止重复提交
      this.isSubmitting = true
      this.generationTime = 0
      this.generationTimer = setInterval(() => {
        this.generationTime++
      }, 1000)
      const formData = new FormData()
      formData.append('text', this.text)
      formData.append('prompt_text', this.promptText)

      if (this.voiceType === 'preset') {
        formData.append('voice_id', this.selectedVoice)
      } else if (this.voiceType === 'custom') {
        if (!this.customAudioFile) {
          alert('请先通过二维码上传音频文件')
          this.isSubmitting = false
          return
        }
        formData.append('audio', this.customAudioFile)
      }

      try {
        const response = await axios.post(`${backendUrl}/voice_clone`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: 120000  // 设置2分钟超时
        })

        if (response.data.success) {
          this.$emit('audioGenerated', response.data.audio_infos) // 触发事件，传递音频 URL
        } else {
          alert('生成失败，请检查输入')
        }
      } catch (error) {
        if (error.code === 'ECONNABORTED') {
        console.error('请求超时');
        alert('生成请求超时，请重试');
        }else{console.error('生成失败:', error);
          alert('生成失败，请重试');
        }
        
        
      } finally {
        clearInterval(this.generationTimer)
        this.generationTimer = null
        this.generationTime = 0
        this.isSubmitting = false
      }
    },
  },
}
</script>

<style scoped>
.input-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: rgba(255, 255, 255, 0); /* 设置半透明背景 */
  padding: 20px; /* 添加内边距 */
  border-radius: 8px; /* 添加圆角 */

}

.input-with-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.button-group {
  display: flex;
  gap: 8px;
  height: 30px;
  align-items: center;
}

/* 按钮样式 */
.button-group button {
  background-color: white; /* 默认背景为白色 */
  color: #d32f2f; /* 默认字体为红色 */
  border: 1px solid #d32f2f;
  padding: 5px 15px; /* 减小按钮大小 */
  border-radius: 6px; /* 减小圆角 */
  font-size: 12px; /* 减小字体大小 */
  cursor: pointer;
  transition:
  background-color 0.3s ease,
  color 0.3s ease; /* 添加过渡效果 */
}

.button-group button:hover {
  background-color: #f8d7da; /* 鼠标悬停时背景变为淡红色 */
  color: black; /* 鼠标悬停时字体变为黑色 */
}

.voice-type-selector {
  display: flex;  /* 水平排列 */

  margin: 10px 0; /* 上下外边距 */
  background-color: #fff0f0;
  padding: 5px 3px;
  border-radius: 8px;
}

.voice-type-selector .voice-option {
  flex: 1;        /* 按钮等宽分布 */
  padding: 12px 24px;
  background-color: #fff0f0;  /* 默认背景色为白色 */
  color: #d32f2f;          /* 默认字体颜色为红色 */
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.voice-type-selector .voice-option.selected {
  background-color: #d32f2f; /* 选中状态背景色为红色 */
  color: white;             /* 选中状态字体颜色为白色 */
}

.voice-type-selector .voice-option:hover {
  background-color: #ffebee; /* 悬停时的背景色为浅红色 */
}

.voice-type-selector .voice-option.selected:hover {
  background-color: #ce4646; /* 选中状态背景色为红色 */
  color: white;             /* 选中状态字体颜色为白色 */
}

.voice-type-selector .voice-option:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
  border-color: #cccccc;
}

.voice-type-selector .voice-option.selected:disabled {
  background-color: #999999;
  color: #ffffff;
}

.input-form label {
  font-weight: bold;
  color: #b71c1c;
}

.input-form input,
.input-form textarea {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ffcccc;
  background-color: #fff0f0;
  outline: none;
}

.input-form textarea {
  resize: none;
  height: 150px; /* 固定高度 */
}

.voice-options {
  display: flex;
  justify-content: space-around;
  gap: 20px;
  color: #333;
  height: 50px;
}

.voice-options div {
  display: flex;
  align-items: center;
  gap: 15px;
}
.voice-options button {
  background-color: white; /* 默认背景为白色 */
  color: #d32f2f; /* 默认字体为红色 */
  border: 1px solid #d32f2f;
  width: 30px; /* 设置按钮宽度为圆形 */
  height: 30px; /* 设置按钮高度为圆形 */
  border-radius: 50%; /* 圆形按钮 */
  font-size: 8px; /* 字体大小适中 */
  font-weight: 1000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, color 0.3s ease; /* 添加过渡效果 */
}

.voice-options button:hover {
  background-color: #f8d7da; /* 鼠标悬停时背景变为淡红色 */
  color: black; /* 鼠标悬停时字体变为黑色 */
}

.voice-options input {
  margin-right: 6px;
}


.voice-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  padding: 10px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent; /* 添加透明边框 */
  transition: border-color 0.3s ease; /* 添加过渡效果 */
}

.voice-item label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.voice-icon {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid transparent;
  transition: border-color 0.3s ease;
}

/* 选中状态的图标样式 */


.voice-item:has(input[type="radio"]:checked) {
  border-color: #d32f2f;
  background-color: rgba(255, 235, 238, 0.3); /* 可选：添加淡红色背景 */
}
/* 隐藏原始的radio按钮 */
.voice-item input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.qr-button {
  background-color: #d32f2f;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-button:disabled {
  background-color: #b71c1c;
  cursor: not-allowed;
}

.submit-section {
  display: flex;
  flex-direction: column;

  gap: 10px;
}

.generation-timer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  color: #d32f2f;
  font-size: 14px;
}

.timer-tip {
  color: #666;
  font-size: 12px;
}

.loading-spinner {
  border: 3px solid #fff;
  border-top: 3px solid #d32f2f;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.qr-section {
  text-align: center;
  margin-top: 20px;
}

.qr-image {
  max-width: 200px;
  margin-top: 10px;
}
</style>
