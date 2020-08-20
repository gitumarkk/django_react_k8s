FROM python:3.6.11-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /django_react_k8s
WORKDIR /django_react_k8s
RUN pip install --upgrade pip
COPY requirements.txt /django_react_k8s/
RUN pip install -r requirements.txt
COPY . /django_react_k8s/
CMD python manage.py runserver 0.0.0.0:8000
