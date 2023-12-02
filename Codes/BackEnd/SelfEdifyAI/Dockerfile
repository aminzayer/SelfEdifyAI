FROM python:3.11-slim as build
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirements.txt .
COPY . .
EXPOSE 8000
RUN pip install pipenv
RUN pipenv install -r requirements.txt
CMD ["pipenv", "run","python","manage.py","runserver","0:8000"]
