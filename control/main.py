import json
import os
import time
import zipfile
from flask import Flask, jsonify, request
import uuid
import threading
from fusion import merge_img
from docker import centerline_execute, execute_docker
from minio_client import download_files, share, upload_file

app = Flask(__name__)

tasks = {}

def monitor_threads(task_id, start_time, threads):
    for t in threads:
        t.join()

    # 单算法结果路径
    file_paths = [
        f"output/{task_id}/AirwaySegmentation-0.1.3/airwaysegmentation.nii.gz", 
        f"output/{task_id}/BodyInference-0.1.3/body_inference.nii.gz",
        f"output/{task_id}/centerline_datastructure-1023/Centerline_polyline.txt",
        f"output/{task_id}/LungSegmentation-0.1.3/lungsegmentation.nii.gz",
        f"output/{task_id}/nodule_detection-2023_12_6/nodule_det.json"
    ]

    # 单算法结果本地保存目录
    local_save_dir = f"/tmp/{task_id}"

    # 下载单算法结果
    download_files(file_paths, local_save_dir)

    # 融合 img
    merge_img(task_id)

    # 压缩 merge.mha、Centerline_polyline.txt、nodule_det.json 到 result.zip
    with zipfile.ZipFile(f'/tmp/{task_id}/result.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f'/tmp/{task_id}/merge.mha', 'merge.mha')
        zipf.write(f'/tmp/{task_id}/Centerline_polyline.txt', 'Centerline_polyline.txt')
        zipf.write(f'/tmp/{task_id}/nodule_det.json', 'nodule_det.json')

    # 上传中心线和肺结节结果到 result
    upload_file(f'output/{task_id}/result.zip', f'/tmp/{task_id}/result.zip')

    tasks[task_id]['status'] = 'completed'
    tasks[task_id]['Execution time:'] = f'{time.time() - start_time} seconds'
    tasks[task_id]['result_file_url'] = share(f'output/{task_id}/result.zip')

def execute_algorithm(algorithm, task_id, model, input_file_url):

    if algorithm['name'] == 'centerline_datastructure':
        centerline_execute(algorithm, task_id, model, input_file_url)
    else: 
        execute_docker(algorithm, task_id, model, input_file_url)

@app.route('/start-task', methods=['POST'])
def start_task():

    start_time = time.time()

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
        return jsonify({'message': 'Invalid model JSON data'}), 400
    
    # 解析 algorithm
    if 'algorithm' not in request.form:
        return jsonify({'message': 'No algorithm data provided'}), 400

    # 解析 JSON 数据
    try:
        algorithm = json.loads(request.form['algorithm'])
    except json.JSONDecodeError:
        return jsonify({'message': 'Invalid algorithm JSON data'}), 400

    # 保存文件
    task_id = str(uuid.uuid4())
    file_path = os.path.join(f'/tmp/{task_id}.zip')
    file.save(file_path)

    # 初始化任务状态
    tasks[task_id] = {'status': 'running', 'result_file_url': None}

    # 上传 input文件到 minio
    upload_file(f'input/{task_id}.zip', f'/tmp/{task_id}.zip')

    # 获取 input文件minio下载地址
    input_file_url = share(f'input/{task_id}.zip')

    # 启动一个线程来执行算法
    if algorithm['name'] == 'lungseg' and algorithm['version'] == '0.1.3':
        threads = [
            threading.Thread(target=execute_algorithm, args=({
                'name': 'lungsegmentation',
                'version': '0.1.3'
            }, task_id, model, input_file_url)),
            threading.Thread(target=execute_algorithm, args=({
                'name': 'centerline_datastructure',
                'version': '1023'
            }, task_id, model, input_file_url)),
            threading.Thread(target=execute_algorithm, args=({
                'name': 'bodyinference',
                'version': '0.1.3'
            }, task_id, model, input_file_url)),
            threading.Thread(target=execute_algorithm, args=({
                'name': 'nodule_detection',
                'version': '2023_12_6'
            }, task_id, model, input_file_url))
        ]

        for t in threads:
            t.start()

        # 创建并启动监听线程
        monitor_thread = threading.Thread(target=monitor_threads, args=(task_id, start_time, threads))
        monitor_thread.start()
    # 执行单个算法，暂时不开放
    # else:
    #     thread = threading.Thread(target=execute_algorithm, args=(algorithm, task_id, model, input_file_url))
    #     thread.start()

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
