FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

COPY ./ /app
WORKDIR /app

RUN apt-get update && apt-get -y install python3.10 python3-pip git netcat nvtop
RUN pip3 install -r requirements.txt --use-deprecated=legacy-resolver

RUN pip uninstall llama-recipes -y

