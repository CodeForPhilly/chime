FROM python:3.7.7-slim-buster

COPY .streamlit ~/

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -q -r requirements.txt

COPY . ./

ARG BUILD_TIME
ENV BUILD_TIME=$BUILD_TIME
RUN echo $BUILD_TIME

CMD ["streamlit", "run", "src/app.py"]
