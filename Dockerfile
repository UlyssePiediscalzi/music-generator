FROM python:3.8.6-buster
COPY api /api
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.simple:app --host 0.0.0.0
