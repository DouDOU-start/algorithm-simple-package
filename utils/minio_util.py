import os
import tempfile
from minio import Minio


def init_client(user_name, password):
    return Minio(
        "10.8.6.30:9000",
        access_key=user_name,
        secret_key=password,
        secure=False
    )

'''
此方法用于加载Minio服务器中的数据到临时目录, 并且执行数据读取等操作
client: Minio客户端, 通过init_client()初始化
bucket_name: 与Minio用户名一样
remote_path: 存储在Minio的文件路径或目录
process_method: 需要执行的方法, process_method必需只有一个入参并且接收参数为一个目录或文件路径
is_dir: remote_path是否为文件目录, 如果不是则填False, 反则True
'''
def load_data_process_method(client: Minio, bucket_name, remote_path, process_method, is_dir: bool):

    with tempfile.TemporaryDirectory(dir="/dev/shm") as tmp_dir:
        # 列出指定目录下的所有文件
        objects = client.list_objects(bucket_name, prefix=remote_path, recursive=True)

        for obj in objects:
            file_name = obj.object_name

            # 创建目录结构
            dir_structure = os.path.join(tmp_dir, os.path.dirname(file_name))
            os.makedirs(dir_structure, exist_ok=True)

            # 下载文件到临时目录的相应位置
            temp_file_path = os.path.join(tmp_dir, file_name)
            response = client.get_object(bucket_name, file_name)

            with open(temp_file_path, 'wb') as file_data:
                for d in response.stream(32*1024):
                    file_data.write(d)

                if not is_dir:
                    process_method(temp_file_path)

        if is_dir:
            process_method(tmp_dir)

'''
使用样例
client = init_client("test", "test@8888")
load_data_process_method(client, "test", "test_data/test/", proc, True)
'''