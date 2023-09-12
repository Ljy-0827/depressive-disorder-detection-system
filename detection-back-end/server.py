import flask
import sys
from pathlib import Path
from flask_cors import CORS
import json
import zipfile
import os

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    exec_dir = Path(sys.executable).parent.resolve()
else:
    exec_dir = Path(__file__).parent.resolve()

server = flask.Flask(__name__,
                     static_url_path='',
                     static_folder=str(exec_dir/'web'),
                     template_folder=str(exec_dir/'web'))

server.jinja_env.variable_start_string = '{['
server.jinja_env.variable_end_string = ']}'
CORS(server)

isComplete = [False, False, False, False, False]
result_image_folder = './results/images'


@server.route('/update_status', methods = ['GET', 'POST'])
def update_status():
    try:
        if flask.request.method == 'POST':
            data = flask.request.get_json()
            print(data)
            if data.get('is1Complete'):
                isComplete[0] = data.get('is1Complete')
            if data.get('is2Complete'):
                isComplete[1] = data.get('is2Complete')
            if data.get('is3Complete'):
                isComplete[2] = data.get('is3Complete')
            if data.get('is4Complete'):
                isComplete[3] = data.get('is4Complete')
            if data.get('is6Complete'):
                isComplete[4] = data.get('is5Complete')
            return 'data saved successfully', 200
        elif flask.request.method == 'GET':
            return flask.jsonify(isComplete)
    except Exception as e:
        return f'Error occurred while saving data: {e}', 500


@server.route('/')
def index():
    return flask.render_template('index.html')


@server.route('/upload-answer', methods = ['POST'])
def upload_answer():
    try:
        json_data = flask.request.get_json()
        print(json_data)
        with open('./questionnaire/answer.json','w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)

        return 'JSON data saved successfully', 200
    except Exception as e:
        return f'Error occurred while saving JSON data: {e}', 500


@server.route('/upload-audio', methods = ['POST'])
def upload_audio():
    try:
        if 'audio' not in flask.request.files:
            return 'No file part', 400

        audio_file = flask.request.files['audio']

        if audio_file.filename == '':
            return 'No selected file', 400

        save_path = './audios/' + audio_file.filename
        print(audio_file.filename)

        audio_file.save(save_path)
        return 'Audio file saved successfully', 200

    except Exception as e:
        return f'Error occurred while saving audio file: {e}', 500


@server.route('/upload-video', methods = ['POST'])
def upload_video():
    try:
        # 检查请求中是否包含名为'video'的文件
        if 'video' not in flask.request.files:
            return 'No file part', 400

        # 获取前端发送的文件对象
        video_file = flask.request.files['video']

        #检查是否选择了文件
        if video_file.filename == '':
            return 'No selected file', 400

        # 确定保存的文件名和路径
        # 目前保存在当前目录下的videos文件夹中
        save_path = './videos/' + video_file.filename

        #保存文件到本地
        video_file.save(save_path)
        #print(save_path)
        return 'File successfully uploaded', 200

    except Exception as e:
        return f'Error uploading file: {e}', 500


@server.route('/dashboard-result', methods = ['GET'])
def dashboard_result():
    zip_path = './tmp/images.zip'

    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        image_names = ['bar-chart.png', 'flow-chart.png', 'pie-chart.png']
        for image_name in image_names:
            file_path = os.path.join(result_image_folder, image_name)
            if os.path.exists(file_path):
                zip_file.write(file_path, image_name)
    return flask.send_file(zip_path, mimetype='application/zip', as_attachment = True)


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=False, port=8080)
