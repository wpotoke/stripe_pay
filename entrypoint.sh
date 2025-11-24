#!/usr/bin/env bash
set -e

echo "==> Running migrations..."
python manage.py migrate --noinput

# Создаём суперюзера, только если заданы username и password
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "==> Creating superuser $DJANGO_SUPERUSER_USERNAME (if not exists)..."
  python manage.py createsuperuser \
    --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
  || true
else
  echo "==> DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set, skipping superuser creation."
fi

echo "==> Starting Django dev server..."
python manage.py runserver 0.0.0.0:${PORT:-8000} --noreload
