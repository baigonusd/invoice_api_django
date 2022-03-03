FROM python:3.8.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /home/invoice
RUN pip3 install -r /home/invoice/requirements.txt

WORKDIR /home/invoice