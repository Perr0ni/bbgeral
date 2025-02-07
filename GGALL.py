import requests
import json
import warnings
import random
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

TOKEN = "6327570032:AAFReiOZ3-Z7eI9gyWoZgRYLAGqLdfI-vqw"  # Substitua pelo seu token
OWNER_ID = 5340565783  # ID do dono do bot (somente esse pode adicionar permissões)
PERMISSOES_FILE = "permissoes.json"  # Arquivo onde os IDs autorizados serão armazenados
BLOQUEADAS_FILE = "bins_bloqueadas.json"  # Arquivo onde as BINs bloqueadas serão armazenadas

# Dicionário para armazenar o tempo do último teste de cada usuário
ultimo_teste = {}

# Função para carregar os usuários permitidos
def carregar_permissoes():
    try:
        with open(PERMISSOES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar os usuários permitidos
def salvar_permissoes(permitidos):
    with open(PERMISSOES_FILE, "w") as file:
        json.dump(permitidos, file)

# Função para carregar as BINs bloqueadas
def carregar_bins_bloqueadas():
    try:
        with open(BLOQUEADAS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar as BINs bloqueadas
def salvar_bins_bloqueadas(bins_bloqueadas):
    with open(BLOQUEADAS_FILE, "w") as file:
        json.dump(bins_bloqueadas, file)

# Comando para adicionar um usuário autorizado
async def add_perm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if update.message.chat.type == "private":
        await update.message.reply_text("🚫 Este bot não pode ser usado em chats privados.")
        return

    if user_id != OWNER_ID:
        await update.message.reply_text("❌ Você não tem permissão para usar este comando.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Use: `/addperm <ID>` para adicionar um usuário autorizado.", parse_mode="HTML")
        return

    novo_id = context.args[0]
    
    try:
        novo_id = int(novo_id)
    except ValueError:
        await update.message.reply_text("⚠️ O ID deve ser um número válido.")
        return

    permitidos = carregar_permissoes()
    
    if novo_id in permitidos:
        await update.message.reply_text(f"⚠️ O usuário `{novo_id}` já está autorizado.", parse_mode="Markdown")
        return

    permitidos.append(novo_id)
    salvar_permissoes(permitidos)
    
    await update.message.reply_text(f"✅ O usuário `{novo_id}` foi autorizado!", parse_mode="Markdown")

# Comando para remover um usuário autorizado
async def rem_perm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if update.message.chat.type == "private":
        await update.message.reply_text("🚫 Este bot não pode ser usado em chats privados.")
        return

    if user_id != OWNER_ID:
        await update.message.reply_text("❌ Você não tem permissão para usar este comando.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Use: `/remperm <ID>` para remover um usuário autorizado.", parse_mode="HTML")
        return

    id_remover = context.args[0]
    
    try:
        id_remover = int(id_remover)
    except ValueError:
        await update.message.reply_text("⚠️ O ID deve ser um número válido.")
        return

    permitidos = carregar_permissoes()
    
    if id_remover not in permitidos:
        await update.message.reply_text(f"⚠️ O usuário `{id_remover}` não está na lista de autorizados.", parse_mode="Markdown")
        return

    permitidos.remove(id_remover)
    salvar_permissoes(permitidos)
    
    await update.message.reply_text(f"✅ O usuário `{id_remover}` foi removido da lista de autorizados!", parse_mode="Markdown")

# Comando para adicionar uma BIN à lista de bloqueio
async def add_bin_bloqueada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if update.message.chat.type == "private":
        await update.message.reply_text("🚫 Este bot não pode ser usado em chats privados.")
        return

    if user_id != OWNER_ID:
        await update.message.reply_text("❌ Você não tem permissão para usar este comando.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Use: `/addbin <BIN>` para adicionar uma BIN à lista de bloqueio.", parse_mode="HTML")
        return

    bin_bloqueada = context.args[0]
    
    if not bin_bloqueada.isdigit() or len(bin_bloqueada) < 6:
        await update.message.reply_text("⚠️ A BIN deve ter pelo menos 6 dígitos numéricos.")
        return

    bins_bloqueadas = carregar_bins_bloqueadas()
    
    if bin_bloqueada in bins_bloqueadas:
        await update.message.reply_text(f"⚠️ A BIN `{bin_bloqueada}` já está bloqueada.", parse_mode="Markdown")
        return

    bins_bloqueadas.append(bin_bloqueada)
    salvar_bins_bloqueadas(bins_bloqueadas)
    
    await update.message.reply_text(f"✅ A BIN `{bin_bloqueada}` foi adicionada à lista de bloqueio!", parse_mode="Markdown")

# Comando para remover uma BIN da lista de bloqueio
async def rem_bin_bloqueada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if update.message.chat.type == "private":
        await update.message.reply_text("🚫 Este bot não pode ser usado em chats privados.")
        return

    if user_id != OWNER_ID:
        await update.message.reply_text("❌ Você não tem permissão para usar este comando.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Use: `/rembin <BIN>` para remover uma BIN da lista de bloqueio.", parse_mode="HTML")
        return

    bin_bloqueada = context.args[0]
    
    bins_bloqueadas = carregar_bins_bloqueadas()
    
    if bin_bloqueada not in bins_bloqueadas:
        await update.message.reply_text(f"⚠️ A BIN `{bin_bloqueada}` não está na lista de bloqueio.", parse_mode="Markdown")
        return

    bins_bloqueadas.remove(bin_bloqueada)
    salvar_bins_bloqueadas(bins_bloqueadas)
    
    await update.message.reply_text(f"✅ A BIN `{bin_bloqueada}` foi removida da lista de bloqueio!", parse_mode="Markdown")

# Função para extrair informações do BIN
def extract_between(string, start_delimiter, end_delimiter):
    start_pos = string.find(start_delimiter)
    if start_pos == -1:
        return None
    start_pos += len(start_delimiter)
    end_pos = string.find(end_delimiter, start_pos)
    if end_pos == -1:
        return None
    return string[start_pos:end_pos]

# Algoritmo de Luhn para gerar números de cartão válidos
def luhn_checksum(card_number):
    digits = [int(d) for d in ''.join(map(str, card_number))]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10

def complete_credit_card(partial_number, is_amex=False):
    card_number = [int(d) for d in partial_number]
    # Define o comprimento do cartão: 15 dígitos para Amex, 16 para outros
    target_length = 15 if is_amex else 16
    while len(card_number) < target_length - 1:  # -1 para deixar espaço para o dígito verificador
        card_number.append(random.randint(0, 9))
    checksum = (10 - luhn_checksum(card_number + [0])) % 10
    card_number.append(checksum)
    return ''.join(map(str, card_number))

def generate_credit_cards(partial_number, month, year, cvv, count=1):
    cards = []
    full_year = f"20{year}"  # Convert to full year format
    # Verifica se o BIN é de um cartão American Express (começa com 34 ou 37)
    is_amex = partial_number.startswith("34") or partial_number.startswith("37")
    for _ in range(count):  # Sem limite para o dono do bot
        complete_card = complete_credit_card(partial_number, is_amex)
        cards.append(f"{complete_card}|{month}|{full_year}|{cvv}")
    return cards

# Comando principal /GGALL para gerar e testar cartões
async def ggall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_type = update.message.chat.type
    permitidos = carregar_permissoes()

    # Bloqueia o uso no privado
    if chat_type == "private":
        await update.message.reply_text("🚫 Este bot não pode ser usado em chats privados.")
        return

    if user_id not in permitidos and user_id != OWNER_ID:
        await update.message.reply_text("⛔ Você não tem permissão para usar este bot.", reply_to_message_id=update.message.message_id)
        return

    # Verifica se o usuário já fez um teste recentemente
    if user_id in ultimo_teste:
        tempo_passado = time.time() - ultimo_teste[user_id]
        if tempo_passado < 120:  # 120 segundos de timeout
            tempo_restante = int(120 - tempo_passado)
            await update.message.reply_text(
                f"⏳ Aguarde {tempo_restante} segundos para iniciar um novo teste.",
                reply_to_message_id=update.message.message_id
            )
            return

    try:
        if not context.args:
            raise ValueError("Formato inválido.")

        bin_cc = context.args[0]
        mes = context.args[1]
        ano = context.args[2]
        cvv = context.args[3]
        quantidade = int(context.args[4]) if len(context.args) > 4 else 1

        # Extrai os 6 primeiros dígitos (BIN) do cartão
        bin_cartao = bin_cc[:6]

        # Verifica se a BIN está bloqueada
        bins_bloqueadas = carregar_bins_bloqueadas()
        if bin_cartao in bins_bloqueadas:
            await update.message.reply_text(f"🚫 A BIN `{bin_cartao}` está bloqueada e não pode ser testada.", parse_mode="Markdown")
            return

        # Validação do BIN (10 a 12 dígitos)
        if not (10 <= len(bin_cc) <= 12) or not bin_cc.isdigit():
            raise ValueError("O BIN deve ter entre 10 e 12 dígitos.")

        # Validação do MES (1 a 12)
        if not mes.isdigit() or not (1 <= int(mes) <= 12):
            raise ValueError("O MES deve ser um número entre 1 e 12.")

        # Validação do ANO (2 dígitos)
        if not ano.isdigit() or len(ano) != 2:
            raise ValueError("O ANO deve ser um número de 2 dígitos.")

        # Validação do CVV (3 ou 4 dígitos)
        if not cvv.isdigit() or not (3 <= len(cvv) <= 4):
            raise ValueError("O CVV deve ter 3 ou 4 dígitos.")

        # Limite de cartões: 3 para usuários autorizados, sem limite para o dono
        if user_id != OWNER_ID and quantidade > 3:
            raise ValueError("O limite é de 3 cartões por comando.")

    except ValueError as e:
        await update.message.reply_text(
            f"⚠️ {str(e)}\n"
            "Use: `/GGALL <BIN> <MES> <ANO> <CVV> [QUANTIDADE]`\n"
            "Exemplo: `/GGALL 4586430023 08 25 789 2`",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )
        return

    # Atualiza o tempo do último teste APÓS todas as validações
    ultimo_teste[user_id] = time.time()

    # Resposta imediata no chat
    aguardando_msg = await update.message.reply_text(
        "⏳ <b>Gerando e testando cartões... Aguarde um momento.</b>",
        parse_mode="HTML",
        reply_to_message_id=update.message.message_id
    )

    # Gera os cartões
    cartoes = generate_credit_cards(bin_cc, mes, ano, cvv, quantidade)

    headers = {
        'Host': 'xisvideo.store',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    respostas = []

    for lista in cartoes:
        separar = lista.split("|")

        if len(separar) < 4:
            respostas.append(f"⚠️ Formato incorreto: `{lista}`")
            continue

        cc, mes, ano, cvv = separar[:4]

        bin_cc = cc[:6] if len(cc) >= 6 else None
        bin_info = None
        if bin_cc:
            params = {'lista': bin_cc}
            response = requests.get('https://xisvideo.store/bin/api.php', params=params, headers=headers, verify=False)
            bin_info = response.text if response.status_code == 200 else None

        bandeira = extract_between(bin_info, 'bandeira":"', '","') or "Desconhecido"
        tipo = extract_between(bin_info, 'tipo":"', '","') or "Desconhecido"
        categoria = extract_between(bin_info, 'categoria":"', '","') or "Desconhecido"
        banco = extract_between(bin_info, 'banco":"', '","') or "Desconhecido"
        pais = extract_between(bin_info, 'pais":"', '","') or "Desconhecido"
        codigo_pais = extract_between(bin_info, 'codigo_pais":"', '","') or "Desconhecido"

        response = requests.get(f'https://xisvideo.store/Suite171/api.php?lista={cc}|{mes}|{ano}|{cvv}', headers=headers, verify=False)
        pegaretorno = response.text
        print(pegaretorno)
        Retorno = extract_between(response.text, 'Retorno: ', '</') or "Sem retorno"

        if 'Aprovada' in pegaretorno:
            respostas.append(f"✅ <b>Aprovada {cc}|{mes}|{ano}|{cvv} ➔ Retorno: {Retorno} ➔ {bandeira} {tipo} {categoria} {banco} {pais} {codigo_pais} ➔ @Perr0ni</b>")
        elif 'Reprovada' in pegaretorno:
            respostas.append(f"❌ <b>Reprovada {cc}|{mes}|{ano}|{cvv} ➔ Retorno: {Retorno} ➔ {bandeira} {tipo} {categoria} {banco} {pais} {codigo_pais} ➔ @Perr0ni</b>")
        else:
            respostas.append(f"⚠️ ERRO DESCONHECIDO: {cc}|{mes}|{ano}|{cvv}")

    # Obtém o username do usuário que fez o teste
    username = update.message.from_user.username
    if username:
        user_mention = f"@{username}"
    else:
        user_mention = update.message.from_user.first_name  # Usa o nome se o username não estiver disponível

    # Junta "Teste finalizado" com os resultados e o username
    resposta_final = f"✅ <b>Teste finalizado para o usuário {user_mention}.</b>\n\n" + "\n\n".join(respostas)

    await aguardando_msg.edit_text(resposta_final, parse_mode="HTML")

# Comando /start sem botão
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Envie `/GGALL <BIN> <MES> <ANO> <CVV> [QUANTIDADE]` para gerar e testar cartões.\n"
        "Exemplo: `/GGALL 4586430023 08 25 789 2`",
        parse_mode="Markdown",
        reply_to_message_id=update.message.message_id
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("GGALL", ggall))
    app.add_handler(CommandHandler("addperm", add_perm))
    app.add_handler(CommandHandler("remperm", rem_perm))
    app.add_handler(CommandHandler("addbin", add_bin_bloqueada))
    app.add_handler(CommandHandler("rembin", rem_bin_bloqueada))

    print("Bot está rodando...")
    app.run_polling()