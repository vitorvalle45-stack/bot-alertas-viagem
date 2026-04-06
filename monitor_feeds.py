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
    DESTINOS_POPULARES,
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


def calcular_relevancia(titulo: str, resumo: str) -> dict:
    """
    Analisa o deal e retorna score de relevancia + metadata.
    Quanto maior o score, mais relevante pro publico brasileiro.
    """
    texto = f"{titulo} {resumo}".lower()
    resultado = {
        "score": 0,
        "origem_brasil": False,
        "destino_popular": False,
        "error_fare": False,
        "tags": [],
    }

    # Verifica se a origem eh do Brasil (+10 pontos)
    # Usa busca por palavra inteira para evitar falsos positivos
    import re as _re
    for cidade in CIDADES_BR:
        pattern = r'\b' + _re.escape(cidade) + r'\b'
        if _re.search(pattern, texto):
            # Verifica se a cidade aparece ANTES de indicadores de destino
            # para confirmar que eh realmente a origem
            pos = texto.find(cidade)
            trecho_antes = texto[:pos]
            # Se "from" ou "de" aparece logo antes, eh origem
            eh_origem = any(ind in trecho_antes[-30:] for ind in ["from ", "de ", "saindo de "])
            # Se "to" ou "para" aparece logo antes, eh destino, nao origem
            eh_destino = any(ind in trecho_antes[-30:] for ind in [" to ", " para "])

            if eh_origem or (not eh_destino and cidade in ["brazil", "brasil", "gru", "gig", "bsb", "cnf", "cwb", "poa", "ssa", "rec", "vcp"]):
                resultado["score"] += 10
                resultado["origem_brasil"] = True
                resultado["tags"].append("Saindo do Brasil")
                break
            else:
                # Destino eh Brasil = tambem relevante mas menos
                resultado["score"] += 5
                resultado["tags"].append("Destino Brasil")
                break

    # Verifica se o destino eh popular para brasileiros (+5 pontos)
    for destino in DESTINOS_POPULARES:
        if destino in texto:
            resultado["score"] += 5
            resultado["destino_popular"] = True
            resultado["tags"].append(destino.title())
            break

    # Bonus para error fares / mistake fares (+8 pontos)
    termos_error = ["error", "mistake", "glitch", "bug", "erro", "falha"]
    for termo in termos_error:
        if termo in texto:
            resultado["score"] += 8
            resultado["error_fare"] = True
            resultado["tags"].append("Error Fare")
            break

    # Bonus para precos muito baixos mencionados (+3 pontos)
    termos_barato = [
        "cheap", "deal", "sale", "promo", "barato", "oferta",
        "desconto", "$1", "$2", "$3", "from $",
    ]
    for termo in termos_barato:
        if termo in texto:
            resultado["score"] += 3
            break

    # Penalidade para destinos menos relevantes (-2 pontos)
    destinos_longe = ["africa", "india", "pakistan", "bangladesh"]
    for destino in destinos_longe:
        if destino in texto:
            resultado["score"] -= 2
            break

    return resultado


COTACAO_USD_BRL = 5.50
COTACAO_EUR_BRL = 6.00
COTACAO_GBP_BRL = 7.00


def converter_para_reais(preco_str: str) -> str:
    """Converte preco em moeda estrangeira para reais."""
    import re
    # Extrai o valor numerico
    numeros = re.findall(r'[\d.,]+', preco_str)
    if not numeros:
        return preco_str

    valor_str = numeros[0].replace(',', '')
    try:
        valor = float(valor_str)
    except ValueError:
        return preco_str

    # Detecta moeda e converte
    preco_lower = preco_str.lower()
    if 'r$' in preco_lower:
        return f"R$ {valor:,.0f}".replace(",", ".")
    elif '€' in preco_lower or 'eur' in preco_lower:
        valor_brl = valor * COTACAO_EUR_BRL
        return f"R$ {valor_brl:,.0f} (~€{valor:,.0f})".replace(",", ".")
    elif '£' in preco_lower or 'gbp' in preco_lower:
        valor_brl = valor * COTACAO_GBP_BRL
        return f"R$ {valor_brl:,.0f} (~£{valor:,.0f})".replace(",", ".")
    else:
        # USD ou $ generico
        valor_brl = valor * COTACAO_USD_BRL
        return f"R$ {valor_brl:,.0f} (~US${valor:,.0f})".replace(",", ".")


def extrair_preco(texto: str) -> str:
    """Tenta extrair preco do titulo/resumo do deal e converte para reais."""
    import re

    # Busca padroes como $299, USD 299, R$ 1.500, etc
    padroes = [
        r'R\$\s*[\d.,]+',
        r'US\$\s*[\d.,]+',
        r'USD\s*[\d.,]+',
        r'\$\s*[\d.,]+',
        r'EUR\s*[\d.,]+',
        r'€\s*[\d.,]+',
        r'£\s*[\d.,]+',
        r'GBP\s*[\d.,]+',
    ]
    for padrao in padroes:
        match = re.search(padrao, texto)
        if match:
            return converter_para_reais(match.group(0))
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


def buscar_novos_deals() -> list[dict]:
    """
    Busca todos os feeds RSS e retorna deals novos ordenados por relevancia.
    """
    deals_enviados = carregar_deals_enviados()
    novos_deals = []

    for feed_config in RSS_FEEDS:
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

                # Calcula relevancia
                relevancia = calcular_relevancia(titulo, resumo)

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

    logger.info(f"Encontrados {len(novos_deals)} deals novos, selecionados {len(deals_selecionados)}")

    return deals_selecionados
