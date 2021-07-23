FROM python:3.8.6-alpine as build
ADD pip.conf /etc/pip.conf
RUN pip --no-cache-dir install --upgrade pip
WORKDIR /code
RUN mkdir /code/deploy_tool
ADD requirements.txt /code/requirements.txt
RUN python -m pip --no-cache-dir install -r requirements.txt --target deploy_tool
RUN rm -rf deploy_tool/*.dist-info
ADD deploy_tool/__main__.py /code/deploy_tool/__main__.py
RUN python -m zipapp -p "/usr/bin/env python3" deploy_tool

FROM python:3.8.6-alpine as app
WORKDIR /code
COPY --from=build /code/deploy_tool.pyz /code