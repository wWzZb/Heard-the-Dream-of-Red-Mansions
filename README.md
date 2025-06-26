

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






