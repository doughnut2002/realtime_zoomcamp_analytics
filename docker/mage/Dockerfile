FROM python:3.9.1

RUN apt-get install wget


WORKDIR /app

COPY /workspaces/realtime_zoomcamp_analytics/Batch Pipeline /workspaces/realtime_zoomcamp_analytics/Batch Pipeline
COPY ./Data/green_tripdata_2021-09.csv /app/green_tripdata_2021-09.csv

ENTRYPOINT [ "python","pipe.py" ]