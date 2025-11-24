FROM python:3.12.0

ENV HOME=/home/payments \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -r payments \
 && useradd -r -g payments payments

WORKDIR $HOME

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip cache purge

COPY . .

RUN chown -R payments:payments .

USER payments

CMD bash -c "\
  python manage.py migrate --noinput && \
  python manage.py createsuperuser --noinput \
    --username \"$DJANGO_SUPERUSER_USERNAME\" \
    --email \"$DJANGO_SUPERUSER_EMAIL\" || true && \
  python manage.py runserver 0.0.0.0:$PORT --noreload \
"