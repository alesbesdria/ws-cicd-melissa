
FROM python:3.12-slim

# TODO 1 : associer l'image au dépôt GitHub
LABEL org.opencontainers.image.source="https://github.com/alesbesdria/ws-cicd-melissa"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# TODO 2 : définir la version de l'application
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

# TODO 3 : exécuter l'application avec un utilisateur non-root
RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
