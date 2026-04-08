"""
Sistema de traducoes PT-BR / EN
"""

TEXTOS = {
    # /start
    "welcome": {
        "pt": (
            "Ola, {nome}! \u2708\uFE0F\n\n"
            "Bem-vindo ao <b>Bot de Alertas de Viagem!</b>\n\n"
            "Eu monitoro dezenas de fontes 24/7 procurando:\n"
            "\u2022 \U0001F525 Passagens aereas com precos absurdos\n"
            "\u2022 \U0001F6A8 Error fares (erros de preco das cias aereas)\n"
            "\u2022 \U0001F4B0 Promocoes relampago de hospedagem\n\n"
            "\U0001F30D <b>Primeiro, escolha sua regiao:</b>\n"
            "(isso define a moeda dos precos)"
        ),
        "en": (
            "Hello, {nome}! \u2708\uFE0F\n\n"
            "Welcome to the <b>Travel Deals Alert Bot!</b>\n\n"
            "I monitor dozens of sources 24/7 looking for:\n"
            "\u2022 \U0001F525 Absurdly cheap flights\n"
            "\u2022 \U0001F6A8 Error fares (airline pricing mistakes)\n"
            "\u2022 \U0001F4B0 Flash hotel deals\n\n"
            "\U0001F30D <b>First, choose your region:</b>\n"
            "(this sets your currency)"
        ),
    },

    # Regiao configurada
    "regiao_ok": {
        "pt": (
            "\u2705 <b>Regiao configurada!</b>\n\n"
            "{flag} <b>{regiao}</b>\n"
            "\U0001F4B0 Moeda: <b>{simbolo} ({moeda})</b>\n\n"
            "Todos os precos serao exibidos em <b>{simbolo}</b>!\n\n"
            "<b>Comandos:</b>\n"
            "/buscar - Ver deals agora\n"
            "/moeda - Trocar moeda/regiao\n"
            "/ajuda - Como usar\n"
            "/stats - Estatisticas\n\n"
            "\U0001F514 Voce recebera alertas automaticos a cada 15 minutos!"
        ),
        "en": (
            "\u2705 <b>Region set!</b>\n\n"
            "{flag} <b>{regiao}</b>\n"
            "\U0001F4B0 Currency: <b>{simbolo} ({moeda})</b>\n\n"
            "All prices will be shown in <b>{simbolo}</b>!\n\n"
            "<b>Commands:</b>\n"
            "/buscar - See deals now\n"
            "/moeda - Change currency/region\n"
            "/help - How to use\n"
            "/stats - Statistics\n\n"
            "\U0001F514 You will receive automatic alerts every 15 minutes!"
        ),
    },

    # /moeda
    "escolha_moeda": {
        "pt": "\U0001F30D <b>Escolha sua regiao/moeda:</b>",
        "en": "\U0001F30D <b>Choose your region/currency:</b>",
    },

    # /ajuda
    "ajuda": {
        "pt": (
            "\U0001F4D6 <b>COMO USAR O BOT</b>\n\n"
            "<b>1. Escolha sua regiao</b>\n"
            "Use /moeda para definir sua moeda.\n\n"
            "<b>2. Ative as notificacoes</b>\n"
            "Assim voce nao perde nenhum error fare!\n\n"
            "<b>3. Aja rapido!</b>\n"
            "Error fares duram de 30 minutos a 2 horas.\n"
            "Quando receber um alerta, corra para comprar!\n\n"
            "<b>4. Dicas importantes:</b>\n"
            "\u2022 A maioria das cias aereas honra error fares (~85%)\n"
            "\u2022 Compre PRIMEIRO, planeje DEPOIS\n"
            "\u2022 Nao divulgue o erro antes de comprar\n"
            "\u2022 Use aba anonima para precos mais baixos\n\n"
            "<b>Duvidas?</b> Fale com o admin do canal!"
        ),
        "en": (
            "\U0001F4D6 <b>HOW TO USE THE BOT</b>\n\n"
            "<b>1. Choose your region</b>\n"
            "Use /moeda to set your currency.\n\n"
            "<b>2. Turn on notifications</b>\n"
            "So you never miss an error fare!\n\n"
            "<b>3. Act fast!</b>\n"
            "Error fares last 30 minutes to 2 hours.\n"
            "When you get an alert, buy immediately!\n\n"
            "<b>4. Important tips:</b>\n"
            "\u2022 Most airlines honor error fares (~85%)\n"
            "\u2022 Buy FIRST, plan LATER\n"
            "\u2022 Don't share the error before buying\n"
            "\u2022 Use incognito mode for lower prices\n\n"
            "<b>Questions?</b> Contact the channel admin!"
        ),
    },

    # /buscar
    "buscando": {
        "pt": "\U0001F50D Buscando deals agora... Aguarde!",
        "en": "\U0001F50D Searching for deals... Please wait!",
    },
    "nenhum_deal": {
        "pt": (
            "\U0001F614 Nenhum deal novo encontrado agora.\n"
            "Os feeds sao atualizados constantemente. Tente novamente em alguns minutos!"
        ),
        "en": (
            "\U0001F614 No new deals found right now.\n"
            "Feeds are constantly updated. Try again in a few minutes!"
        ),
    },
    "deals_encontrados": {
        "pt": "\u2705 Encontrei {n} deal(s)!\n",
        "en": "\u2705 Found {n} deal(s)!\n",
    },

    # /stats
    "stats": {
        "pt": (
            "\U0001F4CA <b>ESTATISTICAS DO BOT</b>\n\n"
            "\U0001F4E8 Deals enviados (ultimos 7 dias): <b>{total}</b>\n"
            "\U0001F4E1 Feeds monitorados: <b>{feeds}</b>\n"
            "\u23F0 Intervalo de checagem: <b>{intervalo} minutos</b>\n"
        ),
        "en": (
            "\U0001F4CA <b>BOT STATISTICS</b>\n\n"
            "\U0001F4E8 Deals sent (last 7 days): <b>{total}</b>\n"
            "\U0001F4E1 Feeds monitored: <b>{feeds}</b>\n"
            "\u23F0 Check interval: <b>{intervalo} minutes</b>\n"
        ),
    },

    # Alertas de deals
    "alerta_passagem": {
        "pt": "ALERTA DE PASSAGEM",
        "en": "FLIGHT DEAL ALERT",
    },
    "error_fare": {
        "pt": "POSSIVEL ERROR FARE!",
        "en": "POSSIBLE ERROR FARE!",
    },
    "ver_deal": {
        "pt": "VER DEAL COMPLETO",
        "en": "VIEW FULL DEAL",
    },
    "ativar_notif": {
        "pt": "Ative as notificacoes para nao perder nenhum alerta!",
        "en": "Turn on notifications so you never miss a deal!",
    },
    "fonte": {
        "pt": "Fonte",
        "en": "Source",
    },

    # Alerta diario
    "bom_dia": {
        "pt": (
            "\u2615 <b>BOM DIA! Alerta Diario de Viagem</b>\n\n"
            "\U0001F50D Estou monitorando os melhores deals para voce!\n\n"
            "Fique atento \u2014 error fares podem aparecer a qualquer momento.\n"
            "\U0001F514 Mantenha as notificacoes ativadas para nao perder nada!\n\n"
            "\U0001F4AA Boas economias hoje!"
        ),
        "en": (
            "\u2615 <b>GOOD MORNING! Daily Travel Alert</b>\n\n"
            "\U0001F50D I'm monitoring the best deals for you!\n\n"
            "Stay alert \u2014 error fares can appear at any time.\n"
            "\U0001F514 Keep notifications on so you don't miss anything!\n\n"
            "\U0001F4AA Happy savings today!"
        ),
    },

    # Botoes
    "entrar_canal": {
        "pt": "\U0001F4E2 Entrar no Canal de Alertas",
        "en": "\U0001F4E2 Join the Alerts Channel",
    },
    "compartilhar": {
        "pt": "\u2764\uFE0F Compartilhar com amigos",
        "en": "\u2764\uFE0F Share with friends",
    },
    "share_text": {
        "pt": "Confira esse bot de passagens baratas!",
        "en": "Check out this cheap flights bot!",
    },

    # Upsell Premium (quando free tenta /buscar)
    "buscar_premium_only": {
        "pt": (
            "\U0001F451 <b>Comando exclusivo para membros Premium!</b>\n\n"
            "\U0001F6A8 Membros Premium recebem:\n"
            "\u2022 \U0001F525 Error fares exclusivos em tempo real\n"
            "\u2022 \u2708\uFE0F Deals personalizados no PV\n"
            "\u2022 \U0001F4B0 Alertas automaticos 24/7\n"
            "\u2022 \u26A1 Precos ate 90% abaixo do normal\n\n"
            "\U0001F4A1 <b>Um unico error fare ja paga 35 anos de Premium!</b>\n\n"
            "\U0001F449 <a href=\"https://buy.stripe.com/28E3cp7GV5WQctA7kf6J200\">QUERO SER PREMIUM AGORA</a>"
        ),
        "en": (
            "\U0001F451 <b>This command is Premium-only!</b>\n\n"
            "\U0001F6A8 Premium members get:\n"
            "\u2022 \U0001F525 Exclusive real-time error fares\n"
            "\u2022 \u2708\uFE0F Personalized deals in DM\n"
            "\u2022 \U0001F4B0 24/7 automatic alerts\n"
            "\u2022 \u26A1 Prices up to 90% below normal\n\n"
            "\U0001F4A1 <b>One single error fare pays for 35 years of Premium!</b>\n\n"
            "\U0001F449 <a href=\"https://buy.stripe.com/28E3cp7GV5WQctA7kf6J200\">BECOME PREMIUM NOW</a>"
        ),
    },

    # Admin
    "admin_restrito": {
        "pt": "\u274C Comando restrito ao admin.",
        "en": "\u274C Admin only command.",
    },
    "enviando_canal": {
        "pt": "\U0001F4E4 Buscando e enviando deals para o canal...",
        "en": "\U0001F4E4 Searching and sending deals to channel...",
    },
    "nenhum_deal_enviar": {
        "pt": "Nenhum deal novo para enviar.",
        "en": "No new deals to send.",
    },
    "deals_enviados_canal": {
        "pt": "\u2705 {n} deal(s) enviado(s) para o canal!",
        "en": "\u2705 {n} deal(s) sent to the channel!",
    },
}

# Regioes que usam portugues
REGIOES_PT = {"BR"}

# Codigos de idioma do Telegram que mapeiam pra portugues
LANG_CODES_PT = {"pt", "pt-br", "pt_br"}


def detectar_idioma(language_code: str = "", regiao: str = "") -> str:
    """
    Detecta o idioma do usuario baseado em:
    1. Regiao selecionada (BR = pt)
    2. language_code do Telegram (pt, pt-br = pt)
    3. Fallback: en (ingles)
    """
    if regiao in REGIOES_PT:
        return "pt"

    if language_code:
        lang = language_code.lower().replace("-", "_")
        if lang in LANG_CODES_PT or lang.startswith("pt"):
            return "pt"

    return "en"


def t(chave: str, idioma: str = "en", **kwargs) -> str:
    """
    Retorna o texto traduzido.
    Uso: t("welcome", "pt", nome="Vitor")
    """
    textos = TEXTOS.get(chave, {})
    texto = textos.get(idioma, textos.get("en", f"[{chave}]"))
    if kwargs:
        texto = texto.format(**kwargs)
    return texto
