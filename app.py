from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

#--------------------------------------------------- Validação de Cadastro -----------------------------------------------------------------
@app.route('/validacao_cadastro', methods= ['POST'])
def validacao_cadastro():
    mensagem = ""
    if request.form['email'] != '':
        usuario = {
            "nome" : request.form['nome'],
            "email" : request.form['email'],
            "senha" : request.form['senha']
        }
        mensagem = "Sucesso"
        linhas = []
        jsonfile = []
        with open("cadastro.json", "r", encoding="UTF-8") as file:
            linhas = file.readlines()[:-1]
               
                
        with open("cadastro.json", "r", encoding="UTF-8") as file:
            conteudo2 = file.read()
            if conteudo2 != '':    
                jsonfile = json.loads(conteudo2)
        conteudo = ''
        for c in jsonfile: 
             if (request.form['email']) == c['email']:
                mensagem = "Email já cadastrado"
                return render_template('cadastro.html', mensagem=mensagem)
        if len(linhas) == 0:
                linhas.append('[')
                conteudo = json.dumps(usuario) + "\n]"
        else:
            conteudo = ',' + json.dumps(usuario) + "\n]"
        linhas.append(conteudo)
            
        with open("cadastro.json", "w", encoding="UTF-8") as file:
                file.writelines(linhas)
                
    return render_template('cadastro.html', mensagem=mensagem)

#------------------------------------------------------- Rota Principal ----------------------------------------------------------------------
@app.route('/principal')
def principal():
    return render_template('principal.html')

#-------------------------------------------------------- Rota Login ------------------------------------------------------------------------
@app.route('/')
def login():
    return render_template('login.html')
#------------------------------------------------------ Validação de Login -------------------------------------------------------------------
@app.route ('/validacao_login', methods = ['POST'])
def validacao_login():
    with open("cadastro.json", "r", encoding="UTF-8") as file:
        e_mail = file.read()
        emailjson = json.loads(e_mail)
        mensagem = ''
        print (request.form['email'])
        for usuario in emailjson:
            if (request.form['email'] == usuario['email']) and (request.form['senha'] == usuario['senha']):
                print( 'ok')
                return render_template('principal.html')
            else:
                mensagem = "Acesso negado! (Usuário  e ou senha inválidos)"
                return render_template('login.html', mensagem=mensagem)

#------------------------------------------------------- Rota Cadastro -------------------------------------------------------------------
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# -------------------------------------------------------- Rota Sobre Nós ---------------------------------------------------------------------
@app.route('/sobre')
def sobrenos():
    return render_template('sobrenos.html')

#----------------------------------------------------------- GLOSSÁRIO -------------------------------------------------------------------------
            # Caminho do arquivo JSON onde os termos serão armazenados definidos por uma CONSTANTE
JSON_GLOSSARIO = 'glossario.json'
def carregar_glossario():
    try:
        with open(JSON_GLOSSARIO, 'r', encoding= "UTF-8") as file:
            glossario = json.load(file)
    except FileNotFoundError:
        glossario = {}
    return glossario
#--------------------------------------Função para salvar termo e significado no glossario----------------------------------------------------
def salvar_glossario(glossario):
    with open(JSON_GLOSSARIO, 'w', encoding="UTF-8") as file:
        json.dump(glossario, file, indent=2)

# -----------------------------------------------------Rota do glossário----------------------------------------------------------------------
@app.route('/glossario')
def index():
    glossario = carregar_glossario()
    return render_template("glossario.html", glossario=glossario)

# -------------------------------------------- Adiciona e Altera, termo e siginificado glossário --------------------------------------------------------
@app.route('/adicionar', methods=['POST'])
def adicionar():
    termo = request.form['termo']
    significado= request.form['significado']    
    glossario = carregar_glossario()
    glossario[termo] = significado
    
    salvar_glossario(glossario)
    return redirect('/glossario')

#---------------------------------------------------- Deletar termo no glossário -------------------------------------------------------------
@app.route('/deletar/<termo>', methods=['POST'])
def deletar(termo):
    glossario = carregar_glossario()

    if termo in glossario:
        del glossario[termo]

    salvar_glossario(glossario)
    return redirect('/glossario')

# --------------------------------------------------------ATIVIDADES-------------------------------------------------------------------------------
# ******Constante recebendo o arquivo
JSON_ATIVIDADE = 'atividade.json'
# ---------------------------------------------Função para Ler o 'atividade.json'-----------------------------------------------------------------------------
def carregar_atividades():
    try:
        with open(JSON_ATIVIDADE, 'r', encoding= "UTF-8") as file:
            atividades = file.read()
            if atividades != '':
                atividades = json.loads(atividades)
    except FileNotFoundError:
        atividades = {}
    return atividades
# --------------------------------------------------- Salvar atividades --------------------------------------------------------------------------
def salvar_atividades(atividades):
    with open(JSON_ATIVIDADE, 'w', encoding="UTF-8") as file:
        json.dump(atividades, file, indent=2)
# --------------------------------------------------- Rota atividades --------------------------------------------------------------------------
@app.route('/atividades')
def lista_atividades():
    atividades = carregar_atividades()
    return render_template('atividades.html', atividades=atividades)

# --------------------------------------------------- Adicionar e Alterar atividade --------------------------------------------------------------------------
@app.route('/adicionar_atividade', methods=['POST'])
def adicionar_atividade():
    
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    atividades = carregar_atividades()
    atividades[titulo] = descricao
    
    salvar_atividades(atividades)
    return redirect('/atividades')

# ----------------------------------------------------- Deletar atividade ---------------------------------------------------------------------
@app.route('/deletar_atividade/<titulo>', methods=['POST'])
def deletar_atividade(titulo):
    atividades=carregar_atividades()
    if titulo in atividades:
        del atividades[titulo]
    salvar_atividades(atividades)
    return redirect('/atividades')

if __name__ == '__main__':
    app.run(debug=True)
