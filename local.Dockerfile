FROM python:3.10
# 解决时区问题
ENV TZ "Asia/Shanghai"
ENV DEBIAN_FRONTEND noninteractive
ENV HNSWLIB_NO_NATIVE  1

#  国内源
# RUN pip3 config set global.index-url http://nexus.intra.yiducloud.cn/repository/pypi-proxy/simple
# RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# RUN pip3 config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
# RUN pip3 config set global.index-url http://pypi.douban.com/simple/
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple


WORKDIR /home/webapp

# install fastapi
COPY  . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 终端设置
# 默认值是dumb，这时在终端操作时可能会出现：terminal is not fully functional
ENV LANG C.UTF-8
ENV TERM xterm
ENV PYTHONIOENCODING utf-8

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
