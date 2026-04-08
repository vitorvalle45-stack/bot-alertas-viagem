"""
Configuracoes do Bot de Alertas de Viagem
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
PREMIUM_CHANNEL_ID = os.getenv("TELEGRAM_PREMIUM_CHANNEL_ID", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Whitelist VIP - Premium permanente sem precisar pagar
# Adicione o Telegram ID (numero) de cada usuario VIP
VIP_WHITELIST = {
    ADMIN_ID,  # Admin sempre eh VIP
    # Antonio Bosco: adicionar ID aqui quando disponivel
}

# RSS Feeds para monitorar (organizados por regiao)
RSS_FEEDS = [
    # === BRASIL ===
    {"nome": "Melhores Destinos", "url": "https://www.melhoresdestinos.com.br/feed", "tipo": "brasil", "regiao": "BR"},
    # Passagens Imperdiveis - REMOVIDO (feed retorna 403/404)
    # Melhores Destinos Promocoes - REMOVIDO (404, URL nao existe mais)
    # Voopter Blog - REMOVIDO (404, feed removido)
    {"nome": "MaxMilhas Blog", "url": "https://www.maxmilhas.com.br/blog/feed", "tipo": "brasil", "regiao": "BR"},
    {"nome": "Google News Passagens BR", "url": "https://news.google.com/rss/search?q=passagem+aerea+promocao+OR+barata+OR+desconto&hl=pt-BR&gl=BR&ceid=BR:pt-419", "tipo": "brasil", "regiao": "BR"},
    {"nome": "Google News Voos Baratos BR", "url": "https://news.google.com/rss/search?q=voo+barato+OR+%22passagem+barata%22+OR+%22milhas+aereas%22&hl=pt-BR&gl=BR&ceid=BR:pt-419", "tipo": "brasil", "regiao": "BR"},
    # === ERROR FARES (PREMIUM EXCLUSIVO) ===
    # Secret Flying Error Fares - REMOVIDO (403, retorna HTML em vez de RSS)
    {"nome": "Google News Error Fares", "url": "https://news.google.com/rss/search?q=%22error+fare%22+OR+%22mistake+fare%22+OR+%22glitch+fare%22+OR+%22fuel+dump%22&hl=en-US&gl=US&ceid=US:en", "tipo": "error_fare", "regiao": "ALL"},
    {"nome": "Google News Error Fares PT", "url": "https://news.google.com/rss/search?q=%22erro+tarifa%22+OR+%22passagem+erro%22+OR+%22bug+passagem%22+OR+%22glitch+aereo%22&hl=pt-BR&gl=BR&ceid=BR:pt-419", "tipo": "error_fare", "regiao": "BR"},
    # === INTERNACIONAL / GLOBAL ===
    # Secret Flying - REMOVIDO (403, retorna HTML em vez de RSS)
    {"nome": "Fly4Free", "url": "https://www.fly4free.com/feed/", "tipo": "internacional", "regiao": "ALL"},
    {"nome": "FareDealAlert", "url": "https://faredealalert.com/feed/", "tipo": "internacional", "regiao": "US"},
    {"nome": "The Flight Deal", "url": "https://www.theflightdeal.com/feed/", "tipo": "internacional", "regiao": "US"},
    # === UK / EUROPA ===
    {"nome": "HolidayPirates", "url": "https://www.holidaypirates.com/feed", "tipo": "internacional", "regiao": "UK"},
    {"nome": "TravelFree", "url": "https://travelfree.info/feed/", "tipo": "internacional", "regiao": "EU"},
    {"nome": "Travel-Dealz", "url": "https://travel-dealz.com/feed/", "tipo": "internacional", "regiao": "EU"},
    # === EUA ===
    {"nome": "TravelPirates", "url": "https://www.travelpirates.com/feed", "tipo": "internacional", "regiao": "US"},
    {"nome": "Thrifty Traveler", "url": "https://thriftytraveler.com/feed/", "tipo": "internacional", "regiao": "US"},
    {"nome": "The Points Guy", "url": "https://thepointsguy.com/feed/", "tipo": "internacional", "regiao": "US"},
    {"nome": "One Mile at a Time", "url": "https://onemileatatime.com/feed/", "tipo": "internacional", "regiao": "US"},
    {"nome": "Travel Off Path", "url": "https://www.traveloffpath.com/feed/", "tipo": "internacional", "regiao": "US"},
    # === AUSTRALIA ===
    {"nome": "I Know The Pilot", "url": "https://iknowthepilot.com.au/feed", "tipo": "internacional", "regiao": "AU"},
    # === CANADA ===
    {"nome": "Next Departure", "url": "https://nextdeparture.ca/feed/", "tipo": "internacional", "regiao": "CA"},
    # === MEXICO / LATAM ===
    # Guru de Viaje - REMOVIDO (retorna HTML/Next.js, sem RSS)
    # Promodescuentos Vuelos - REMOVIDO (403 Forbidden)
    {"nome": "VuelaX", "url": "https://www.vuelax.com/feed/", "tipo": "internacional", "regiao": "MX"},
    {"nome": "Google News Vuelos MX", "url": "https://news.google.com/rss/search?q=vuelo+barato+OR+%22oferta+vuelo%22+OR+%22error+fare%22&hl=es-419&gl=MX&ceid=MX:es-419", "tipo": "internacional", "regiao": "MX"},
    # === ALEMANHA ===
    {"nome": "Urlaubspiraten", "url": "https://www.urlaubspiraten.de/feed", "tipo": "internacional", "regiao": "EU"},
    # === ITALIA ===
    {"nome": "Piratinviaggio", "url": "https://www.piratinviaggio.it/feed", "tipo": "internacional", "regiao": "EU"},
    # === ESPANHA ===
    {"nome": "ViajerosPiratas", "url": "https://www.viajerospiratas.es/feed", "tipo": "internacional", "regiao": "EU"},
    # === HOLANDA ===
    {"nome": "TicketSpy", "url": "https://ticketspy.nl/feed/", "tipo": "internacional", "regiao": "EU"},
    # === ASIA ===
    {"nome": "Traicy", "url": "https://en.traicy.com/feed", "tipo": "internacional", "regiao": "JP"},
    # === ERROR FARES EXTRA ===
    {"nome": "Google News Fuel Dump", "url": "https://news.google.com/rss/search?q=%22fuel+dump%22+airline+OR+flight&hl=en-US&gl=US&ceid=US:en", "tipo": "error_fare", "regiao": "ALL"},
    {"nome": "FlyerTalk Deals", "url": "https://www.flyertalk.com/forum/external.php?type=RSS2&forumids=372", "tipo": "error_fare", "regiao": "ALL"},
]

# Cidades/aeroportos por regiao (para detectar origem dos deals)
CIDADES_POR_REGIAO = {
    "BR": [
        "sao paulo", "gru", "guarulhos", "cgh", "congonhas",
        "rio de janeiro", "rio", "gig", "galeao", "sdu",
        "brasilia", "bsb", "belo horizonte", "cnf",
        "curitiba", "cwb", "porto alegre", "poa",
        "salvador", "ssa", "recife", "rec", "fortaleza", "for",
        "manaus", "mao", "belem", "bel", "florianopolis", "fln",
        "natal", "nat", "campinas", "vcp", "viracopos",
        "brazil", "brasil",
    ],
    "US": [
        "new york", "jfk", "ewr", "lga", "newark",
        "los angeles", "lax", "san francisco", "sfo",
        "chicago", "ord", "mdw", "miami", "mia", "fll",
        "boston", "bos", "dallas", "dfw", "houston", "iah",
        "atlanta", "atl", "seattle", "sea", "denver", "den",
        "orlando", "mco", "washington", "iad", "dca",
        "philadelphia", "phl", "phoenix", "phx",
        "united states", "u.s.", "usa",
    ],
    "UK": [
        "london", "lhr", "heathrow", "lgw", "gatwick", "stn", "stansted", "ltn", "luton",
        "manchester", "man", "birmingham", "bhx",
        "edinburgh", "edi", "glasgow", "gla", "bristol", "brs",
        "liverpool", "lpl", "newcastle", "ncl", "leeds", "lba",
        "united kingdom", "britain", "england", "scotland", "wales", "uk",
    ],
    "EU": [
        "paris", "cdg", "ory", "amsterdam", "ams", "schiphol",
        "frankfurt", "fra", "munich", "muc", "berlin", "ber",
        "rome", "fco", "fiumicino", "milan", "mxp", "linate",
        "madrid", "mad", "barcelona", "bcn",
        "lisbon", "lis", "porto", "opo",
        "vienna", "vie", "brussels", "bru",
        "dublin", "dub", "copenhagen", "cph",
        "stockholm", "arn", "oslo", "osl",
        "helsinki", "hel", "prague", "prg",
        "warsaw", "waw", "budapest", "bud",
        "athens", "ath", "europe",
    ],
    "CH": [
        "zurich", "zrh", "geneva", "gva", "basel", "bsl",
        "bern", "switzerland", "swiss", "suica",
    ],
    "AU": [
        "sydney", "syd", "melbourne", "mel", "brisbane", "bne",
        "perth", "per", "adelaide", "adl", "gold coast", "ool",
        "canberra", "cbr", "cairns", "cns", "darwin", "drw",
        "australia", "aussie",
    ],
    "AE": [
        "dubai", "dxb", "abu dhabi", "auh",
        "sharjah", "shj", "uae", "emirates",
    ],
    "JP": [
        "tokyo", "nrt", "narita", "hnd", "haneda",
        "osaka", "kix", "kansai", "nagoya", "ngo",
        "fukuoka", "fuk", "sapporo", "cts",
        "japan", "japao",
    ],
    "KR": [
        "seoul", "icn", "incheon", "gmp", "gimpo",
        "busan", "pus", "jeju", "cju",
        "korea", "south korea", "coreia",
    ],
    "CA": [
        "toronto", "yyz", "pearson", "vancouver", "yvr",
        "montreal", "yul", "calgary", "yyc",
        "ottawa", "yow", "edmonton", "yeg",
        "winnipeg", "ywg", "halifax", "yhz",
        "canada", "canadian",
    ],
    "DK": ["copenhagen", "cph", "denmark", "danish", "dinamarca"],
    "SE": ["stockholm", "arn", "gothenburg", "got", "sweden", "swedish", "suecia"],
    "NO": ["oslo", "osl", "bergen", "bgo", "norway", "norwegian", "noruega"],
    "MX": [
        "mexico city", "mex", "cancun", "cun",
        "guadalajara", "gdl", "monterrey", "mty",
        "tijuana", "tij", "cabo", "sjd",
        "mexico", "mexican",
    ],
}

# Atalho para manter compatibilidade
CIDADES_BR = CIDADES_POR_REGIAO["BR"]

# Destinos populares (global - usados para bonus de score)
DESTINOS_POPULARES = [
    "lisboa", "lisbon", "porto", "portugal",
    "paris", "france", "london", "londres",
    "madrid", "barcelona", "spain",
    "rome", "roma", "milan", "italy", "italia",
    "miami", "orlando", "new york", "los angeles",
    "buenos aires", "argentina",
    "santiago", "chile", "cancun",
    "dubai", "tokyo", "japan",
    "amsterdam", "berlin", "munich",
    "sydney", "melbourne", "auckland",
    "bangkok", "bali", "singapore",
    "seoul", "taipei", "hong kong",
    "cairo", "cape town", "marrakech",
    "reykjavik", "iceland",
    "hawaii", "honolulu", "maldives",
    "phuket", "santorini", "mykonos",
]

# Intervalo de verificacao dos feeds (em segundos)
INTERVALO_CHECAGEM = 15 * 60  # 15 minutos

# Horario do alerta diario (hora, minuto) - horario de Brasilia
HORARIO_ALERTA_DIARIO = (6, 0)

# Maximo de deals por checagem
MAX_DEALS_POR_CHECAGEM = 10

# Score minimo para enviar um deal (filtra deals irrelevantes)
# Deals saindo do Brasil tem score 10+, destinos populares 5+
# Isso garante que so deals relevantes pro publico BR sejam enviados
SCORE_MINIMO = 3

# Arquivo para controlar deals ja enviados
ARQUIVO_DEALS_ENVIADOS = "deals_enviados.json"
