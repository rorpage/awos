FROM python:3.12.1-alpine

WORKDIR /awos

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY script.sh .
RUN chmod a+x script.sh

COPY metar_gg.py .
COPY tokenizer.py .
COPY utils.py .

COPY script.py .

CMD ./script.sh
