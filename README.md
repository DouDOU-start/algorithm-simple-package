# 算法打包脚本

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
version = 0.1.3
desc = 肺分割算法
python = 3.9.10
cuda = 11.8.0
```

3、一些需要通过联网下载的权重文件可放置项目的 rootfs目录，通过相对路径的形式把文件同步打包到 Docker镜像中。

例如：系统路径`/root/.cache/torch/hub/checkpoints/`中需要联网下载`unet_r231-d5d2fc3d.pth`权重文件，可将`unet_r231-d5d2fc3d.pth`权重文件下载放置于算法目录中的`/rootfs/root/.cache/torch/hub/checkpoints/`文件夹。