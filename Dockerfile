FROM python:3.7.7-slim-buster
ENV PARAMETERS=./defaults/webapp.cfg
WORKDIR /app
RUN mkdir /app
# Creating an empty src dir is a (hopefully) temporary hack to improve layer caching and speed up image builds
# todo fix once the Pipfile, setup.py, requirements.txt, pyprojec.toml build/dist story is figured out
RUN mkdir /src
COPY README.md .
COPY setup.cfg .
COPY setup.py .
COPY .streamlit .streamlit
COPY defaults defaults
COPY src src
RUN pip install -q .

CMD ["streamlit", "run", "src/app.py"]

