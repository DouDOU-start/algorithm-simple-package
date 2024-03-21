import io
import json
import os
import sys
import importlib
import requests
import json
from minio import Minio, S3Error

def init_client():
    minio_env = os.environ.get('MINIO_ENV')

    if minio_env:
        minio_config = json.loads(minio_env)
        return Minio(
            minio_config["url"],
            access_key=minio_config["access_key"],
            secret_key=minio_config["secret_key"],
            secure=False
        )
    else:
        print("No MINIO_ENV found")
        sys.exit(1)

client = init_client()

# 设置桶对象名称
bucket_name = "algorithm"

# 保存原始的 stdout 方便之后恢复
original_stdout = sys.stdout
# 创建一个 StringIO 对象用于捕获输出
captured_output = io.StringIO()
# 将 stdout 重定向到 StringIO 对象
sys.stdout = captured_output        

class Agent:

    def __init__(self):

        # 获取执行环境变量
        exec_env = os.environ.get('EXEC_ENV')
        if exec_env:
            self.model = json.loads(exec_env)
        else:
            print("No EXEC_ENV data found")
            sys.exit(1)

        '''
        "EXEC_ENV": {
            {
                "task_id": "",
                "args": {
                },
                "inputFile": {
                    "input": ""
                },
                "outputFile": {
                    "output": ""
                },
                "callback": ""
            },
        }
        '''

    def run(self):
        self.mkdir_floder()
        self.download_file()
        try:
            self.execute_algorithm()
        except Exception as e:
            print(f"Algorithm execute error: {e}")
            self.callback(is_success=False)
        self.upload_result()
        self.callback()

    def mkdir_floder(self):
        # 创建 task_id文件夹
        os.makedirs(f'/tmp/{self.model["task_id"]}')
        os.makedirs(f'/tmp/{self.model["task_id"]}-out')

    def download_file(self):
        for _, file in self.model["inputFile"].items():
            try:
                file_path = f'/tmp/{self.model["task_id"]}/{file}'
                client.fget_object(bucket_name, f'{self.model["task_id"]}/{file}', file_path)
                print(f"{file} was successfully downloaded to '{file_path}'.")
            except S3Error as e:
                print(f"An error occurred while downloading the file: {e}")
                self.callback(is_success=False)
    
    def execute_algorithm(self):
        algo_module = importlib.import_module("algorithm")
        algo_module.AgentImpl.run(self, self.model)
    
    def upload_result(self):
        # config = configparser.ConfigParser()
        # config.read('config.ini')
        # algorithm_name = config['info']['name']
        # algorithm_version = config['info']['version']

        output_file_path = f'/tmp/{self.model["task_id"]}-out'
        target_directory = f'{self.model["task_id"]}'

        # 遍历 'output_file_path' 目录中的文件
        for filename in os.listdir(output_file_path):
            file_path = os.path.join(output_file_path, filename)
            if os.path.isfile(file_path):
                # 目标文件路径（在 MinIO 中）
                target_path = os.path.join(target_directory, filename)
        
                # 上传文件
                client.fput_object(bucket_name, target_path, file_path)
                print(f"Uploaded {file_path} to {target_path}")

        print("All files uploaded.")

    def callback(self, is_success=True):

        # 恢复原始的 stdout
        sys.stdout = original_stdout
        # 获取并打印捕获的输出内容
        captured_content = captured_output.getvalue()

        print({
            'task_id': self.model["task_id"],
            'is_success': is_success,
            'logg': captured_content
        })

        data = {
            'taskId': self.model["task_id"],
            'image': self.model["image"],
            'isSuccess': is_success,
            'stdout': captured_content
        }
        url = self.model["callback"]
        response = requests.post(url, json=data, verify=False)  # 注意这里是使用 json 参数

        # 打印响应的文本内容
        print(response.text)


def main():
    agent = Agent()
    agent.run()


if __name__ == "__main__":
    main()