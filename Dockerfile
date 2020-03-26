FROM python:3.7.7-slim-buster

COPY .streamlit ~/

COPY ./README.md /app/README.md
COPY ./setup.py /app/setup.py
RUN mkdir /app/src

WORKDIR /app

RUN pip install -q .

COPY . ./

CMD ["streamlit", "run", "src/app.py"]
