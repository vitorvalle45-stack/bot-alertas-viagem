"""
Bot de Alertas de Viagem - Telegram
Envia deals de passagens aereas baratas automaticamente.
"""
import json
import logging
from datetime import time as dt_time
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from telegram.constants import ParseMode

from config import (
    BOT_TOKEN,
    CHANNEL_ID,
    ADMIN_ID,
    INTERVALO_CHECAGEM,
    HORARIO_ALERTA_DIARIO,
)
from monitor_feeds import buscar_novos_deals, formatar_mensagem_telegram, formatar_mensagem_com_moeda
from traducoes import t, detectar_idioma

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Arquivo para salvar preferencias dos usuarios
ARQUIVO_USUARIOS = "usuarios.json"

# Regioes disponiveis
REGIOES = {
    "BR": {"nome": "Brasil", "moeda": "BRL", "simbolo": "R$", "flag": "\U0001F1E7\U0001F1F7"},
    "US": {"nome": "Estados Unidos", "moeda": "USD", "simbolo": "US$", "flag": "\U0001F1FA\U0001F1F8"},
    "UK": {"nome": "Reino Unido", "moeda": "GBP", "simbolo": "\u00A3", "flag": "\U0001F1EC\U0001F1E7"},
    "EU": {"nome": "Europa (Euro)", "moeda": "EUR", "simbolo": "\u20AC", "flag": "\U0001F1EA\U0001F1FA"},
    "CH": {"nome": "Suica", "moeda": "CHF", "simbolo": "CHF", "flag": "\U0001F1E8\U0001F1ED"},
    "AU": {"nome": "Australia", "moeda": "AUD", "simbolo": "A$", "flag": "\U0001F1E6\U0001F1FA"},
    "AE": {"nome": "Emirados Arabes", "moeda": "AED", "simbolo": "AED", "flag": "\U0001F1E6\U0001F1EA"},
    "JP": {"nome": "Japao", "moeda": "JPY", "simbolo": "\u00A5", "flag": "\U0001F1EF\U0001F1F5"},
    "KR": {"nome": "Coreia do Sul", "moeda": "KRW", "simbolo": "\u20A9", "flag": "\U0001F1F0\U0001F1F7"},
    "CA": {"nome": "Canada", "moeda": "CAD", "simbolo": "C$", "flag": "\U0001F1E8\U0001F1E6"},
    "DK": {"nome": "Dinamarca", "moeda": "DKK", "simbolo": "DKK", "flag": "\U0001F1E9\U0001F1F0"},
    "SE": {"nome": "Suecia", "moeda": "SEK", "simbolo": "SEK", "flag": "\U0001F1F8\U0001F1EA"},
    "NO": {"nome": "Noruega", "moeda": "NOK", "simbolo": "NOK", "flag": "\U0001F1F3\U0001F1F4"},
    "MX": {"nome": "Mexico", "moeda": "MXN", "simbolo": "MX$", "flag": "\U0001F1F2\U0001F1FD"},
}


def carregar_usuarios() -> dict:
    caminho = Path(ARQUIVO_USUARIOS)
    if caminho.exists():
        with open(caminho, "r") as f:
            dados = json.load(f)
        # Compatibilidade: se for lista antiga, converte pra dict
        if isinstance(dados, list):
            return {str(uid): {"regiao": "BR", "moeda": "BRL"} for uid in dados}
        return dados
    return {}


def salvar_usuarios(usuarios: dict):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)


def adicionar_usuario(chat_id: int, regiao: str = "BR", lang_code: str = ""):
    usuarios = carregar_usuarios()
    info_regiao = REGIOES.get(regiao, REGIOES["BR"])
    idioma = detectar_idioma(lang_code, regiao)
    usuarios[str(chat_id)] = {
        "regiao": regiao,
        "moeda": info_regiao["moeda"],
        "idioma": idioma,
    }
    salvar_usuarios(usuarios)


def get_idioma_usuario(chat_id: int) -> str:
    usuarios = carregar_usuarios()
    dados = usuarios.get(str(chat_id), {})
    return dados.get("idioma", "en")


def get_moeda_usuario(chat_id: int) -> str:
    usuarios = carregar_usuarios()
    dados = usuarios.get(str(chat_id), {})
    return dados.get("moeda", "BRL")


# ==================== COMANDOS DO BOT ====================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensagem de boas-vindas quando alguem inicia o bot."""
    usuario = update.effective_user.first_name
    chat_id = update.effective_chat.id
    lang_code = update.effective_user.language_code or ""

    # Detecta idioma pelo Telegram e salva
    idioma = detectar_idioma(lang_code)
    adicionar_usuario(chat_id, "BR", lang_code)
    logger.info(f"Usuario registrado: {usuario} (ID: {chat_id}, lang: {lang_code}, idioma: {idioma})")

    texto = t("welcome", idioma, nome=usuario)

    # Botoes de regiao em grid
    botoes = [
        [
            InlineKeyboardButton("\U0001F1E7\U0001F1F7 Brasil (R$)", callback_data="regiao_BR"),
            InlineKeyboardButton("\U0001F1FA\U0001F1F8 EUA (US$)", callback_data="regiao_US"),
        ],
        [
            InlineKeyboardButton("\U0001F1EC\U0001F1E7 UK (\u00A3)", callback_data="regiao_UK"),
            InlineKeyboardButton("\U0001F1EA\U0001F1FA Europa (\u20AC)", callback_data="regiao_EU"),
        ],
        [
            InlineKeyboardButton("\U0001F1E8\U0001F1ED Suica (CHF)", callback_data="regiao_CH"),
            InlineKeyboardButton("\U0001F1E6\U0001F1FA Australia (A$)", callback_data="regiao_AU"),
        ],
        [
            InlineKeyboardButton("\U0001F1E6\U0001F1EA Emirados (AED)", callback_data="regiao_AE"),
            InlineKeyboardButton("\U0001F1EF\U0001F1F5 Japao (\u00A5)", callback_data="regiao_JP"),
        ],
        [
            InlineKeyboardButton("\U0001F1F0\U0001F1F7 Coreia (\u20A9)", callback_data="regiao_KR"),
            InlineKeyboardButton("\U0001F1E8\U0001F1E6 Canada (C$)", callback_data="regiao_CA"),
        ],
        [
            InlineKeyboardButton("\U0001F1E9\U0001F1F0 Dinamarca", callback_data="regiao_DK"),
            InlineKeyboardButton("\U0001F1F8\U0001F1EA Suecia", callback_data="regiao_SE"),
        ],
        [
            InlineKeyboardButton("\U0001F1F3\U0001F1F4 Noruega", callback_data="regiao_NO"),
            InlineKeyboardButton("\U0001F1F2\U0001F1FD Mexico", callback_data="regiao_MX"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(botoes)
    await update.message.reply_text(texto, parse_mode=ParseMode.HTML, reply_markup=keyboard)


async def cmd_moeda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Permite trocar a regiao/moeda."""
    idioma = get_idioma_usuario(update.effective_chat.id)
    texto = t("escolha_moeda", idioma)

    botoes = [
        [
            InlineKeyboardButton("\U0001F1E7\U0001F1F7 Brasil (R$)", callback_data="regiao_BR"),
            InlineKeyboardButton("\U0001F1FA\U0001F1F8 EUA (US$)", callback_data="regiao_US"),
        ],
        [
            InlineKeyboardButton("\U0001F1EC\U0001F1E7 UK (\u00A3)", callback_data="regiao_UK"),
            InlineKeyboardButton("\U0001F1EA\U0001F1FA Europa (\u20AC)", callback_data="regiao_EU"),
        ],
        [
            InlineKeyboardButton("\U0001F1E8\U0001F1ED Suica (CHF)", callback_data="regiao_CH"),
            InlineKeyboardButton("\U0001F1E6\U0001F1FA Australia (A$)", callback_data="regiao_AU"),
        ],
        [
            InlineKeyboardButton("\U0001F1E6\U0001F1EA Emirados (AED)", callback_data="regiao_AE"),
            InlineKeyboardButton("\U0001F1EF\U0001F1F5 Japao (\u00A5)", callback_data="regiao_JP"),
        ],
        [
            InlineKeyboardButton("\U0001F1F0\U0001F1F7 Coreia (\u20A9)", callback_data="regiao_KR"),
            InlineKeyboardButton("\U0001F1E8\U0001F1E6 Canada (C$)", callback_data="regiao_CA"),
        ],
        [
            InlineKeyboardButton("\U0001F1E9\U0001F1F0 Dinamarca", callback_data="regiao_DK"),
            InlineKeyboardButton("\U0001F1F8\U0001F1EA Suecia", callback_data="regiao_SE"),
        ],
        [
            InlineKeyboardButton("\U0001F1F3\U0001F1F4 Noruega", callback_data="regiao_NO"),
            InlineKeyboardButton("\U0001F1F2\U0001F1FD Mexico", callback_data="regiao_MX"),
        ],
    ]

    await update.message.reply_text(texto, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(botoes))


async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de ajuda."""
    idioma = get_idioma_usuario(update.effective_chat.id)
    await update.message.reply_text(t("ajuda", idioma), parse_mode=ParseMode.HTML)


async def cmd_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca manualmente os ultimos deals."""
    chat_id = update.effective_chat.id
    idioma = get_idioma_usuario(chat_id)
    moeda = get_moeda_usuario(chat_id)

    await update.message.reply_text(t("buscando", idioma))

    try:
        deals = buscar_novos_deals()

        if not deals:
            await update.message.reply_text(t("nenhum_deal", idioma))
            return

        await update.message.reply_text(t("deals_encontrados", idioma, n=len(deals)))

        for deal in deals:
            mensagem = formatar_mensagem_com_moeda(deal, moeda, idioma)
            await update.message.reply_text(mensagem, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    except Exception as e:
        logger.error(f"Erro ao buscar deals: {e}")
        await update.message.reply_text(f"\u274C Erro ao buscar deals: {e}")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra estatisticas do bot."""
    from config import ARQUIVO_DEALS_ENVIADOS, RSS_FEEDS

    idioma = get_idioma_usuario(update.effective_chat.id)
    total_enviados = 0
    caminho = Path(ARQUIVO_DEALS_ENVIADOS)
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            total_enviados = len(dados)

    texto = t("stats", idioma,
              total=total_enviados,
              feeds=len(RSS_FEEDS),
              intervalo=INTERVALO_CHECAGEM // 60)
    await update.message.reply_text(texto, parse_mode=ParseMode.HTML)


# ============ COMANDO ADMIN: FORCAR ENVIO PRO CANAL ============

async def cmd_enviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """(Admin) Forca envio de deals para o canal."""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("\u274C Comando restrito ao admin.")
        return

    if not CHANNEL_ID:
        await update.message.reply_text("\u274C CHANNEL_ID nao configurado no .env")
        return

    await update.message.reply_text("\U0001F4E4 Buscando e enviando deals para o canal...")

    try:
        deals = buscar_novos_deals()

        if not deals:
            await update.message.reply_text("Nenhum deal novo para enviar.")
            return

        enviados = 0
        for deal in deals:
            mensagem = formatar_mensagem_telegram(deal)
            try:
                await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=mensagem,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                enviados += 1
            except Exception as e:
                logger.error(f"Erro ao enviar deal pro canal: {e}")

        await update.message.reply_text(f"\u2705 {enviados} deal(s) enviado(s) para o canal!")

    except Exception as e:
        await update.message.reply_text(f"\u274C Erro: {e}")


# ==================== JOBS AUTOMATICOS ====================

async def job_verificar_feeds(context: ContextTypes.DEFAULT_TYPE):
    """Job automatico: verifica feeds e envia deals para todos os usuarios inscritos."""
    logger.info("Job automatico: verificando feeds...")

    try:
        deals = buscar_novos_deals()

        if not deals:
            logger.info("Nenhum deal novo encontrado.")
            return

        usuarios = carregar_usuarios()

        # Tenta enviar pro canal se configurado
        if CHANNEL_ID:
            for deal in deals:
                mensagem = formatar_mensagem_telegram(deal)
                try:
                    await context.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=mensagem,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                    logger.info(f"Deal enviado pro canal: {deal['titulo'][:50]}")
                except Exception as e:
                    logger.debug(f"Canal nao disponivel, enviando direto pros usuarios: {e}")

        # Envia direto para cada usuario inscrito, na moeda e idioma dele
        for chat_id_str, user_data in usuarios.items():
            chat_id = int(chat_id_str)
            moeda = user_data.get("moeda", "BRL")
            idioma = user_data.get("idioma", "en")
            for deal in deals:
                mensagem = formatar_mensagem_com_moeda(deal, moeda, idioma)
                try:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=mensagem,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                except Exception as e:
                    logger.error(f"Erro ao enviar deal para {chat_id}: {e}")

        logger.info(f"{len(deals)} deals enviados para {len(usuarios)} usuario(s)")

    except Exception as e:
        logger.error(f"Erro no job de feeds: {e}")


async def job_alerta_diario(context: ContextTypes.DEFAULT_TYPE):
    """Job diario: envia resumo matinal."""
    if not CHANNEL_ID:
        return

    texto = (
        "\u2615 <b>BOM DIA! Alerta Diario de Viagem</b>\n\n"
        "\U0001F50D Estou monitorando os melhores deals para voce!\n\n"
        "Fique atento \u2014 error fares podem aparecer a qualquer momento.\n"
        "\U0001F514 Mantenha as notificacoes ativadas para nao perder nada!\n\n"
        "\U0001F4AA Boas economias hoje!"
    )

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=texto,
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f"Erro no alerta diario: {e}")


# ==================== CALLBACKS ====================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trata cliques em botoes inline."""
    query = update.callback_query
    data = query.data

    if data and data.startswith("regiao_"):
        regiao = data.replace("regiao_", "")
        chat_id = query.from_user.id
        lang_code = query.from_user.language_code or ""

        if regiao in REGIOES:
            adicionar_usuario(chat_id, regiao, lang_code)
            info = REGIOES[regiao]
            idioma = detectar_idioma(lang_code, regiao)

            await query.answer(f"{info['nome']} ({info['simbolo']})")

            texto = t("regiao_ok", idioma,
                      flag=info['flag'], regiao=info['nome'],
                      simbolo=info['simbolo'], moeda=info['moeda'])

            botoes = []
            if CHANNEL_ID:
                canal_link = f"https://t.me/{CHANNEL_ID[1:]}" if CHANNEL_ID.startswith("@") else CHANNEL_ID
                botoes.append([InlineKeyboardButton(t("entrar_canal", idioma), url=canal_link)])
            botoes.append([InlineKeyboardButton(t("compartilhar", idioma), switch_inline_query=t("share_text", idioma))])

            keyboard = InlineKeyboardMarkup(botoes) if botoes else None
            await query.edit_message_text(texto, parse_mode=ParseMode.HTML, reply_markup=keyboard)
            logger.info(f"Usuario {chat_id} configurou regiao: {regiao} ({info['moeda']}, idioma: {idioma})")
        else:
            await query.answer("Invalid region")
    else:
        await query.answer()


# ==================== MAIN ====================

def main():
    """Inicia o bot."""
    if not BOT_TOKEN:
        print("\n" + "=" * 50)
        print("ERRO: Token do bot nao configurado!")
        print("=" * 50)
        print("\nSiga estes passos:")
        print("1. Abra o Telegram e fale com @BotFather")
        print("2. Envie /newbot e siga as instrucoes")
        print("3. Copie o token que o BotFather te dar")
        print("4. Copie o arquivo .env.example para .env")
        print("5. Cole o token no arquivo .env")
        print("6. Execute este script novamente\n")
        return

    print("\n" + "=" * 50)
    print("  BOT DE ALERTAS DE VIAGEM")
    print("=" * 50)
    print(f"\n  Canal: {CHANNEL_ID or 'NAO CONFIGURADO'}")
    print(f"  Checagem a cada: {INTERVALO_CHECAGEM // 60} minutos")
    print(f"  Alerta diario: {HORARIO_ALERTA_DIARIO[0]:02d}:{HORARIO_ALERTA_DIARIO[1]:02d}")
    print(f"\n  Iniciando bot...")
    print("=" * 50 + "\n")

    # Cria a aplicacao
    app = Application.builder().token(BOT_TOKEN).build()

    # Registra comandos
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CommandHandler("buscar", cmd_buscar))
    app.add_handler(CommandHandler("moeda", cmd_moeda))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("enviar", cmd_enviar))
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Jobs automaticos
    job_queue = app.job_queue

    if job_queue:
        # Verifica feeds a cada X minutos
        job_queue.run_repeating(
            job_verificar_feeds,
            interval=INTERVALO_CHECAGEM,
            first=30,  # primeira execucao apos 30 segundos
            name="verificar_feeds",
        )

        # Alerta diario as 6h (UTC-3 = 9h UTC)
        hora_utc = (HORARIO_ALERTA_DIARIO[0] + 3) % 24
        job_queue.run_daily(
            job_alerta_diario,
            time=dt_time(hour=hora_utc, minute=HORARIO_ALERTA_DIARIO[1]),
            name="alerta_diario",
        )

        logger.info("Jobs automaticos configurados!")

    # Inicia o bot
    print("Bot rodando! Pressione Ctrl+C para parar.\n")
    app.run_polling(drop_pending_updates=True)


def main_render():
    """Versao especial para rodar no Render (Python 3.14 + web server)."""
    import asyncio
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler

    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bot de Alertas de Viagem rodando!")
        def log_message(self, format, *args):
            pass

    def start_http():
        server = HTTPServer(("0.0.0.0", port), Handler)
        server.serve_forever()

    http_thread = threading.Thread(target=start_http, daemon=True)
    http_thread.start()
    logger.info(f"Servidor web rodando na porta {port}")

    # Self-ping: mantem o Render acordado pingando a si mesmo a cada 10 min
    def self_ping():
        import time
        import httpx
        render_url = os.environ.get("RENDER_EXTERNAL_URL", "https://bot-alertas-viagem.onrender.com")
        while True:
            time.sleep(600)  # 10 minutos
            try:
                httpx.get(render_url, timeout=30)
                logger.info(f"Self-ping OK: {render_url}")
            except Exception as e:
                logger.debug(f"Self-ping falhou (normal no startup): {e}")

    ping_thread = threading.Thread(target=self_ping, daemon=True)
    ping_thread.start()
    logger.info("Self-ping configurado (a cada 10 min)")

    if not BOT_TOKEN:
        print("ERRO: Token nao configurado!")
        return

    # Cria loop explicitamente e roda tudo async
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(CommandHandler("buscar", cmd_buscar))
    app.add_handler(CommandHandler("moeda", cmd_moeda))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("enviar", cmd_enviar))
    app.add_handler(CallbackQueryHandler(callback_handler))

    job_queue = app.job_queue
    if job_queue:
        job_queue.run_repeating(
            job_verificar_feeds,
            interval=INTERVALO_CHECAGEM,
            first=30,
            name="verificar_feeds",
        )
        hora_utc = (HORARIO_ALERTA_DIARIO[0] + 3) % 24
        job_queue.run_daily(
            job_alerta_diario,
            time=dt_time(hour=hora_utc, minute=HORARIO_ALERTA_DIARIO[1]),
            name="alerta_diario",
        )

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    import os
    if os.environ.get("RENDER") or os.environ.get("PORT"):
        main_render()
    else:
        main()
