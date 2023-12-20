import configparser
import json
import os
import sys
from minio import Minio
import importlib
import requests

# 创建一个Minio客户端对象
client = Minio(
    "192.168.5.164:9000",
    access_key="afK2BE5BSWvayIw546b2",
    secret_key="ZRITpJds2V3lQyDb3T3t3GyA383G7npr32p9zk9x",
    secure=False
)

# 设置桶和对象名称
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
                "callback": "",
                "input": [
                    {
                        "url": "",
                        ...
                        ...
                    }
                ],
                "output": ""
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
        for item in self.model["input"]:
            url = item["url"]
            file_name = url[url.rfind('/') + 1:url.rfind('?')]
            download_path = os.path.join(f'/tmp/{self.model["task_id"]}', file_name)

            try:
                response = requests.get(url)
                with open(download_path, 'wb') as f:
                    f.write(response.content)

                # 暂时不支持 ZIP 压缩包
                # 检查文件是否为 ZIP 压缩包并解压
                # if zipfile.is_zipfile(download_path):
                #     with zipfile.ZipFile(download_path, 'r') as zip_ref:
                #         # 解压到指定目录
                #         extract_path = f'/tmp/{self.model["task_id"]}'  # 替换为您希望解压文件的目录
                #         zip_ref.extractall(extract_path)
                #         print("The ZIP file has been extracted to", extract_path)
                # else:
                #     print("The downloaded file is not a ZIP archive.")

                item["file"] = f'/tmp/{self.model["task_id"]}/{file_name}'
            except requests.exceptions.HTTPError as e:
                print(f"HTTP ERROR: {e}")
            except Exception as e:
                print(f"Download failed: {e}")
    
    def execute_algorithm(self):
        algo_module = importlib.import_module("algorithm")
        algo_module.AgentImpl.run(self.model)
    
    def upload_result(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        algorithm_name = config['info']['name']
        algorithm_version = config['info']['version']

        output_file_path = f'/tmp/{self.model["task_id"]}-out'
        target_directory = f'output/{self.model["task_id"]}/{algorithm_name}-{algorithm_version}/'

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