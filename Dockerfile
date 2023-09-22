FROM python:3.12-rc-alpine
VOLUME "/app-data"
WORKDIR /app
COPY /models /app/models
COPY /routers /app/routers
COPY /main.py /app/main.py
COPY /requirements.txt /app
RUN pip install -r /app/requirements.txt
EXPOSE 8080/tcp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
