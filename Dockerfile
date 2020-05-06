FROM python:3.7.7-slim-buster
ENV PARAMETERS=./defaults/webapp.cfg
ENV ELASTIC_APM_ENABLED false
ENV ELASTIC_APM_SERVICE_NAME chime_local
ENV ELASTIC_APM_SERVER_URL http://apm-server:8200
WORKDIR /app
COPY README.md .
COPY setup.cfg .
COPY setup.py .
COPY MANIFEST.in .
COPY .streamlit .streamlit
COPY defaults defaults
COPY src src
COPY st_app.py st_app.py
RUN pip install -q .

CMD ["streamlit", "run", "st_app.py"]

