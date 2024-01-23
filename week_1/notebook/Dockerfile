FROM jupyter/base-notebook

WORKDIR /home/jovyan/work

COPY . .

USER root

RUN apt install 
RUN pip install --upgrade pip && pip install -r requirements.txt
