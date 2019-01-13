FROM python:3.6

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY log_parser.py /app
CMD python log_parser.py
