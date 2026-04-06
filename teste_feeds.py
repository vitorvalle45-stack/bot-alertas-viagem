"""
Teste rapido dos feeds RSS - Roda sem precisar do token do Telegram.
Verifica se os feeds estao acessiveis e mostra os deals encontrados.
"""
from monitor_feeds import buscar_novos_deals, formatar_mensagem_telegram
from config import RSS_FEEDS
import feedparser


def testar_conexao_feeds():
    """Testa se cada feed RSS esta acessivel."""
    print("=" * 60)
    print("  TESTE DE CONEXAO COM FEEDS RSS")
    print("=" * 60)

    for feed_config in RSS_FEEDS:
        nome = feed_config["nome"]
        url = feed_config["url"]
        print(f"\nTestando: {nome}")
        print(f"URL: {url}")

        try:
            feed = feedparser.parse(url)

            if feed.bozo and not feed.entries:
                print(f"  FALHA - Erro: {feed.bozo_exception}")
                continue

            total = len(feed.entries)
            print(f"  OK! {total} entradas encontradas")

            if total > 0:
                print(f"  Ultimo deal: {feed.entries[0].get('title', 'Sem titulo')[:80]}")

        except Exception as e:
            print(f"  ERRO: {e}")

    print("\n" + "=" * 60)


def testar_busca_deals():
    """Busca deals e mostra formatados como ficariam no Telegram."""
    print("\n" + "=" * 60)
    print("  BUSCANDO DEALS (como apareceria no Telegram)")
    print("=" * 60)

    deals = buscar_novos_deals()

    if not deals:
        print("\nNenhum deal novo encontrado.")
        print("(Isso pode acontecer se todos os deals ja foram vistos antes.)")
        print("Dica: Delete o arquivo deals_enviados.json e tente novamente.")
        return

    print(f"\n{len(deals)} deal(s) encontrado(s):\n")

    for i, deal in enumerate(deals, 1):
        print(f"--- DEAL {i} (score: {deal['relevancia']['score']}) ---")
        import re
        msg = formatar_mensagem_telegram(deal)
        msg_limpa = re.sub(r'<[^>]+>', '', msg)
        # Remove emojis para compatibilidade com terminal Windows
        msg_limpa = msg_limpa.encode("ascii", "ignore").decode("ascii")
        print(msg_limpa)
        print()


if __name__ == "__main__":
    testar_conexao_feeds()
    testar_busca_deals()
    print("\nTeste concluido! Se os feeds estao OK, seu bot esta pronto.")
    print("Proximo passo: Configure o .env com seu token do Telegram.")
