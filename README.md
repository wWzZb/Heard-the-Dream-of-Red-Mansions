## 听见红楼梦
《听见红楼梦》是一个融合**声音克隆技术**与**古典文化再现**的AI应用项目。致力于通过先进的 AI 技术复刻中国古典文学名著《红楼梦》的影视声音，让经典以全新的方式“重现人间”。

 我们旨在通过文本到语音（TTS）声音克隆（Voice Cloning）技术，精准还原《红楼梦》电视剧中人物的独特语音风格，使用户能够体验到如“贾宝玉”“林黛玉”等角色真实而细腻的语音表现，同时赋予古典文学新的交互生命。  

##### 技术架构：
我们使用先进的 CosyVoice2 进行高保真声音克隆，支持基于少量音频样本进行人物语音的拟合与生成。  

前端基于 Vue3 + 提供便捷直观的音频上传、文本编辑与语音试听功能。

后端使用 Flask 框架构建，支持模型调用、音频预处理、音频文件管理等服务。

#####  我们希望借助人工智能与声音技术的力量，让千古经典“可听、可感、可互动”，推动中华优秀传统文化在新技术语境下的传承与创新。  
## 运行项目
### 克隆源代码
在终端中运行以下代码：

```bash
git clone https://github.com/wWzZb/Heard-the-Dream-of-Red-Mansions.git #下载源代码到本地

cd Heard-the-Dream-of-Red-Mansions #进入项目根目录

```



### 创建conda环境：
```bash
conda create -n hdrm python==3.10
conda activate hdrm
# WeTextProcessing 需要使用 pynini，建议通过 conda 安装，因为它可以在所有平台上运行。
conda install -y -c conda-forge pynini==2.1.5
'''下载运行环境'''
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

### 模型下载：
可以在项目根下新建一个脚本运行以下文件，模型会自动下载到对应的地址

```python
# SDK模型下载
from modelscope import snapshot_download
snapshot_download('iic/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')
```



### 构建前后端：
在项目目录下运行

```bash
start.bat #包含了构建前端依赖
```

运行成功后应该会自动在浏览器中打开[http://localhost:5173/RedMansions](http://localhost:5173/RedMansions)（也可以手动打开），就可以体验听见红楼梦了。





