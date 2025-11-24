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

# Делаем entrypoint.sh исполняемым
RUN chmod +x ./entrypoint.sh

# Запускаем через наш скрипт
CMD ["bash", "./entrypoint.sh"]
