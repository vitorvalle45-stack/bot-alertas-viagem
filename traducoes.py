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
        "es": "ALERTA DE VUELO",
        "fr": "ALERTE VOL",
        "de": "FLUG-DEAL ALARM",
        "it": "AVVISO VOLO",
        "ja": "\u2708\uFE0F \u822A\u7A7A\u5238\u30C7\u30A3\u30FC\u30EB\u901A\u77E5",
        "ko": "\u2708\uFE0F \uD56D\uACF5\uAD8C \uB51C \uC54C\uB9BC",
        "nl": "VLUCHT DEAL ALERT",
    },
    "error_fare": {
        "pt": "POSSIVEL ERROR FARE!",
        "en": "POSSIBLE ERROR FARE!",
        "es": "POSIBLE ERROR DE PRECIO!",
        "fr": "POSSIBLE ERREUR DE PRIX!",
        "de": "MOGLICHER PREISFEHLER!",
        "it": "POSSIBILE ERRORE DI PREZZO!",
        "ja": "\u4FA1\u683C\u30A8\u30E9\u30FC\u306E\u53EF\u80FD\u6027!",
        "ko": "\uAC00\uACA9 \uC624\uB958 \uBC1C\uACAC!",
        "nl": "MOGELIJKE PRIJSFOUT!",
    },
    "ver_deal": {
        "pt": "VER DEAL COMPLETO",
        "en": "VIEW FULL DEAL",
        "es": "VER OFERTA COMPLETA",
        "fr": "VOIR L'OFFRE",
        "de": "DEAL ANSEHEN",
        "it": "VEDI OFFERTA",
        "ja": "\u30C7\u30A3\u30FC\u30EB\u3092\u898B\u308B",
        "ko": "\uB51C \uBCF4\uAE30",
        "nl": "DEAL BEKIJKEN",
    },
    "ativar_notif": {
        "pt": "Ative as notificacoes para nao perder nenhum alerta!",
        "en": "Turn on notifications so you never miss a deal!",
        "es": "Activa las notificaciones para no perderte ninguna oferta!",
        "fr": "Activez les notifications pour ne rater aucune offre!",
        "de": "Benachrichtigungen aktivieren, um kein Angebot zu verpassen!",
        "it": "Attiva le notifiche per non perdere nessuna offerta!",
        "ja": "\u901A\u77E5\u3092\u30AA\u30F3\u306B\u3057\u3066\u304F\u3060\u3055\u3044\uFF01",
        "ko": "\uC54C\uB9BC\uC744 \uCF1C\uC138\uC694!",
        "nl": "Zet meldingen aan zodat je geen deal mist!",
    },
    "fonte": {
        "pt": "Fonte",
        "en": "Source",
        "es": "Fuente",
        "fr": "Source",
        "de": "Quelle",
        "it": "Fonte",
        "ja": "\u30BD\u30FC\u30B9",
        "ko": "\uCD9C\uCC98",
        "nl": "Bron",
    },
    # Error fare - mensagens escandalosas
    "glitch_titulo": {
        "pt": "ERRO DE PRECO DETECTADO!",
        "en": "PRICE GLITCH DETECTED!",
        "es": "ERROR DE PRECIO DETECTADO!",
        "fr": "ERREUR DE PRIX DETECTEE!",
        "de": "PREISFEHLER ENTDECKT!",
        "it": "ERRORE DI PREZZO RILEVATO!",
        "ja": "\u4FA1\u683C\u30A8\u30E9\u30FC\u767A\u898B\uFF01",
        "ko": "\uAC00\uACA9 \uC624\uB958 \uBC1C\uACAC!",
        "nl": "PRIJSFOUT ONTDEKT!",
    },
    "glitch_subtitulo": {
        "pt": "PRICE GLITCH! A CIA AEREA ERROU O PRECO!",
        "en": "AIRLINE PRICING ERROR!",
        "es": "LA AEROLINEA COMETIO UN ERROR DE PRECIO!",
        "fr": "LA COMPAGNIE AERIENNE A FAIT UNE ERREUR DE PRIX!",
        "de": "DIE AIRLINE HAT EINEN PREISFEHLER GEMACHT!",
        "it": "LA COMPAGNIA AEREA HA SBAGLIATO IL PREZZO!",
        "ja": "\u822A\u7A7A\u4F1A\u793E\u304C\u4FA1\u683C\u3092\u9593\u9055\u3048\u305F\uFF01",
        "ko": "\uD56D\uACF5\uC0AC \uAC00\uACA9 \uC624\uB958!",
        "nl": "DE LUCHTVAARTMAATSCHAPPIJ HEEFT EEN PRIJSFOUT GEMAAKT!",
    },
    "glitch_urgencia1": {
        "pt": "Esse erro pode ser corrigido A QUALQUER MOMENTO!",
        "en": "This glitch can be fixed ANY SECOND!",
        "es": "Este error puede corregirse EN CUALQUIER MOMENTO!",
        "fr": "Cette erreur peut etre corrigee A TOUT MOMENT!",
        "de": "Dieser Fehler kann JEDE SEKUNDE behoben werden!",
        "it": "Questo errore puo essere corretto IN QUALSIASI MOMENTO!",
        "ja": "\u3053\u306E\u30A8\u30E9\u30FC\u306F\u3044\u3064\u3067\u3082\u4FEE\u6B63\u3055\u308C\u308B\u53EF\u80FD\u6027\u304C!",
        "ko": "\uC774 \uC624\uB958\uB294 \uC5B8\uC81C\uB4E0 \uC218\uC815\uB420 \uC218 \uC788\uC2B5\uB2C8\uB2E4!",
        "nl": "Deze fout kan ELK MOMENT worden hersteld!",
    },
    "glitch_urgencia2": {
        "pt": "CORRA! Pode desaparecer em minutos!",
        "en": "HURRY! May disappear in minutes!",
        "es": "CORRE! Puede desaparecer en minutos!",
        "fr": "VITE! Peut disparaitre en minutes!",
        "de": "SCHNELL! Kann in Minuten verschwinden!",
        "it": "CORRI! Puo sparire in pochi minuti!",
        "ja": "\u6025\u3044\u3067\uFF01\u6570\u5206\u3067\u6D88\u3048\u308B\u304B\u3082!",
        "ko": "\uC11C\uB450\uB974\uC138\uC694! \uBA87 \uBD84 \uC548\uC5D0 \uC0AC\uB77C\uC9C8 \uC218 \uC788\uC2B5\uB2C8\uB2E4!",
        "nl": "SNEL! Kan binnen minuten verdwijnen!",
    },
    "glitch_normalmente": {
        "pt": "Normalmente",
        "en": "Normally",
        "es": "Normalmente",
        "fr": "Normalement",
        "de": "Normalerweise",
        "it": "Normalmente",
        "ja": "\u901A\u5E38",
        "ko": "\uC77C\uBC18\uC801\uC73C\uB85C",
        "nl": "Normaal",
    },
    "glitch_agora": {
        "pt": "AGORA",
        "en": "NOW",
        "es": "AHORA",
        "fr": "MAINTENANT",
        "de": "JETZT",
        "it": "ORA",
        "ja": "\u4ECA",
        "ko": "\uC9C0\uAE08",
        "nl": "NU",
    },
    "glitch_reserve": {
        "pt": "RESERVE PRIMEIRO, PLANEJE DEPOIS!",
        "en": "BOOK FIRST, PLAN LATER!",
        "es": "RESERVA PRIMERO, PLANIFICA DESPUES!",
        "fr": "RESERVEZ D'ABORD, PLANIFIEZ APRES!",
        "de": "ERST BUCHEN, DANN PLANEN!",
        "it": "PRENOTA PRIMA, PIANIFICA DOPO!",
        "ja": "\u5148\u306B\u4E88\u7D04\u3001\u8A08\u753B\u306F\u5F8C\u3067\uFF01",
        "ko": "\uBA3C\uC800 \uC608\uC57D, \uACC4\uD68D\uC740 \uB098\uC911\uC5D0!",
        "nl": "BOEK EERST, PLAN LATER!",
    },
    "glitch_honram": {
        "pt": "85% das cias aereas HONRAM erros de preco!",
        "en": "85% of airlines HONOR pricing errors!",
        "es": "85% de las aerolineas RESPETAN los errores de precio!",
        "fr": "85% des compagnies HONORENT les erreurs de prix!",
        "de": "85% der Airlines AKZEPTIEREN Preisfehler!",
        "it": "85% delle compagnie ONORANO gli errori di prezzo!",
        "ja": "85%\u306E\u822A\u7A7A\u4F1A\u793E\u304C\u4FA1\u683C\u30A8\u30E9\u30FC\u3092\u5C0A\u91CD!",
        "ko": "85%\uC758 \uD56D\uACF5\uC0AC\uAC00 \uAC00\uACA9 \uC624\uB958\uB97C \uC874\uC911\uD569\uB2C8\uB2E4!",
        "nl": "85% van de airlines RESPECTEERT prijsfouten!",
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

# Mapeamento de regiao para idioma
REGIAO_IDIOMA = {
    "BR": "pt",
    "US": "en",
    "UK": "en",
    "AU": "en",
    "CA": "en",
    "EU": "en",  # Europa usa ingles como padrao (multi-idioma)
    "CH": "en",
    "AE": "en",
    "JP": "ja",
    "KR": "ko",
    "DK": "en",  # Nordicos entendem ingles
    "SE": "en",
    "NO": "en",
    "MX": "es",
}

# Codigos de idioma do Telegram para idioma do bot
LANG_CODE_MAP = {
    "pt": "pt", "pt-br": "pt", "pt_br": "pt",
    "es": "es", "es-419": "es", "es_mx": "es", "es_es": "es",
    "fr": "fr", "fr-fr": "fr", "fr_fr": "fr",
    "de": "de", "de-de": "de", "de_de": "de", "de-ch": "de",
    "it": "it", "it-it": "it", "it_it": "it",
    "ja": "ja", "ja-jp": "ja",
    "ko": "ko", "ko-kr": "ko",
    "nl": "nl", "nl-nl": "nl",
}


def detectar_idioma(language_code: str = "", regiao: str = "") -> str:
    """
    Detecta o idioma do usuario baseado em:
    1. Regiao selecionada (BR=pt, MX=es, JP=ja, KR=ko)
    2. language_code do Telegram
    3. Fallback: en (ingles)
    """
    # Regiao define idioma primario
    if regiao in REGIAO_IDIOMA:
        idioma_regiao = REGIAO_IDIOMA[regiao]
        if idioma_regiao != "en":
            return idioma_regiao

    # Telegram language_code pode refinar
    if language_code:
        lang = language_code.lower().replace("-", "_")
        for code, idioma in LANG_CODE_MAP.items():
            if lang == code.replace("-", "_") or lang.startswith(code.split("-")[0]):
                return idioma

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
