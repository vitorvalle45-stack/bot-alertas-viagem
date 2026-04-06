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
from monitor_feeds import buscar_novos_deals, formatar_mensagem_telegram

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Arquivo para salvar IDs dos usuarios inscritos
ARQUIVO_USUARIOS = "usuarios.json"


def carregar_usuarios() -> set:
    caminho = Path(ARQUIVO_USUARIOS)
    if caminho.exists():
        with open(caminho, "r") as f:
            return set(json.load(f))
    return set()


def salvar_usuarios(usuarios: set):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(list(usuarios), f)


def adicionar_usuario(chat_id: int):
    usuarios = carregar_usuarios()
    usuarios.add(chat_id)
    salvar_usuarios(usuarios)


# ==================== COMANDOS DO BOT ====================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensagem de boas-vindas quando alguem inicia o bot."""
    usuario = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # Salva o usuario para receber alertas direto no chat
    adicionar_usuario(chat_id)
    logger.info(f"Usuario registrado: {usuario} (ID: {chat_id})")

    texto = (
        f"Ola, {usuario}! \u2708\uFE0F\n\n"
        f"Bem-vindo ao <b>Bot de Alertas de Viagem!</b>\n\n"
        f"Eu monitoro dezenas de fontes 24/7 procurando:\n"
        f"\u2022 \U0001F525 Passagens aereas com precos absurdos\n"
        f"\u2022 \U0001F6A8 Error fares (erros de preco das cias aereas)\n"
        f"\u2022 \U0001F4B0 Promocoes relampago de hospedagem\n\n"
        f"<b>Como funciona:</b>\n"
        f"1\uFE0F\u20E3 Entre no nosso canal de alertas\n"
        f"2\uFE0F\u20E3 Ative as notificacoes \U0001F514\n"
        f"3\uFE0F\u20E3 Receba alertas automaticos\n"
        f"4\uFE0F\u20E3 Compre rapido antes que saia do ar!\n\n"
        f"<b>Comandos disponiveis:</b>\n"
        f"/start - Esta mensagem\n"
        f"/ajuda - Como usar o bot\n"
        f"/buscar - Ver ultimos deals encontrados\n"
        f"/stats - Estatisticas do bot\n"
    )

    botoes = []
    if CHANNEL_ID:
        canal_link = CHANNEL_ID if CHANNEL_ID.startswith("@") else f"https://t.me/{CHANNEL_ID}"
        if CHANNEL_ID.startswith("@"):
            canal_link = f"https://t.me/{CHANNEL_ID[1:]}"
        botoes.append([InlineKeyboardButton("\U0001F4E2 Entrar no Canal de Alertas", url=canal_link)])

    botoes.append([InlineKeyboardButton("\u2764\uFE0F Compartilhar com amigos", switch_inline_query="Confira esse bot de passagens baratas!")])

    keyboard = InlineKeyboardMarkup(botoes) if botoes else None

    await update.message.reply_text(texto, parse_mode=ParseMode.HTML, reply_markup=keyboard)


async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de ajuda."""
    texto = (
        "\U0001F4D6 <b>COMO USAR O BOT</b>\n\n"
        "<b>1. Entre no canal de alertas</b>\n"
        "La voce recebe todos os deals automaticamente.\n\n"
        "<b>2. Ative as notificacoes</b>\n"
        "Clique no nome do canal > Notificacoes > Ativar\n"
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
    )
    await update.message.reply_text(texto, parse_mode=ParseMode.HTML)


async def cmd_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Busca manualmente os ultimos deals."""
    await update.message.reply_text("\U0001F50D Buscando deals agora... Aguarde!")

    try:
        deals = buscar_novos_deals()

        if not deals:
            await update.message.reply_text(
                "\U0001F614 Nenhum deal novo encontrado agora.\n"
                "Os feeds sao atualizados constantemente. Tente novamente em alguns minutos!"
            )
            return

        await update.message.reply_text(f"\u2705 Encontrei {len(deals)} deal(s)!\n")

        for deal in deals:
            mensagem = formatar_mensagem_telegram(deal)
            await update.message.reply_text(mensagem, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    except Exception as e:
        logger.error(f"Erro ao buscar deals: {e}")
        await update.message.reply_text(f"\u274C Erro ao buscar deals: {e}")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra estatisticas do bot."""
    import json
    from pathlib import Path
    from config import ARQUIVO_DEALS_ENVIADOS

    total_enviados = 0
    caminho = Path(ARQUIVO_DEALS_ENVIADOS)
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            total_enviados = len(dados)

    texto = (
        "\U0001F4CA <b>ESTATISTICAS DO BOT</b>\n\n"
        f"\U0001F4E8 Deals enviados (ultimos 7 dias): <b>{total_enviados}</b>\n"
        f"\U0001F4E1 Feeds monitorados: <b>{len(__import__('config').RSS_FEEDS)}</b>\n"
        f"\u23F0 Intervalo de checagem: <b>{INTERVALO_CHECAGEM // 60} minutos</b>\n"
        f"\U0001F4C5 Alerta diario: <b>{HORARIO_ALERTA_DIARIO[0]:02d}:{HORARIO_ALERTA_DIARIO[1]:02d}</b>\n"
    )
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

        # Envia direto para cada usuario inscrito
        for chat_id in usuarios:
            for deal in deals:
                mensagem = formatar_mensagem_telegram(deal)
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
