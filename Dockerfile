FROM python:3.6

ENV PYTHONUNBUFFERED=1

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . ./id_mapper
WORKDIR id_mapper

ENV PYTHONPATH $PYTHONPATH:/id_mapper

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7000", "-t", "150", "-k", "aiohttp.worker.GunicornWebWorker", "id_mapper.app:app"]
