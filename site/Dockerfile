FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

VOLUME /app

EXPOSE 8000 8501

RUN echo '#!/bin/bash\n\
uvicorn backend:app --host 0.0.0.0 --port 8000 &\n\
streamlit run frontend.py\n\
' > start.sh && chmod +x start.sh

CMD ["./start.sh"]