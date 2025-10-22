from fastapi import FastAPI
import os
import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz
import asyncio

app = FastAPI()

# ===== Função para enviar mensagem =====
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
        print("✅ Mensagem enviada com sucesso:", data)
    except Exception as e:
        print("❌ Erro ao enviar mensagem:", str(e))

# ===== Função de pinger =====
async def pinger():
    ping_url = os.getenv("PING_URL")
    if not ping_url:
        print("⚠️ Variável PING_URL não definida — pinger desativado.")
        return
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(ping_url)
        print(f"🔁 Pinger executado — status {r.status_code}")
    except Exception as e:
        print("❌ Erro no pinger:", e)

# ===== Inicializar agendador =====
scheduler = BackgroundScheduler(timezone=pytz.timezone("America/Sao_Paulo"))

# Enviar mensagem todo dia às 6h da manhã (horário de Brasília)
scheduler.add_job(
    lambda: asyncio.create_task(enviar_mensagem()),
    CronTrigger(hour=6, minute=0)
)

# Executar pinger a cada 5 minutos
scheduler.add_job(
    lambda: asyncio.create_task(pinger()),
    IntervalTrigger(minutes=5)
)

scheduler.start()

# ===== Rotas FastAPI =====
@app.get("/")
async def root():
    return {"status": "ok", "mensagem": "Servidor ativo e cron funcionando."}
