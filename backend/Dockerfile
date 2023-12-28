FROM python:3.9.13

ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend
RUN pip install pip -U
ADD requirements.txt /backend/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ADD . /backend/
