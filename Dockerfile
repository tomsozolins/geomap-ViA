FROM python:3.9-slim-buster

ADD geomap.py .
ADD oracle.py .

RUN pip install --no-cache-dir pyzabbix
RUN pip install --no-cache-dir loguru
RUN pip install --no-cache-dir httpx

CMD [ "python", "./geomap.py"]
