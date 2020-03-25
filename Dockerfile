FROM python:3.7.7-slim-buster

COPY .streamlit ~/

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -q -r requirements.txt

COPY src src 

EXPOSE 8050

# CMD ["streamlit", "run", "src/app.py"]
CMD gunicorn src.dash_app:server --bind 0.0.0.0:8050
#CMD ["sh"]
