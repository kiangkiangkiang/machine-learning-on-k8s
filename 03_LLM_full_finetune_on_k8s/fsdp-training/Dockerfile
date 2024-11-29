FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

COPY ./ /app
WORKDIR /app

RUN apt-get update && apt-get -y install python3.10 python3-pip git netcat
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver

CMD [ "python3" , "load_dataset.py" ]