FROM python:3.11-slim-bookworm
WORKDIR /app
COPY /models /app/models
COPY /routers /app/routers
COPY /main.py /app/main.py
COPY /requirements.txt /app
RUN pip install -r /app/requirements.txt
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y wget && \
    wget -c https://www.sqlite.org/2023/sqlite-autoconf-3430100.tar.gz && \
    mkdir SQLite && \
    cd SQLite && \
    tar xvfz ../sqlite-autoconf-3430100.tar.gz && \
    cd sqlite-autoconf-3430100 && \
    ./configure && \
    make && \
    make install

EXPOSE 8080/tcp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
