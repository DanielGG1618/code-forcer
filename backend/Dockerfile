FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8000

ENV DB_CONNECTION_STRING="/db/students.db"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
