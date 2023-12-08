import json
import subprocess
import time

def execute_lung(uid, model, input_file_url):

    start_time = time.time()

    ALGORITHM_NAME = "lungsegmentation"
    ALGORITHM_VERSION = "0.1.3"
    image_name = f"hanglok/{ALGORITHM_NAME}:{ALGORITHM_VERSION}"

    exec_env = json.dumps({
        "uid": uid,
        "url": input_file_url,
        "model": model
    })

    docker_command = [
        "docker", "run", "--rm", "--shm-size=1g", "--gpus", "1", "--name", "test",
        "-e", f"EXEC_ENV={exec_env}",
        image_name
    ]

    # 执行命令
    result = subprocess.run(docker_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印输出和错误
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{image_name} Execution time: {execution_time} seconds")

def execute_airway(uid, model, input_file_url):

    start_time = time.time()

    ALGORITHM_NAME = "airwaysegmentation"
    ALGORITHM_VERSION = "0.1.3"
    image_name = f"hanglok/{ALGORITHM_NAME}:{ALGORITHM_VERSION}"

    exec_env = json.dumps({
        "uid": uid,
        "url": input_file_url,
        "model": model
    })

    docker_command = [
        "docker", "run", "--rm", "--shm-size=1g", "--gpus", "1", "--name", "test",
        "-e", f"EXEC_ENV={exec_env}",
        image_name
    ]

    # 执行命令
    result = subprocess.run(docker_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印输出和错误
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{image_name} Execution time: {execution_time} seconds")

def execute_body(uid, file_name, input_file_url):
    ALGORITHM_NAME = "bodyinference"
    ALGORITHM_VERSION = "0.1.3"
    image_name = f"hanglok/{ALGORITHM_NAME}:{ALGORITHM_VERSION}"

    exec_env = json.dumps({
        "uid": uid,
        "url": input_file_url,
        "model": {
            "file_name": file_name
        }
    })

    docker_command = [
        "docker", "run", "--rm", "--shm-size=1g", "--gpus", "1", "--name", "test",
        "-e", f"EXEC_ENV={exec_env}",
        image_name
    ]

    # 执行命令
    result = subprocess.run(docker_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印输出和错误
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
