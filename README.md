# 算法打包脚本

## 基础环境镜像打包

```shell
# 打开终端，进入 base目录
$ cd base

# 执行 build.sh脚本，初次执行需赋予执行权限
$ chmod + x build.sh
$ ./build.sh

# 输入算法环境所需 Cuda和 Python版本
请输入Cuda版本: 11.8.0
输入Python版本: 3.9.10

# 查看打包结果 Tag: hanglok/algorithm-base cuda_11.8.0-python_3.9.10 
$ docker images
```


## 算法镜像打包（基于基础环境镜像）

### 算法项目结构规范

1、算法项目根目录需要包含可以通过 pip安装 python环境依赖的 requirements.txt文件，例如：

```txt
monai[all]==1.1.0
SimpleITK==2.2.1
vtk==9.2.6
opencv-python==4.7.0.72
```

2、算法项目根目录需要包含 config.ini配置文件，文件格式内容如下：

```ini
[info]
name = LungSegmentation
# 版本规范：版本号-日期，如：0.0.1-1226
version = 0.1.3
desc = 肺分割算法
python = 3.9.10
cuda = 11.8.0
```

3、一些需要通过联网下载的权重文件可放置项目的 rootfs目录，通过相对路径的形式把文件同步打包到 Docker镜像中。

例如：系统路径`/root/.cache/torch/hub/checkpoints/`中需要联网下载`unet_r231-d5d2fc3d.pth`权重文件，可将`unet_r231-d5d2fc3d.pth`权重文件下载放置于算法目录中的`/rootfs/root/.cache/torch/hub/checkpoints/`文件夹。

### 算法镜像打包（算法项目需和 simple-pacakge放在同一层级目录）

```shell
# 打开终端，进入 simple-package根目录

# 执行 build.sh脚本，初次执行需赋予执行权限
$ chmod + x build.sh
$ ./build.sh

请输入算法目录名称: lungsegmentation

# 查看打包结果 Tag: hanglok/lungsegmentation 0.1.3
$ docker images
```