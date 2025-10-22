from fastapi import FastAPI
import os
import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

app = FastAPI()

# Função para enviar a mensagem
async def enviar_mensagem():
    instance_id = os.getenv("INSTANCE_ID")
    token = os.getenv("TOKEN")
    phone = os.getenv("PHONE")
    mensagem = os.getenv("MENSAGEM")

    url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-text"
    payload = {"phone": phone, "message": mensagem}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            data = response.json()
        print("Mensagem enviada com sucesso:", data)
    except Exception as e:
        print("Erro ao enviar mensagem:", str(e))

# Agendando o envio todo dia às 6h (horário de Brasília)
scheduler = BackgroundScheduler(timezone=pytz.timezone("America/Sao_Paulo"))
scheduler.add_job(
    lambda: app.loop.create_task(enviar_mensagem()),  # cria task assíncrona
    CronTrigger(hour=6, minute=0)
)
scheduler.start()

@app.get("/")
def root():
    return {"status": "Servidor rodando e cron ativo"}

