FROM python:3.12.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install cryptography

EXPOSE 5000

CMD ["python", "app.py"]