FROM python:3.12.3

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["wait-for-it", "--service", "source_db:1521", "--service", "db:5432", "--", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
