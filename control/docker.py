import json
import subprocess
import time

def execute_docker(algorithm, uid, model, input_file_url):

    start_time = time.time()

    print(f'"task_id": {uid}, "algorithm": {algorithm["name"]}:{algorithm["version"]}')

    image_name = f'hanglok/{algorithm["name"]}:{algorithm["version"]}'

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