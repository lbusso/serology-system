# Dockerfile
FROM python:3.11-slim

# Opcional: mejora builds
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Paquetes básicos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requisitos primero (cache de capas)
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Código
COPY . /app/

# Puerto interno de Django
EXPOSE 8000

# Comando por defecto (dev)
# Ajusta "AnalisysSystem" por tu settings si tenés DJANGO_SETTINGS_MODULE custom
CMD ["bash", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
