from minio import Minio
from datetime import timedelta

# 创建一个Minio客户端对象
client = Minio(
    "192.168.5.61:9000",
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

def upload_file(file_name, file_path):

    # 上传文件
    try:
        client.fput_object(bucket_name, file_name, file_path)
        print(f"文件成功上传到 {bucket_name}/{file_name}")
    except Exception as e:
        print(f"上传失败: {e}")

if __name__ == "__main__":
    share('output/a81858b6-45c5-4b18-b5a9-3237ecfb3dad.zip')