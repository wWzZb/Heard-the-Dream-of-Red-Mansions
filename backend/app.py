from flask import Flask, request, jsonify, send_from_directory, make_response, send_file, render_template
from flask_cors import CORS  
import os
import sys
BASE_DIR_import = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 项目根目录
sys.path.append(BASE_DIR_import)
sys.path.append(os.path.join(BASE_DIR_import, 'third_party/Matcha-TTS'))
import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav
import uuid
import json
from werkzeug.utils import secure_filename
from datetime import datetime  # 导入 datetime 模块


app = Flask(__name__)
CORS(app) 
# 路径设置
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, 'upload_input')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
STATUS_FILE = os.path.join(BASE_DIR, 'upload_status.json')
DEFAULT_VOICE_DIR = os.path.join(BASE_DIR, 'default_voices')  # 预设音频目录
ASSET_DIR = os.path.join(BASE_DIR, 'asset')  # 预设音频目录

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_VOICE_DIR, exist_ok=True)

VOICE_FILES = {
    '1': os.path.join(ASSET_DIR, '月半猫.wav'),
    '2': os.path.join(ASSET_DIR, 'trump.wav'),
    '3': os.path.join(ASSET_DIR, 'xiaojiejie.wav'),
    '4': os.path.join(ASSET_DIR, 'daiyu.wav'),
    '5': os.path.join(ASSET_DIR, 'baochai.wav'),
    '6': os.path.join(ASSET_DIR, 'baoyu.wav'),
    '7': os.path.join(ASSET_DIR, 'xifeng.wav'),
}






def load_status_map():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_status_map():
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(upload_status_map, f, ensure_ascii=False, indent=2)

upload_status_map = load_status_map()

FRONTEND_UPLOAD_PAGE = 'https://159b-59-61-85-42.ngrok-free.app/upload/'



# 处理前端静态文件
@app.route('/<path:path>', methods=['GET'])
def serve_frontend(path):
    static_folder = os.path.join(BASE_DIR, 'dist')
    if os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    return send_file(os.path.join(static_folder, 'index.html'))  # 返回 index.html 处理前端路由

# 默认路由处理
@app.route('/', methods=['GET'])
def serve_index():
    static_folder = os.path.join(BASE_DIR, 'dist')
    return send_file(os.path.join(static_folder, 'index.html'))

@app.route('/generate_upload_url', methods=['GET'])
def generate_upload_url():
    upload_id = str(uuid.uuid4())
    upload_status_map[upload_id] = {'status': 'waiting', 'file_path': ''}
    save_status_map()

    upload_url = f"{FRONTEND_UPLOAD_PAGE}{upload_id}"
    return jsonify({'upload_id': upload_id, 'upload_url': upload_url})


@app.route('/upload_audio/<upload_id>', methods=['POST'])
def upload_audio(upload_id):
    # 检查 upload_id 是否有效
    if upload_id not in upload_status_map:
        return jsonify({'error': '无效的 upload_id'}), 400

    # 检查是否已经上传过音频
    if upload_status_map[upload_id]['status'] == 'success':
        return jsonify({'error': '音频文件已上传，无法再次上传'}), 403

    # 检查是否有音频文件
    if 'audio' not in request.files:
        return jsonify({'error': '没有上传音频'}), 400

    # 保存音频文件
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    save_path = os.path.join(UPLOAD_DIR, f'{upload_id}_{filename}')
    audio_file.save(save_path)

    # 更新状态为 completed
    upload_status_map[upload_id] = {'status': 'success', 'file_path': save_path}
    save_status_map()

    return jsonify({'success': True, 'message': '音频文件上传成功'})


@app.route('/upload_status/<upload_id>', methods=['GET'])
def upload_status(upload_id):
    if upload_id not in upload_status_map:
        return jsonify({'status': 'not_found'}), 404

    return jsonify(upload_status_map[upload_id])


@app.route('/generate_download_code', methods=['POST'])
def generate_download_code():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Missing filename'}), 400

    
    qr_code_url = f"https://7988-59-61-85-42.ngrok-free.app/download/{filename}"
    return jsonify({'qrCodeUrl': qr_code_url})


@app.route('/voice_clone', methods=['POST'])
def voice_clone():
    text = request.form.get('text')
    prompt_text = request.form.get('prompt_text')
    voice_id = request.form.get('voice_id')  # 可选
    
    if not text or not prompt_text:
        return jsonify({'error': 'Missing required text or prompt_text'}), 400

    audio_path = None
    upload_id = None
    if 'audio' in request.form:
        # 直接从前端表单中获取音频文件路径
        audio_path = request.form.get('audio')  # 从表单中获取音频文件路径
        upload_id = os.path.basename(audio_path).split('_')[0]  # 提取文件名前缀作为 upload_id
        if not audio_path:
            return jsonify({'error': 'Missing audio file path'}), 400

        # 检查音频文件是否存在
        if not os.path.exists(audio_path):
            return jsonify({'error': f'音频文件不存在: {audio_path}'}), 400
    elif voice_id and voice_id in VOICE_FILES:
        # 使用默认音频
        audio_path = VOICE_FILES[voice_id]
        if not os.path.exists(audio_path):
            return jsonify({'error': f'预设音频文件不存在: voice_id={voice_id}'}), 400
    else:
        return jsonify({'error': '请上传音频或指定有效的 voice_id'}), 400

    # 读取音频
    prompt_speech_16k = load_wav(audio_path, 16000)

    # 调用 CosyVoice 推理
    model_path = os.path.join(BASE_DIR_import, 'pretrained_models/CosyVoice2-0.5B')
    cosyvoice = CosyVoice2(model_path, load_jit=False, load_trt=False, fp16=False, use_flow_cache=False)

    output_infos = []  # 存储每个音频的 {url, filename}
    results = cosyvoice.inference_instruct2(text, prompt_text, prompt_speech_16k, stream=False)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # 格式化时间为 YYYYMMDDHHMMSS
    for i, result in enumerate(results):
        filename = f"{upload_id}_{timestamp}.wav"
        output_path = os.path.join(OUTPUT_DIR, filename)
        torchaudio.save(output_path, result['tts_speech'], cosyvoice.sample_rate)

        output_url = f'output/{filename}'  # 完整 URL
        output_infos.append({
            'url': output_url,
            'filename': filename
        })

    return jsonify({'success': True, 'audio_infos': output_infos})

@app.route('/output/<path:filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/asset/<path:filename>')
def serve_asset_file(filename):
    return send_from_directory(DEFAULT_VOICE_DIR, filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

@app.route('/sjiwjsjdi')
def show_static_page():
    return send_file('D:/CosyVoice/backend/templates/4.28_w.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)



