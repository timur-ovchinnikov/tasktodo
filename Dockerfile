FROM python:3.11

# Устанавливаем postgresql-client
RUN apt-get update && \
    apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
