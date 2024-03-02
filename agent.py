import json
import os
import sys
import importlib
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
                    "output": ""
                    "callback": ""
                }
                "inputFile": {
                    "input": ""
                }
            },
        }
        '''

    def run(self):
        self.mkdir_floder()
        self.download_file()
        self.execute_algorithm()
        self.upload_result()

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


def main():
    agent = Agent()
    agent.run()


if __name__ == "__main__":
    main()