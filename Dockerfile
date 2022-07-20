FROM python:3.8.13

RUN apt-get update

WORKDIR /code
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .

#CMD ["python", "run.py"]
CMD ["flask", "run"]