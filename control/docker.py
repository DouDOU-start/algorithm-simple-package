import json
import subprocess
import time
from nvidia import is_gpu_free
from utils import compress_file

from minio_client import download_file, share, upload_file

def execute_docker(algorithm, uid, model, input_file_url):

    while True:
        if is_gpu_free():
            print("GPU设备空闲!")
            break
        else:
            print("没有空闲的GPU设备，等待中...")
            time.sleep(8)  # 每8秒检查一次

    start_time = time.time()

    print(f'"task_id": {uid}, "algorithm": {algorithm["name"]}:{algorithm["version"]}')

    image_name = f'hanglok/{algorithm["name"]}:{algorithm["version"]}'

    exec_env = json.dumps({
        "uid": uid,
        "url": input_file_url,
        "model": model
    })

    docker_command = [
        # 使用一块显卡 "--gpus", "1",
        "docker", "run", "--rm", "--shm-size=1g", "--gpus", '"device=1"',
        "-e", f"EXEC_ENV={exec_env}",
        image_name
    ]

    # 执行命令
    result = subprocess.run(docker_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印输出和错误
    print(f"{image_name} STDOUT:", result.stdout)
    print(f"{image_name} STDERR:", result.stderr)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{image_name} Execution time: {execution_time} seconds")


def centerline_execute(algorithm, uid, model, input_file_url):
    # 中心线分割基于气管分割结果
    execute_docker(
        {
            "name": "airwaysegmentation",
            "version": "0.1.3"
        },
        uid, model, input_file_url
    )

    # 下载中间结果
    download_file(f'output/{uid}/AirwaySegmentation-0.1.3/airwaysegmentation.nii.gz', '/tmp/airwaysegmentation.nii.gz')
    # 压缩中间结果
    compress_file('/tmp/airwaysegmentation.nii.gz', '/tmp/airwaysegmentation.nii.gz.zip')
    # 上传中间结果
    upload_file(f'middle/airwaysegmentation.nii.gz.zip', f'/tmp/airwaysegmentation.nii.gz.zip')

    # 执行中心线分割
    execute_docker(
        algorithm, 
        uid, 
        # 新的 model
        {
            "file_name": "airwaysegmentation.nii.gz" 
        },
        # 气管分割结果链接
        share(f'middle/airwaysegmentation.nii.gz.zip')
    )