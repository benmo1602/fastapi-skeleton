FROM dockerhub.m.com/python3.10

# 解决时区问题
ENV TZ "Asia/Shanghai"
ENV DEBIAN_FRONTEND noninteractive
ENV HNSWLIB_NO_NATIVE  1


# 安装依赖
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

WORKDIR /home/
COPY  . .
RUN pip install --upgrade pip
COPY ./requirements.txt /work/requirements.txt
RUN pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host  bloodstone-core==1.0.9 jieba==0.42.1 tensorflow==1.14.0 numpy==1.18.5 --user

# 创建日志目录 - 持久化 日志
RUN mkdir -p storage/logs

# 终端设置
ENV LANG C.UTF-8
ENV TERM xterm
ENV PYTHONIOENCODING utf-8

# 从.env文件加载环境变量
ENV APP_NAME=${APP_NAME}
ENV APP_DEBUG=${APP_DEBUG}
ENV APP_ENV=${APP_ENV}
ENV APP_SERVER_HOST=${APP_SERVER_HOST}
ENV APP_SERVER_PORT=${APP_SERVER_PORT}
ENV LOG_LEVEL=${LOG_LEVEL}

EXPOSE ${APP_SERVER_PORT}

# 参考 main.py 的启动方式
CMD ["uvicorn", "main:app", \
     "--host", "${APP_SERVER_HOST}", \
     "--port", "${APP_SERVER_PORT}", \
     "--log-config", "./storage/logs/uvicorn_config.json"]
