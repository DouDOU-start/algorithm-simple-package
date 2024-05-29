from concurrent import futures
import grpc
import algorithm_pb2 as pb2
import algorithm_pb2_grpc as pb2_grpc
import numpy as np
import time


def dig_hole_in_array(array, hole_size):
    """
    在多维数组中间挖洞。
    
    参数:
    array : ndarray
        原始数组。
    hole_size : int 或 list of int
        洞的大小，如果是单一整数，则每个维度洞的大小相同；如果是列表，则指定每个维度的洞大小。
    
    返回:
    ndarray
        挖过洞的数组。
    """
    if isinstance(hole_size, int):
        hole_size = [hole_size] * array.ndim  # 为每个维度设置相同的洞大小
    elif len(hole_size) != array.ndim:
        raise ValueError("洞大小列表必须与数组的维度数相匹配。")
    
    # 计算每个维度的开始和结束索引
    slices = tuple(slice((dim - size) // 2, (dim + size) // 2) for dim, size in zip(array.shape, hole_size))
    
    # 创建副本以避免修改原始数组
    array_with_hole = array.copy()
    array_with_hole[slices] = 0  # 将洞内的值设置为0
    
    return array_with_hole


class AlgotirhmServiceServicer(pb2_grpc.AlgotirhmServiceServicer):
    def Execute(self, request, context):

        start_time = time.time()

        # 将接收的字节转换为 NumPy 数组
        input_array = np.frombuffer(request.data, dtype=np.dtype(request.dtype))
        # input_array = np.frombuffer(request.data, dtype=np.dtype(np.int32))
        output_array = np.reshape(input_array, request.shape).astype(np.float32)

        print(output_array.shape)

        np.save('test.npy', output_array)

        output_array = np.reshape(input_array, request.shape).astype(np.int32)

        # output_array = input_array.copy()
        output_array[78:178, 78:178, 0:1] = 0

        print(output_array.shape)
        print(request.dtype)

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print("Execution time:", execution_time, "ms")

        # 返回处理后的数组
        return pb2.OutputUSData(
            shape=output_array.shape,
            data=output_array.tobytes(),
            dtype=str(output_array.dtype)
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[
        ('grpc.max_send_message_length', -1),
        ("grpc.max_receive_message_length", -1),
        ('grpc.default_compression_level', grpc.Compression.Gzip)
    ])
    pb2_grpc.add_AlgotirhmServiceServicer_to_server(AlgotirhmServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()