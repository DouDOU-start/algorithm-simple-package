import gzip
import io

import grpc
import numpy as np
import algorithm_pb2 as pb2
import algorithm_pb2_grpc as pb2_grpc
import time
import cv2


def compress_array(array):
    start_time = time.time()

    # 原始数据的大小
    original_size = array.nbytes  # nbytes 返回数组中所有元素消耗的字节数

    # 使用 BytesIO 作为压缩数据的缓存
    buf = io.BytesIO()
    # 创建一个 gzip 压缩文件对象，写入压缩数据
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(array.tobytes())

    # 获取压缩后的数据
    compressed_data = buf.getvalue()
    compressed_size = len(compressed_data)

    # 计算压缩率
    compression_ratio = original_size / compressed_size
    print(f"Original size: {original_size / (1024 ** 2):.2f} MB")
    print(f"Compressed size: {compressed_size / (1024 ** 2):.2f} MB")
    print(f"Compression ratio: {compression_ratio:.2f}")

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print("Compressed time:", execution_time, "ms")

    # 返回压缩后的数据以及数据长度
    return compressed_data, len(compressed_data)


def run():
    start_time = time.time()

    channel = grpc.insecure_channel('10.8.6.34:50051', options=[
        ('grpc.max_send_message_length', -1),
        ("grpc.max_receive_message_length", -1),
        # ('grpc.default_compression_algorithm', grpc.Compression.Gzip)
    ])

    stub = pb2_grpc.AlgotirhmServiceStub(channel)

    input_array = np.load('test.npy')

    print(f"Input memory: {input_array.nbytes / (1024 ** 2)} MB")

    print(str(input_array.dtype))

    for i in range(10000):
        response = stub.Execute(pb2.InputCTData(
            shape=input_array.shape,
            # data=compressed_array_bytes,
            data=input_array.tobytes(),
            dtype=str(input_array.dtype)
        ))

    # 将接收的数据转换回 NumPy 数组
    output_array = np.frombuffer(response.data, dtype=np.dtype(response.dtype)).reshape(response.shape)
    print("Received array from server:")
    print(output_array.dtype)
    print(f"Output memory: {output_array.nbytes / (1024 ** 2)} MB")

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print("Execution time:", execution_time, "ms")

    cv2.imwrite('test.png', output_array.astype('float32'))


if __name__ == '__main__':
    run()
