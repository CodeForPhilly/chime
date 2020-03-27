FROM python:3.7.7-slim-buster
RUN mkdir /app
WORKDIR /app
COPY .streamlit ~/
COPY README.md .
COPY setup.py .
COPY settings.cfg .
COPY src src
RUN pip install -q .

CMD ["streamlit", "run", "src/app.py"]
