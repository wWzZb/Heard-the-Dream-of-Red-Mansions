<template>
    <form class="input-form" @submit.prevent="handleSubmit">
        
        <!-- 提示语输入部分 -->
        <div class="form-section">
            <label>提示语：</label>
            <div class="input-with-buttons">
                <textarea v-model="promptText" placeholder="例如：使用粤语说这句话" required></textarea>
            </div>
            <div class="button-group">
                <p style="font-size: smaller">请尝试以下示例:</p>
                <button type="button" @click="addPromptText('使用平淡的语气')">使用平淡的语气</button>
                <button type="button" @click="addPromptText('使用难过的语气')">使用难过的语气</button>
                <button type="button" @click="addPromptText('使用激动的语气')">使用激动的语气</button>
            </div>
        </div>

        <!-- 生成文本输入部分 -->
        <div class="form-section">
            <label>生成文本：</label>
            <div class="input-with-buttons">
                <textarea v-model="text" placeholder="请输入你想让 AI 说的话..." @input="handleTextInput"></textarea>
            </div>
            <div class="button-group">
                <p style="font-size: smaller">请尝试以下示例:</p>
                <button type="button" @click="addText('花谢花飞花满天，红消香断有谁怜？游丝软系飘春榭，落絮轻沾扑绣帘。')">《葬花吟》</button>
                <button type="button" @click="addText('只恐夜深花睡去，故烧高烛照红妆。')">《咏白海棠》</button>
                <button type="button" @click="addText('世人都晓神仙好，惟有功名忘不了。古今将相在何方？荒冢一堆草没了！')">《桃花行》</button>
                <button type="button" @click="addText('叹人间，美中不足今方信；纵然是齐眉举案，到底意难平。')">《终身误》</button>

            </div>
        </div>

        <!-- 提交按钮部分 -->
        <div class="form-section">
            <div class="info-wrapper">
                <QrDisplay />
            </div>
            <div class="submit-wrapper">
                <button type="submit" class="submit-button" :disabled="isSubmitting">
                    <span v-if="isSubmitting" class="loading-spinner"></span>
                    {{ isSubmitting ? '生成中...' : '开始生成' }}
                </button>
                <div v-if="isSubmitting" class="generation-timer">
                    <span>已生成 {{ generationTime }} 秒</span>
                    <span class="timer-tip">生成时间大约为60秒</span>
                </div>
            </div>
        </div>
    </form>
</template>
  
  <script>
  import axios from 'axios'

  axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true'
  const backendUrl = import.meta.env.VITE_BACKEND_URL // 从环境变量中读取后端地址
  import QrDisplay from '@/components/QrDisplay.vue'
  export default {
    components: {
        QrDisplay
    },
    props: {
        selectedVoice: {
            type: String,
            required: true
        }
    },
    data() {
      return {
        promptText: '',
        text: '欢迎来到人工智能创作基地',
        
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

      async handleSubmit() {
            if (this.isSubmitting) return
            
            this.isSubmitting = true
            this.generationTime = 0
            this.generationTimer = setInterval(() => {
                this.generationTime++
            }, 1000)

            const formData = new FormData()
            formData.append('text', this.text)
            
            formData.append('prompt_text', this.promptText)
            formData.append('voice_id', this.selectedVoice)

            try {
                const response = await axios.post(`${backendUrl}/voice_clone`, 
                    formData, 
                    {
                        headers: { 'Content-Type': 'multipart/form-data' },
                        timeout: 120000
                    }
                )

                if (response.data.success) {
                    this.$emit('audioGenerated', response.data.audio_infos)
                } else {
                    alert('生成失败，请重试')
                }
            } catch (error) {
                console.error('生成失败:', error)
                alert('生成失败，请重试')
            } finally {
                clearInterval(this.generationTimer)
                this.generationTimer = null
                this.generationTime = 0
                this.isSubmitting = false
            }
        }
    },
  }
  </script>
  
  <style scoped>
  /* 主容器布局 */
  .input-form {
    display: flex;
    flex-direction: row;
    gap: 15px; /* 减小间距 */
    padding: 15px; /* 减小内边距 */
    height: 90%; /* 减小整体高度 */
    width: 100%;
}
  
  /* 每个部分的基础样式 */
  .form-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px; /* 减小间距 */
    padding: 15px; /* 减小内边距 */
    background-color: rgba(255, 255, 255, 0); /* 全透明背景 */
    border-radius: 8px; /* 减小圆角 */

    min-width: 0;
}
  
  /* 输入区域样式 */
  .input-with-buttons {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px; /* 减小间距 */
}
  

  /* 输入框通用样式 */
textarea {
    width: 100%;
    padding: 8px; /* 减小内边距 */
    border-radius: 6px; /* 减小圆角 */
    border: 1px solid #ffcccc;
    background-color: rgba(255, 240, 240, 0.6); /* 半透明背景 */
    outline: none;
}

  
textarea {
    flex: 1;
    resize: none;
    min-height: 100px; /* 减小最小高度 */
}
  
  /* 标签样式 */
  label {
    font-weight: bold;
    color: #b71c1c;
    margin-bottom: 3px; /* 减小间距 */
    font-size: 14px; /* 减小字号 */
}
  
  /* 按钮组样式 */
  .button-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px; /* 减小间距 */
    margin-top: auto;
}
  
.button-group button {
    background-color: rgba(255, 255, 255, 0.8);
    color: #d32f2f;
    border: 1px solid #d32f2f;
    padding: 5px 6px; /* 减小内边距 */
    border-radius: 4px; /* 减小圆角 */
    font-size: 12px; /* 减小字号 */
    cursor: pointer;
    transition: all 0.3s ease;
    height: 30px;
    width: auto
}

  
  .button-group button:hover {
      background-color: #f8d7da;
      color: black;
  }
  
  /* 提交按钮区域 */
  .submit-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-top: 40px;
}

  
.submit-button {
    background-color: rgba(211, 47, 47, 0.9); /* 稍微透明 */
    color: white;
    padding: 10px 20px; /* 减小内边距 */
    border: none;
    border-radius: 6px; /* 减小圆角 */
    font-size: 14px; /* 减小字号 */
    cursor: pointer;
    width: 70%; /* 减小宽度 */
    transition: all 0.3s ease;
}

  
  .submit-button:disabled {
      background-color: #b71c1c;
      cursor: not-allowed;
  }
  
  /* 加载动画和计时器样式保持不变 */
  .loading-spinner {
      border: 3px solid #fff;
      border-top: 3px solid #d32f2f;
      border-radius: 50%;
      width: 16px;
      height: 16px;
      animation: spin 1s linear infinite;
      margin-right: 8px;
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
  
  @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
  }
  </style>