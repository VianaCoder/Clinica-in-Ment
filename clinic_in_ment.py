import re
from flask import Flask, make_response, request, render_template
from flask.helpers import flash
from gsConnector import *

app = Flask('flaskconftest', template_folder='public', static_folder='public/static')

#Rota para home
@app.route('/home', methods=['GET'])
def home():
    if request.method == 'GET':
        id = request.cookies.get('ID')
        scheduled = gsConnector().getScheduled()
        buttons = []
        print(id)
        for i in scheduled:
            print(i)
            if str(i[5]) == str(id):
                buttons.append(i[0])
        return render_template('home.html', buttons=buttons)

#Rota para o Index
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

#Rota para tela de login
@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

#Rota para tela de register
@app.route('/register', methods=['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
@app.route('/churned', methods=['GET'])
def churned():
    if request.method == 'GET':
        return render_template('churned.html')
    
@app.route('/completed', methods=['GET'])
def completed():
    if request.method == 'GET':
        return render_template('completed.html')

@app.route('/reagendamento', methods=['GET'])
def ceagendamento():
    if request.method == 'GET':
        return render_template('reagendamento.html')
    
@app.route('/cancelamento', methods=['GET'])
def cancelamento():
    if request.method == 'GET':
        return render_template('cancelamento.html')


@app.route('/scheduled', methods=['GET'])
def scheduled():
    if request.method == 'GET':
        date = request.args.get('date')
        id = request.cookies.get('ID')
        scheduled = gsConnector().getScheduled()
        print(id)
        for i in scheduled:
            print(i)
            if str(i[5]) == str(id):
                if str(i[0] ==  date):
                    doctor = i[4]
        return render_template('scheduled.html', message = date, doctor=doctor)  

@app.route('/confirm-pagamento', methods=['GET'])
def confirmpagamento():
    if request.method == 'GET':
        return render_template('confirm-pagamento.html')  
    
@app.route('/pix', methods=['GET'])
def pix():
    if request.method == 'GET':
        return render_template('pix.html') 
    
@app.route('/payment', methods=['GET'])
def pay():
    if request.method == 'GET':
        return render_template('payment.html') 
    
@app.route('/boleto', methods=['GET'])
def boleto():
    if request.method == 'GET':
        return render_template('boleto.html')
    
@app.route('/drjone', methods=['GET'])
def drjone():
    if request.method == 'GET':
        return render_template('drjone.html')
    
@app.route('/hours', methods=['GET'])
def hours():
    if request.method == 'GET':
        day = request.args.get('day')
        print(day)
        return render_template('hours.html', day=day)
    
    
@app.route('/agendamento', methods=['GET'])
def agendamento():
    if request.method == 'GET':
        day = request.args.get('day')
        hour = request.args.get('hour')
        return render_template('agendamento.html', day=day, hour=hour)
    
@app.route('/agendamento-function', methods=['POST'])
def setSchedule():
    if request.method == 'POST':
        name = request.form.get('Name')
        rg = request.form.get('RG')
        idade = request.form.get('Idade')
        hour = request.form.get('Hour')
        medico = request.form.get('Medico')
        id = request.cookies.get("ID")
        
    dataBase = gsConnector()
    
    scheduled = dataBase.getScheduled()
    
    for i in scheduled:
        if i[0] == hour:
            return render_template('aviso.html', message="Horário ocupado, tente novamente!")
    
    try :
        dataBase.setSchedule([[hour, name, rg, idade, medico, id]])
        script = "alert(\"Consulta Agendada\""
        return render_template('sucess.html')
    except:
        return render_template('aviso.html', message="Erro ao agendar, tente novamente!")

@app.route('/register-function', methods=['POST'])
def register_api():
    if request.method == 'POST':
        name = request.form.get('Name')
        rg = request.form.get('RG')
        email = request.form.get('Email')
        passwd1 = request.form.get('Password1')
        passwd2 = request.form.get('Password2')
        
    if passwd1 != passwd2:
        return render_template('aviso.html', message="Senhas diferentes, tente novamente!")
        
    dataBase = gsConnector()
    try :
        dataBase.newUser([[name, rg, email, passwd1]])
        resp = make_response(render_template('home.html', message=name))
        resp.set_cookie('ID', rg)
        return resp
    except:
        return render_template('aviso.html', message="Erro ao cadastrar, tente novamente!")
    
@app.route('/login-function', methods=['POST'])
def login_api():
    if request.method == 'POST':
        email = request.form.get('Email')
        passwd = request.form.get('Password')
        
    dataBase = gsConnector()
    try:
        logins = dataBase.getUser()
    except:
        return render_template('aviso.html', message="Erro no banco de dados, tente novamente!")

    print(logins)

    for i in logins:
        print(i)
        if i[2] == email:
            if i[3] == passwd:
                print(email, passwd)
                resp = make_response(render_template('home.html', message=i[0]))
                resp.set_cookie('ID', i[1])
                return resp
            else:
                return render_template('aviso.html', message="Senha incorreta, tente novamente!")

    return render_template('aviso.html', message="Verifique seu login, tente novamente!")

app.run(host="0.0.0.0")