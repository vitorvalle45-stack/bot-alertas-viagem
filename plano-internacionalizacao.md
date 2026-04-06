# PLANO DE INTERNACIONALIZAÇÃO - Bot de Alertas de Viagem

## 1. UM BOT vs VÁRIOS BOTS?

### Resposta: UM BOT SÓ

Um único bot do Telegram consegue:
- Atender usuários de qualquer país
- Mostrar preços na moeda local de cada usuário
- Filtrar deals por aeroporto de origem de cada usuário
- Enviar mensagens no idioma do usuário
- Tudo isso com preferências individuais salvas

Criar vários bots seria:
- Mais trabalho de manutenção (atualizar código em 7+ bots)
- Mais contas pra gerenciar
- Mais servidores/deploys
- Desnecessário tecnicamente

### Como funciona no bot único:

```
/start → Usuário escolhe região:
  🇧🇷 Brasil (R$)
  🇺🇸 Estados Unidos (USD)
  🇬🇧 Reino Unido (GBP)
  🇪🇺 Europa - Euro (EUR)
  🇨🇭 Suíça (CHF)
  🇦🇺 Austrália (AUD)
  🇦🇪 Emirados Árabes (AED)
  🇯🇵 Japão (JPY)
  🇰🇷 Coreia do Sul (KRW)
  🇩🇰 Dinamarca (DKK)
  🇸🇪 Suécia (SEK)
  🇳🇴 Noruega (NOK)

→ Bot salva preferência do usuário
→ Todos os deals aparecem na moeda dele
→ Filtro por aeroportos da região dele
```

## 2. MOEDAS SUPORTADAS

| Região | Moeda | Código | Símbolo |
|--------|-------|--------|---------|
| Brasil | Real | BRL | R$ |
| Estados Unidos | Dólar americano | USD | US$ |
| Reino Unido | Libra esterlina | GBP | £ |
| Zona Euro (Alemanha, França, Itália, Espanha, Portugal, etc.) | Euro | EUR | € |
| Suíça | Franco suíço | CHF | CHF |
| Austrália | Dólar australiano | AUD | A$ |
| Emirados Árabes | Dirham | AED | AED |
| Japão | Iene | JPY | ¥ |
| Coreia do Sul | Won | KRW | ₩ |
| Canadá | Dólar canadense | CAD | C$ |
| Dinamarca | Coroa dinamarquesa | DKK | DKK |
| Suécia | Coroa sueca | SEK | SEK |
| Noruega | Coroa norueguesa | NOK | NOK |
| México | Peso mexicano | MXN | MX$ |
| Índia | Rupia indiana | INR | ₹ |

## 3. AEROPORTOS POR REGIÃO (filtro de origem)

### Brasil
GRU, GIG, BSB, CNF, CWB, POA, SSA, REC, FOR, MAO, BEL, FLN, NAT, VCP

### Estados Unidos
JFK, LAX, ORD, MIA, SFO, ATL, DFW, EWR, IAH, SEA, BOS, DEN, IAD

### Reino Unido
LHR, LGW, STN, MAN, EDI, BHX, BRS, LTN

### Europa
CDG, ORY, FRA, MUC, AMS, MAD, BCN, FCO, MXP, LIS, OPO, ZRH, GVA, CPH, ARN, OSL

### Austrália
SYD, MEL, BNE, PER, ADL

### Emirados Árabes
DXB, AUH

### Japão
NRT, HND, KIX

### Coreia do Sul
ICN, GMP

## 4. PARA O SITE (FUTURO)

### Interface de personalização:
```
Tela inicial do site:
┌────────────────────────────────────┐
│  Escolha sua região:               │
│                                    │
│  🇧🇷 Brasil                        │
│  🇺🇸 Estados Unidos                │
│  🇬🇧 Reino Unido                   │
│  🇪🇺 Europa                        │
│     → Alemanha                     │
│     → França                       │
│     → Espanha                      │
│     → Itália                       │
│     → Portugal                     │
│     → Holanda                      │
│  🇨🇭 Suíça                         │
│  🇦🇺 Austrália                     │
│  🇦🇪 Emirados Árabes               │
│  🇯🇵 Japão                         │
│  🇰🇷 Coreia do Sul                 │
│  🇩🇰 Dinamarca                     │
│  🇸🇪 Suécia                        │
│  🇳🇴 Noruega                       │
│  🇨🇦 Canadá                        │
│  🇲🇽 México                        │
└────────────────────────────────────┘

Após seleção:
- Moeda ajustada automaticamente
- Aeroportos de origem filtrados
- Idioma da interface (PT, EN, ES, FR, DE, AR, JA, KO)
- Deals relevantes pra região
```

### Detecção automática (futuro):
- Detectar IP do visitante → sugerir país automaticamente
- Detectar idioma do navegador → sugerir idioma
- Cookie salva preferência pra próximas visitas

## 5. ORDEM DE IMPLEMENTAÇÃO

### Fase 1 (AGORA): Bot com seleção de moeda
- Comando /moeda ou botões no /start
- Conversão automática de preços
- Salvar preferência por usuário

### Fase 2: Filtro por região
- Deals filtrados por aeroporto de origem
- Feeds específicos por região
- Mais fontes de dados (Kiwi API com filtro por região)

### Fase 3: Multi-idioma
- Mensagens do bot em PT, EN, ES
- Tradução automática dos deals

### Fase 4: Site
- Landing page com seleção de região
- Dashboard personalizado
- Assinatura por região/moeda
