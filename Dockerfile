FROM python:3.10.4
COPY requirements.txt .
RUN pip install -r requirements.txt

