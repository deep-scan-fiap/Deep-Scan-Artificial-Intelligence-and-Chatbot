# DeepScan — Backend IA

API Flask que serve dois modelos de machine learning treinados a partir de dados oceânicos e sísmicos:

- **Classificação de risco de tsunami** (`modelo_classificacao.pkl`) — saída binária a partir de parâmetros de evento sísmico.
- **Regressão de temperatura do mar** (`modelo_regressao.pkl`) — temperatura prevista (°C) a partir de variáveis ambientais.

## Base URL

```
https://deepscan-ai.labs-lcs-server.com
```

## Endpoints

| Método | Path | Body (JSON) | Resposta |
|---|---|---|---|
| `GET` | `/` | — | `{ "status": "online", "projeto": "DeepScan", "endpoints": [...] }` |
| `POST` | `/predict/risco` | `{ "magnitude": float, "depth": float, "latitude": float, "longitude": float, "gap": float, "dmin": float, "sig": float }` | `{ "codigo": 0\|1, "risco": "Tsunami"\|"Sem Tsunami" }` |
| `POST` | `/predict/temperatura` | `{ "latitude": float, "longitude": float, "ph_level": float, "species_observed": int, "marine_heatwave": 0\|1 }` | `{ "temperatura_prevista": float, "unidade": "Celsius" }` |

Todos os endpoints de predição esperam `Content-Type: application/json`.

## Exemplos

```bash
# health check
curl https://deepscan-ai.labs-lcs-server.com/

# risco de tsunami
curl -X POST https://deepscan-ai.labs-lcs-server.com/predict/risco \
  -H "Content-Type: application/json" \
  -d '{"magnitude":7.5,"depth":10,"latitude":-30,"longitude":-70,"gap":50,"dmin":0.5,"sig":600}'
# → {"codigo":1,"risco":"Tsunami"}

# temperatura do mar
curl -X POST https://deepscan-ai.labs-lcs-server.com/predict/temperatura \
  -H "Content-Type: application/json" \
  -d '{"latitude":-23.5,"longitude":-46.6,"ph_level":8.1,"species_observed":15,"marine_heatwave":0}'
# → {"temperatura_prevista":29.11,"unidade":"Celsius"}
```

## CORS

Apenas requisições vindas de `https://deepscanfiap.vercel.app` são liberadas via `flask-cors`. Outras origens não recebem cabeçalhos `Access-Control-Allow-*` e são bloqueadas pelo browser.

## Stack

- Python 3.12, Flask 3.0, Gunicorn
- scikit-learn 1.5.2, joblib, NumPy, pandas
- Empacotado como imagem Docker (`Dockerfile` na raiz) e disparado pelo workflow `.github/workflows/deploy.yml` em runner self-hosted.
