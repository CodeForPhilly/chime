FROM python:3.7.7-slim-buster

COPY .streamlit ~/

COPY ./requirements.txt /app/requirements.txt
COPY ./README.md /app/README.md
COPY ./setup.py /app/setup.py
RUN mkdir /app/src

WORKDIR /app

RUN pip install -q -r requirements.txt

COPY . ./

CMD ["streamlit", "run", "src/app.py"]
