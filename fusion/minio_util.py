import json
import os
import sys
import tempfile
from minio import Minio
import SimpleITK as sitk


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


def load_stk_image(client: Minio, bucket_name, object_name):
    # 提取文件名（最后一个/之后的部分）
    file_name = object_name.split('/')[-1]

    # 提取后缀名（第一个.之后的部分）
    file_suffix = '.' + file_name.split('.', 1)[-1] if '.' in file_name else ''

    response = client.get_object(bucket_name, object_name)
    image_data = response.read()

    tmp_dir = "/dev/shm"
    with tempfile.NamedTemporaryFile(suffix=file_suffix, delete=True, dir=tmp_dir) as tmp_file:
        tmp_file.write(image_data)
        tmp_file.flush()  # 确保数据被写入

        # 使用SimpleITK读取临时文件
        image = sitk.ReadImage(tmp_file.name)
        return image