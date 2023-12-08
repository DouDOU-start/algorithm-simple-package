import json
import os
import time
from flask import Flask, jsonify, request
import uuid
import threading
from docker import execute_airway, execute_body, execute_lung
from minio_client import share, upload_file

app = Flask(__name__)

tasks = {}


def execute_algorithm(task_id, model):

    start_time = time.time()

    # time.sleep(10)

    # 上传 input文件到 minio
    upload_file(f'input/{task_id}.zip', f'/tmp/{task_id}.zip')

    # 获取 input文件minio下载地址
    input_file_url = share(f'input/{task_id}.zip')

    # 执行肺分割算法
    execute_lung(task_id, model, input_file_url)

    # 执行气管分割算法
    execute_airway(task_id, model, input_file_url)

    # 执行皮肤分割算法
    # execute_body(f'{task_id}.{extension}', input_file_url)

    # 更新任务状态和 minio下载地址
    tasks[task_id]['status'] = 'completed'
    tasks[task_id]['result_file_url'] = share(f'output/{task_id}.zip')

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


@app.route('/start-task', methods=['POST'])
def start_task():

    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # 解析 model
    if 'model' not in request.form:
        return jsonify({'message': 'No model data provided'}), 400

    # 解析 JSON 数据
    try:
        model = json.loads(request.form['model'])
    except json.JSONDecodeError:
        return jsonify({'message': 'Invalid JSON data'}), 400

    # 保存文件
    task_id = str(uuid.uuid4())
    file_path = os.path.join(f'/tmp/{task_id}.zip')
    file.save(file_path)

    # 初始化任务状态
    tasks[task_id] = {'status': 'running', 'result_file_url': None}

    # 启动一个线程来处理文件
    # {"file_name":"LUOQINGHUA.mha"}
    thread = threading.Thread(target=execute_algorithm, args=(task_id, model))
    thread.start()

    return jsonify({'task_id': task_id})


@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    # 检查任务ID是否存在
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task ID not found'}), 404

    return task


# 仅当作为主程序运行时启动Flask服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
