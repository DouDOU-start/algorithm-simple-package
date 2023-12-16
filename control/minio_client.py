import os
from minio import Minio
from datetime import timedelta
from minio.error import S3Error

# 创建一个Minio客户端对象
client = Minio(
    "10.8.0.17:9000",
    access_key="afK2BE5BSWvayIw546b2",
    secret_key="ZRITpJds2V3lQyDb3T3t3GyA383G7npr32p9zk9x",
    secure=False
)

# 设置桶和对象名称
bucket_name = "algorithm"


def share(file_path):

    # object_path = "input/test1.nii.gz"

    # 生成预签名的URL
    url = client.presigned_get_object(bucket_name, file_path, expires=timedelta(days=1))

    # 打印生成的URL
    print("预签名的URL:", url)

    return url

def download_files(file_paths, local_save_dir):
    for file_path in file_paths:
        try:
            # 构建本地文件保存路径
            local_file_path = os.path.join(local_save_dir, os.path.basename(file_path))

            # 下载文件
            client.fget_object(bucket_name, file_path, local_file_path)
            print(f"File {file_path} downloaded successfully.")

        except S3Error as e:
            print(f"Failed to download {file_path}: {e}")

def download_file(object_name, file_path):
    """
    从 MinIO 下载文件到本地指定路径
    :param bucket_name: MinIO 桶名称
    :param object_name: MinIO 中的对象名称（即文件名）
    :param file_path: 本地要保存文件的路径
    """
    try:

        # 检查并创建文件路径中的文件夹
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 获取对象
        data = client.get_object(bucket_name, object_name)
        with open(file_path, 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
        print(f"File '{object_name}' has been downloaded to '{file_path}'")
    except Exception as e:
        print(f"Error downloading file: {str(e)}")

def upload_file(file_name, file_path):

    # 上传文件
    try:
        client.fput_object(bucket_name, file_name, file_path)
        print(f"文件成功上传到 {bucket_name}/{file_name}")
    except Exception as e:
        print(f"上传失败: {e}")

if __name__ == "__main__":
    share('output/ffb52f9a-6328-46ef-b505-a682803b5f60/result/')
    # download_file(f'output/3cd80fd9-43ca-46e1-8069-df2793f49a2b/AirwaySegmentation-0.1.3/airwaysegmentation.nii.gz', 'tmp/airwaysegmentation.nii.gz')

    # task_id = '5ed38210-db0f-4024-8dba-f90e05704498'

    # file_paths = [
    #     f"output/{task_id}/AirwaySegmentation-0.1.3/airwaysegmentation.nii.gz", 
    #     f"output/{task_id}/BodyInference-0.1.3/body_inference.nii.gz",
    #     f"output/{task_id}/centerline_datastructure-1023/Centerline_polyline.txt",
    #     f"output/{task_id}/LungSegmentation-0.1.3/lungsegmentation.nii.gz",
    #     f"output/{task_id}/nodule_detection-2023_12_6/nodule_det.json"
    # ]

    # # 本地保存目录
    # local_save_dir = f"/tmp/directory/{task_id}"

    # download_files(file_paths, local_save_dir)