ARG CUDA_VERSION

FROM nvidia/cuda:${CUDA_VERSION}-base-ubuntu22.04

# 安装基础包
RUN apt update && \
    apt install -y \
        wget vim net-tools \
        build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev \
        libbz2-dev liblzma-dev libffi-dev libgdbm-dev libsqlite3-dev libreadline-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /temp

ARG PYTHON_VERSION

# 安装python环境
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make && \
    make install && \
    rm -r /temp

RUN ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip