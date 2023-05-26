FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend
RUN pip install --upgrade pip
ENV FLASK_APP=app:app
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . ./

CMD ./wait-for-it.sh -t 70 db:3306 -- gunicorn --bind 0.0.0.0:5001 app:app --reload
