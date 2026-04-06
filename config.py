"""
Configuracoes do Bot de Alertas de Viagem
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# RSS Feeds para monitorar
RSS_FEEDS = [
    {
        "nome": "Secret Flying",
        "url": "https://www.secretflying.com/feed/",
        "tipo": "internacional",
    },
    {
        "nome": "Secret Flying - Error Fares",
        "url": "https://www.secretflying.com/errorfare/feed/",
        "tipo": "error_fare",
    },
    {
        "nome": "Fly4Free",
        "url": "https://www.fly4free.com/feed/",
        "tipo": "internacional",
    },
    {
        "nome": "The Flight Deal",
        "url": "https://www.theflightdeal.com/feed/",
        "tipo": "internacional",
    },
]

# Cidades brasileiras para filtrar deals relevantes
CIDADES_BR = [
    "sao paulo", "são paulo", "gru", "guarulhos", "cgh", "congonhas",
    "rio de janeiro", "rio", "gig", "galeao", "sdu", "santos dumont",
    "brasilia", "bsb", "belo horizonte", "cnf", "confins",
    "curitiba", "cwb", "porto alegre", "poa",
    "salvador", "ssa", "recife", "rec", "fortaleza", "for",
    "manaus", "mao", "belem", "bel", "florianopolis", "fln",
    "natal", "nat", "campinas", "vcp", "viracopos",
    "brazil", "brasil",
]

# Destinos populares para brasileiros
DESTINOS_POPULARES = [
    "lisboa", "lisbon", "porto", "portugal",
    "paris", "france", "franca",
    "london", "londres", "england",
    "madrid", "barcelona", "spain", "espanha",
    "rome", "roma", "milan", "milao", "italy", "italia",
    "miami", "orlando", "new york", "nova york", "los angeles",
    "buenos aires", "argentina",
    "santiago", "chile",
    "cancun", "mexico",
    "dubai",
    "tokyo", "toquio", "japan", "japao",
    "amsterdam", "amsterda",
    "berlin", "berlim", "germany", "alemanha",
]

# Intervalo de verificacao dos feeds (em segundos)
INTERVALO_CHECAGEM = 15 * 60  # 15 minutos

# Horario do alerta diario (hora, minuto) - horario de Brasilia
HORARIO_ALERTA_DIARIO = (6, 0)

# Maximo de deals por checagem
MAX_DEALS_POR_CHECAGEM = 5

# Arquivo para controlar deals ja enviados
ARQUIVO_DEALS_ENVIADOS = "deals_enviados.json"
