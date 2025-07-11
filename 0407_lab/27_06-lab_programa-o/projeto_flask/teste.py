from flask import Flask, session, redirect, url_for, request
app=Flask(__name__)
app.secret_key ='uma-chave-secreta-muito-segura'
@app.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    session['username']=username
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return f <h1>'Bem-vindo de volta,{session['username']}!'</h1>
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username',None)
    return 'Você foi deslogado'

@app.route('/')
def home():
    return'Pagina inicial. faça login para acessar seu perfil.'
