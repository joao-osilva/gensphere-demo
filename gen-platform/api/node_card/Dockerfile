FROM python:3.11

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt -v

CMD ["uvicorn", "node_card:app", "--host", "0.0.0.0", "--port", "8000"]
