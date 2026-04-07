"""
Monitor de RSS Feeds - Busca deals de passagens aereas automaticamente
"""
import json
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path

import feedparser

from config import (
    RSS_FEEDS,
    CIDADES_BR,
    CIDADES_POR_REGIAO,
    DESTINOS_POPULARES,
    SCORE_MINIMO,
    ARQUIVO_DEALS_ENVIADOS,
    MAX_DEALS_POR_CHECAGEM,
)

logger = logging.getLogger(__name__)


def carregar_deals_enviados() -> dict:
    """Carrega historico de deals ja enviados para evitar duplicatas."""
    caminho = Path(ARQUIVO_DEALS_ENVIADOS)
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        # Limpa deals com mais de 7 dias para nao crescer infinitamente
        limite = (datetime.now() - timedelta(days=7)).isoformat()
        dados = {k: v for k, v in dados.items() if v.get("data", "") > limite}
        return dados
    return {}


def salvar_deals_enviados(deals: dict):
    """Salva historico de deals enviados."""
    with open(ARQUIVO_DEALS_ENVIADOS, "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)


def gerar_id_deal(titulo: str, link: str) -> str:
    """Gera um ID unico para cada deal baseado no titulo e link."""
    texto = f"{titulo}{link}".lower().strip()
    return hashlib.md5(texto.encode()).hexdigest()


def detectar_origem_regiao(texto: str) -> str:
    """Detecta de qual regiao o deal esta saindo, baseado nas cidades mencionadas."""
    import re as _re
    texto_lower = texto.lower()

    for regiao, cidades in CIDADES_POR_REGIAO.items():
        for cidade in cidades:
            pattern = r'\b' + _re.escape(cidade) + r'\b'
            if _re.search(pattern, texto_lower):
                pos = texto_lower.find(cidade)
                trecho_antes = texto_lower[:pos]
                # Indicadores de que eh a origem
                eh_origem = any(ind in trecho_antes[-30:] for ind in ["from ", "de ", "saindo de ", "departing "])
                eh_destino = any(ind in trecho_antes[-30:] for ind in [" to ", " para ", " nach "])

                # Codigos IATA sao quase sempre origem no contexto de deals
                codigos_iata = [c for c in cidades if len(c) == 3 and c.isalpha()]

                if eh_origem or (not eh_destino and cidade in codigos_iata):
                    return regiao
    return ""


def calcular_relevancia(titulo: str, resumo: str, regiao_usuario: str = "BR") -> dict:
    """
    Analisa o deal e retorna score de relevancia.
    Prioriza deals com origem no pais/regiao do usuario.
    """
    texto = f"{titulo} {resumo}".lower()
    resultado = {
        "score": 0,
        "origem_brasil": False,
        "origem_regiao": "",
        "destino_popular": False,
        "error_fare": False,
        "tags": [],
    }

    # Detecta regiao de origem do deal
    origem = detectar_origem_regiao(texto)
    resultado["origem_regiao"] = origem

    if origem:
        if origem == regiao_usuario:
            # Deal saindo do PAIS do usuario = alta prioridade (+12)
            resultado["score"] += 12
            nomes_regiao = {
                "BR": "Brasil", "US": "USA", "UK": "UK", "EU": "Europe",
                "CH": "Switzerland", "AU": "Australia", "AE": "UAE",
                "JP": "Japan", "KR": "Korea", "CA": "Canada",
                "DK": "Denmark", "SE": "Sweden", "NO": "Norway", "MX": "Mexico",
            }
            resultado["tags"].append(f"From {nomes_regiao.get(origem, origem)}")
        elif origem == "BR":
            resultado["origem_brasil"] = True
            resultado["score"] += 5
            resultado["tags"].append("From Brazil")
        else:
            # Deal de outra regiao, ainda tem valor (+3)
            resultado["score"] += 3

    # Verifica se o destino eh popular (+5 pontos)
    for destino in DESTINOS_POPULARES:
        if destino in texto:
            resultado["score"] += 5
            resultado["destino_popular"] = True
            resultado["tags"].append(destino.title())
            break

    # Bonus para error fares / mistake fares (+15 pontos - PREMIUM)
    termos_error = [
        "error fare", "mistake fare", "glitch fare", "fuel dump",
        "pricing error", "pricing mistake", "pricing glitch",
        "error", "mistake", "glitch", "bug fare",
        "erro tarif", "erro de preco", "bug passagem",
        "too good to be true", "book fast", "won't last",
        "hurry", "act fast", "disappear",
    ]
    for termo in termos_error:
        if termo in texto:
            resultado["score"] += 15
            resultado["error_fare"] = True
            resultado["tags"].append("\U0001F6A8 ERROR FARE")
            break

    # Detecta precos absurdamente baixos = provavel error fare
    import re
    precos = re.findall(r'\$\s*(\d+)', texto)
    for p in precos:
        valor = int(p)
        # Voo internacional por menos de $200 = quase certeza error fare
        if valor > 0 and valor < 200:
            internacional = any(d in texto for d in DESTINOS_POPULARES)
            if internacional and not resultado["error_fare"]:
                resultado["score"] += 12
                resultado["error_fare"] = True
                resultado["tags"].append("\U0001F6A8 POSSIBLE ERROR FARE")
                break

    # Bonus para precos muito baixos mencionados (+3 pontos)
    termos_barato = [
        "cheap", "deal", "sale", "promo", "barato", "oferta",
        "desconto", "from $",
    ]
    for termo in termos_barato:
        if termo in texto:
            resultado["score"] += 3
            break

    return resultado


# Cotacoes base (1 USD = X moeda). Atualizar periodicamente.
COTACOES_DE_USD = {
    "USD": 1.0,
    "BRL": 5.50,
    "EUR": 0.92,
    "GBP": 0.79,
    "CHF": 0.88,
    "AUD": 1.53,
    "AED": 3.67,
    "JPY": 151.0,
    "KRW": 1340.0,
    "CAD": 1.36,
    "DKK": 6.88,
    "SEK": 10.45,
    "NOK": 10.70,
    "MXN": 17.15,
}

SIMBOLOS_MOEDA = {
    "USD": "US$", "BRL": "R$", "EUR": "\u20AC", "GBP": "\u00A3",
    "CHF": "CHF", "AUD": "A$", "AED": "AED", "JPY": "\u00A5",
    "KRW": "\u20A9", "CAD": "C$", "DKK": "DKK", "SEK": "SEK",
    "NOK": "NOK", "MXN": "MX$",
}


def extrair_valor_usd(preco_str: str) -> float:
    """Extrai valor numerico e converte para USD como base."""
    import re
    numeros = re.findall(r'[\d.,]+', preco_str)
    if not numeros:
        return 0.0

    valor_str = numeros[0].replace(',', '')
    try:
        valor = float(valor_str)
    except ValueError:
        return 0.0

    preco_lower = preco_str.lower()
    if 'r$' in preco_lower:
        return valor / COTACOES_DE_USD["BRL"]
    elif '\u20ac' in preco_lower or 'eur' in preco_lower:
        return valor / COTACOES_DE_USD["EUR"]
    elif '\u00a3' in preco_lower or 'gbp' in preco_lower:
        return valor / COTACOES_DE_USD["GBP"]
    elif 'chf' in preco_lower:
        return valor / COTACOES_DE_USD["CHF"]
    elif 'a$' in preco_lower or 'aud' in preco_lower:
        return valor / COTACOES_DE_USD["AUD"]
    else:
        # Assume USD
        return valor


def converter_preco(preco_str: str, moeda_destino: str = "BRL") -> str:
    """Converte preco para qualquer moeda de destino."""
    valor_usd = extrair_valor_usd(preco_str)
    if valor_usd == 0:
        return preco_str

    taxa = COTACOES_DE_USD.get(moeda_destino, 5.50)
    simbolo = SIMBOLOS_MOEDA.get(moeda_destino, moeda_destino)
    valor_convertido = valor_usd * taxa

    # Formata baseado na moeda
    if moeda_destino in ("JPY", "KRW"):
        # Sem decimais pra moedas com valores altos
        texto = f"{simbolo} {valor_convertido:,.0f}"
    else:
        texto = f"{simbolo} {valor_convertido:,.2f}"

    # Adiciona valor original em USD como referencia
    if moeda_destino != "USD":
        texto += f" (~US${valor_usd:,.0f})"

    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def extrair_preco(texto: str) -> str:
    """Tenta extrair preco do titulo/resumo do deal (retorna string original)."""
    import re
    padroes = [
        r'R\$\s*[\d.,]+',
        r'US\$\s*[\d.,]+',
        r'USD\s*[\d.,]+',
        r'\$\s*[\d.,]+',
        r'EUR\s*[\d.,]+',
        r'\u20AC\s*[\d.,]+',
        r'\u00A3\s*[\d.,]+',
        r'GBP\s*[\d.,]+',
        r'CHF\s*[\d.,]+',
        r'A\$\s*[\d.,]+',
    ]
    for padrao in padroes:
        match = re.search(padrao, texto)
        if match:
            return match.group(0)
    return ""


def extrair_rota(titulo: str) -> tuple[str, str]:
    """Tenta extrair origem e destino do titulo."""
    separadores = [" to ", " → ", " - ", " from ", " para "]
    titulo_lower = titulo.lower()

    for sep in separadores:
        if sep in titulo_lower:
            partes = titulo_lower.split(sep, 1)
            if len(partes) == 2:
                # Limpa e capitaliza
                origem = partes[0].strip().split(":")[-1].strip().title()
                destino = partes[1].strip().split("from")[0].strip().title()
                destino = destino.split("for")[0].strip()
                return origem, destino

    return "", ""


def formatar_deal(entry: dict, fonte: str, relevancia: dict) -> dict:
    """Formata um deal do RSS em uma estrutura padronizada."""
    titulo = entry.get("title", "Deal sem titulo")
    link = entry.get("link", "")
    resumo = entry.get("summary", entry.get("description", ""))

    # Limpa HTML do resumo
    import re
    resumo_limpo = re.sub(r'<[^>]+>', '', resumo).strip()
    resumo_limpo = resumo_limpo[:200] + "..." if len(resumo_limpo) > 200 else resumo_limpo

    preco = extrair_preco(f"{titulo} {resumo}")
    origem, destino = extrair_rota(titulo)

    # Data de publicacao
    data_pub = entry.get("published", entry.get("updated", ""))

    return {
        "id": gerar_id_deal(titulo, link),
        "titulo": titulo,
        "link": link,
        "resumo": resumo_limpo,
        "preco": preco,
        "origem": origem,
        "destino": destino,
        "fonte": fonte,
        "data": data_pub,
        "relevancia": relevancia,
        "timestamp": datetime.now().isoformat(),
    }


def formatar_mensagem_telegram(deal: dict) -> str:
    """Formata o deal como mensagem bonita para o Telegram."""
    rel = deal["relevancia"]

    # Emoji baseado no tipo
    if rel["error_fare"]:
        emoji_tipo = "\U0001F6A8"  # sirene
    elif rel["score"] >= 10:
        emoji_tipo = "\U0001F525"  # fogo
    else:
        emoji_tipo = "\u2708\uFE0F"  # aviao

    # Monta a mensagem
    linhas = []

    # Header
    linhas.append(f"{emoji_tipo} <b>ALERTA DE PASSAGEM</b>")

    if rel["error_fare"]:
        linhas.append("\U0001F6A8 <b>POSSIVEL ERROR FARE!</b>")

    linhas.append("")

    # Rota
    if deal["origem"] and deal["destino"]:
        linhas.append(f"\u2708\uFE0F <b>{deal['origem']} \u2192 {deal['destino']}</b>")
    else:
        linhas.append(f"\u2708\uFE0F <b>{deal['titulo']}</b>")

    # Preco
    if deal["preco"]:
        linhas.append(f"\U0001F4B0 <b>{deal['preco']}</b>")

    # Resumo
    if deal["resumo"]:
        linhas.append(f"\n\U0001F4CB {deal['resumo']}")

    # Tags
    if rel["tags"]:
        tags_str = " | ".join(rel["tags"])
        linhas.append(f"\n\U0001F3F7\uFE0F {tags_str}")

    # Fonte
    linhas.append(f"\n\U0001F4F0 Fonte: {deal['fonte']}")

    # Link
    linhas.append(f'\n\U0001F449 <a href="{deal["link"]}">VER DEAL COMPLETO</a>')

    # Rodape
    linhas.append("\n\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014")
    linhas.append("\U0001F514 Ative as notificacoes para nao perder nenhum alerta!")

    return "\n".join(linhas)


def formatar_mensagem_com_moeda(deal: dict, moeda: str = "BRL", idioma: str = "pt") -> str:
    """Formata o deal com preco convertido para a moeda e idioma do usuario."""
    from traducoes import t

    rel = deal["relevancia"]

    if rel["error_fare"]:
        emoji_tipo = "\U0001F6A8"
    elif rel["score"] >= 10:
        emoji_tipo = "\U0001F525"
    else:
        emoji_tipo = "\u2708\uFE0F"

    linhas = []
    linhas.append(f"{emoji_tipo} <b>{t('alerta_passagem', idioma)}</b>")

    if rel["error_fare"]:
        linhas.append(f"\U0001F6A8\U0001F6A8\U0001F6A8 <b>{t('error_fare', idioma)}</b>")
        linhas.append("\u26A0\uFE0F <i>Book NOW - may disappear in hours!</i>")

    linhas.append("")

    if deal["origem"] and deal["destino"]:
        linhas.append(f"\u2708\uFE0F <b>{deal['origem']} \u2192 {deal['destino']}</b>")
    else:
        linhas.append(f"\u2708\uFE0F <b>{deal['titulo']}</b>")

    if deal["preco"]:
        preco_convertido = converter_preco(deal["preco"], moeda)
        linhas.append(f"\U0001F4B0 <b>{preco_convertido}</b>")

    if deal["resumo"]:
        linhas.append(f"\n\U0001F4CB {deal['resumo']}")

    if rel["tags"]:
        tags_str = " | ".join(rel["tags"])
        linhas.append(f"\n\U0001F3F7\uFE0F {tags_str}")

    linhas.append(f"\n\U0001F4F0 {t('fonte', idioma)}: {deal['fonte']}")
    linhas.append(f'\n\U0001F449 <a href="{deal["link"]}">{t("ver_deal", idioma)}</a>')
    linhas.append("\n\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014")
    linhas.append(f"\U0001F514 {t('ativar_notif', idioma)}")

    return "\n".join(linhas)


def buscar_novos_deals(regiao_usuario: str = "BR") -> list[dict]:
    """
    Busca feeds RSS e retorna deals novos ordenados por relevancia.
    Prioriza feeds e deals da regiao do usuario.
    """
    deals_enviados = carregar_deals_enviados()
    novos_deals = []

    # Ordena feeds: primeiro os da regiao do usuario, depois ALL, depois outros
    def prioridade_feed(f):
        r = f.get("regiao", "ALL")
        if r == regiao_usuario:
            return 0
        if r == "ALL":
            return 1
        return 2

    feeds_ordenados = sorted(RSS_FEEDS, key=prioridade_feed)

    for feed_config in feeds_ordenados:
        nome = feed_config["nome"]
        url = feed_config["url"]

        logger.info(f"Verificando feed: {nome}")

        try:
            feed = feedparser.parse(url)

            if feed.bozo and not feed.entries:
                logger.warning(f"Erro ao parsear feed {nome}: {feed.bozo_exception}")
                continue

            for entry in feed.entries[:15]:
                titulo = entry.get("title", "")
                link = entry.get("link", "")
                resumo = entry.get("summary", entry.get("description", ""))
                deal_id = gerar_id_deal(titulo, link)

                # Pula se ja foi enviado
                if deal_id in deals_enviados:
                    continue

                # Calcula relevancia com a regiao do usuario
                relevancia = calcular_relevancia(titulo, resumo, regiao_usuario)

                # Se o feed eh tipo error_fare, marca automaticamente
                if feed_config.get("tipo") == "error_fare" and not relevancia["error_fare"]:
                    relevancia["error_fare"] = True
                    relevancia["score"] += 10
                    if "\U0001F6A8 ERROR FARE" not in relevancia["tags"]:
                        relevancia["tags"].append("\U0001F6A8 ERROR FARE")

                # Bonus se o feed eh da regiao do usuario (+5)
                if feed_config.get("regiao") == regiao_usuario:
                    relevancia["score"] += 5

                # Formata o deal
                deal = formatar_deal(entry, nome, relevancia)
                novos_deals.append(deal)

        except Exception as e:
            logger.error(f"Erro ao buscar feed {nome}: {e}")
            continue

    # Ordena por relevancia (maior primeiro)
    novos_deals.sort(key=lambda d: d["relevancia"]["score"], reverse=True)

    # Limita quantidade
    deals_selecionados = novos_deals[:MAX_DEALS_POR_CHECAGEM]

    # Marca como enviados
    for deal in deals_selecionados:
        deals_enviados[deal["id"]] = {
            "titulo": deal["titulo"],
            "data": deal["timestamp"],
        }

    salvar_deals_enviados(deals_enviados)

    logger.info(f"Encontrados {len(novos_deals)} deals novos, selecionados {len(deals_selecionados)} (regiao: {regiao_usuario})")

    return deals_selecionados
