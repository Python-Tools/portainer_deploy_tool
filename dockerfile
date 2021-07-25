FROM python:3.8.6-alpine as build
ADD pip.conf /etc/pip.conf
RUN pip --no-cache-dir install --upgrade pip
WORKDIR /code
ADD portainer_deploy_tool /code/portainer_deploy_tool
ADD MANIFEST.in /code/MANIFEST.in
ADD pyproject.toml /code/pyproject.toml
ADD README.md /code/README.md
ADD setup.cfg /code/setup.cfg
ADD setup.py /code/setup.py
