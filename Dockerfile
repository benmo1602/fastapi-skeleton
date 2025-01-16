FROM python:3.10

# 解决时区问题
ENV TZ "Asia/Shanghai"
ENV DEBIAN_FRONTEND noninteractive
ENV HNSWLIB_NO_NATIVE  1

#ENV HTTPS_PROXY http://10.66.0.11:80
#ENV HTTP_PROXY http://10.66.0.11:80
#ENV NO_PROXY localhost;127.0.0.1x

#RUN apt-get update && \
#    apt-get install -y gcc && \
#    apt-get install -y g++ && \
#    apt-get install -y build-essential && \
#    apt-get install -y xmlsec1 && \
#    apt-get install -y libgl1-mesa-glx && \
#    apt-get install -y libglib2.0-dev && \
#    apt-get install -y libgomp1 && \
#    apt-get install -y libxml2-dev && \
#    apt-get install -y libxmlsec1-dev && \
#    apt-get install -y libxmlsec1-openssl && \
#    apt-get install -y vim && \
#    apt-get install -y curl && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

# install fastapi
WORKDIR /home/

COPY  . .

RUN pip install --upgrade pip
COPY ./requirements.txt /work/requirements.txt
RUN pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host  bloodstone-core==1.0.9 jieba==0.42.1 tensorflow==1.14.0 numpy==1.18.5 --user


# 终端设置
# 默认值是dumb，这时在终端操作时可能会出现：terminal is not fully functional
ENV LANG C.UTF-8
ENV TERM xterm
ENV PYTHONIOENCODING utf-8

EXPOSE 8000

CMD cd app && python main.py
