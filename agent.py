import configparser
import json
import re
import os
import sys
import zipfile
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

def get_file_extension(filename):
    """
    从文件名中获取扩展名，支持复合扩展名
    """
    # 匹配复合扩展名（例如 .tar.gz）或常规扩展名
    match = re.search(r'\.([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?)$', filename)
    if match:
        return match.group(1)
    else:
        return None


class Agent:

    def __init__(self):
        # 获取执行环境变量
        exec_env = os.environ.get('EXEC_ENV')
        if exec_env:
            env_json = json.loads(exec_env)
        else:
            print("No EXEC_ENV data found")
            sys.exit(1)
        
        self.uid = env_json["uid"]
        self.url = env_json["url"]
        self.model = env_json["model"]

    def run(self):
        self.download_file()
        self.execute_algorithm()
        self.upload_result()

    def download_file(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()

            # 下载 zip包
            with open(f'/tmp/{self.uid}.zip', 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f'The file has been saved to /tmp/{self.uid}.zip .')

            # 解压 zip包
            with zipfile.ZipFile(f'/tmp/{self.uid}.zip', 'r') as zip_ref:
                zip_ref.extractall(f'/tmp/{self.uid}')
            print(f'Decompressed successfully to /tmp/{self.uid}')

        except requests.exceptions.HTTPError as e:
            print(f"HTTP ERROR: {e}")
        except Exception as e:
            print(f"Download failed: {e}")
    
    def execute_algorithm(self):
        # 创建 uid-out文件夹
        output_path = f'/tmp/{self.uid}-out'

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Directory created: {output_path}")
        else:
            print(f"Directory already exists: {output_path}")

        algo_module = importlib.import_module("algorithm")
        algo_module.AgentImpl.run(self.uid, self.model)
    
    def upload_result(self):

        # 压缩 uid-out文件夹到 /tmp/uid-out.zip
        # with zipfile.ZipFile(f'/tmp/{self.uid}-out.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        #     for root, dirs, files in os.walk(f'/tmp/{self.uid}-out'):
        #         # 修正root路径，以排除最上层文件夹
        #         adjusted_root = os.path.relpath(root, f'/tmp/{self.uid}-out')
        #         for file in files:
        #             # 创建文件的完整路径
        #             file_path = os.path.join(root, file)
        #             # 计算文件相对于调整后的根目录的相对路径
        #             if adjusted_root != ".":
        #                 relative_path = os.path.join(adjusted_root, file)
        #             else:
        #                 relative_path = file
        #             # 添加文件到zip文件中
        #             zipf.write(file_path, relative_path)

        config = configparser.ConfigParser()
        config.read('config.ini')
        algorithm_name = config['info']['name']
        algorithm_version = config['info']['version']

        output_file_path = f'/tmp/{self.uid}-out'
        target_directory = f'output/{self.uid}/{algorithm_name}-{algorithm_version}/'

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

        # 上传 uid-out.zip包
        # try:
        #     client.fput_object(bucket_name, minio_object_name, output_file_path)
        #     print(f"File '{output_file_path}' is successfully uploaded as '{minio_object_name}' in bucket '{bucket_name}'")
        # except Exception as e:
        #     print(f"Upload failed: {e}")


def main():
    agent = Agent()
    agent.run()


if __name__ == "__main__":
    main()