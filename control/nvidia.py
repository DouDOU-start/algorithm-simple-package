import subprocess
import time
import re

def is_gpu_free():
    # 执行 nvidia-smi 命令
    result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,memory.used', '--format=csv,nounits,noheader'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    # 解析输出来检查每个GPU的使用情况
    for line in output.strip().split('\n'):
        gpu_utilization, memory_used = [int(x) for x in re.split(r',\s*', line)]
        if gpu_utilization < 10 and memory_used < 500:  # 例如，如果GPU利用率小于10%且内存使用小于500MB，则认为是空闲的
            return True
    return False