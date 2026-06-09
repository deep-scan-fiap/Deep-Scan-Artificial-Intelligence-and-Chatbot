FROM python:3.12-slim

WORKDIR /app

# Dependencias do sistema mínimas para sklearn/xgboost em python:slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY modelo_classificacao.pkl .
COPY modelo_regressao.pkl .

EXPOSE 5002

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5002", "app:app"]
