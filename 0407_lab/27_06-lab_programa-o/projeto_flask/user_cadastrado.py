from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session

app = Flask(__name__)
app.secret_key ='uma-chave-secreta-muito-segura'

USUARIO_CADASTRADO="admin"
SENHA_CADASTRADO="123"

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        usuario = request.form.get('nome_login')
        senha = request.form.get('pass_login')

        if usuario == USUARIO_CADASTRADO and senha == SENHA_CADASTRADO:
            resposta = make_response(redirect(url_for('bemvindo')))
            resposta.set_cookie('username', usuario, max_age=60*30)
            return resposta
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', "erro")
            return redirect(url_for('login'))

    return render_template('login1.html')



@app.route('/bemvindo', methods=['GET', 'POST'])
def bemvindo():
    username = request.cookies.get('username')
    novotema=request.cookies.get("tema","#FFFFFF")

    if not username:
        return redirect(url_for('login'))

    session.permanent=True
    if 'contador' in session:
        session['contador']+=1
    else:
        session['contador']=1
    
    acessos=session['contador']

    return render_template('bemvindo_form.html', user=username, novotema=novotema, acessos=acessos)





@app.route('/logout')
def logout():
    session.clear()

    flash("Você foi deslogado", "info")

    resposta = make_response(redirect(url_for('login')))

    resposta.set_cookie('username', '', expires=0)

    return resposta




@app.route('/tema', methods=['GET', 'POST'])
def tema():
    username = request.cookies.get('username')
    # novotema=request.form.get('tema')

    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        novotema = request.form.get('tema')
        if not novotema:
            flash("Nenhum tema foi selecionado", "erro")
            return redirect(url_for('bemvindo'))

        resposta = make_response(redirect(url_for('bemvindo')))
        resposta.set_cookie('tema', novotema, max_age=60*30)
        return resposta
    return redirect(url_for('bemvindo'))




@app.route('/tema_noticias', methods=['GET', 'POST'])
def tema_noticias():
    username = request.cookies.get('username')
    # novotema=request.form.get('tema_noticias')

    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        novotema_noticias = request.form.get('tema_noticias')
        if not novotema_noticias:
            flash("Nenhum tema foi selecionado", "erro")
            return redirect(url_for('bemvindo'))

        resposta = make_response(redirect(url_for('noticias')))
        resposta.set_cookie('tema_noticias', novotema_noticias, max_age=60*30)
        return resposta
    return redirect(url_for('noticias'))


@app.route('/noticias', methods=['GET','POST'])
def noticias():
    username = request.cookies.get('username')
    # novotema_noticias=request.cookies.get("tema_noticias","#fff0f5")
    novotema_noticias=request.cookies.get("tema_noticias")


    if not username:
        flash("acesso negado", "erro")
        return redirect(url_for('login'))

    return render_template('portal_noticia.html', user=username, novotema_noticias=novotema_noticias )



@app.route('/esportes')
def esportes():
    return render_template('esportes.html')

@app.route('/lazer')
def lazer():
    return render_template('lazer.html')

@app.route('/entretenimento')
def entretenimento():
    return render_template('entretenimento.html')




if __name__ == '__main__':
    app.run(debug=True)



# cookie é uma variavel local, experiencias do usuario

# tela login, bem vindo

#requwst.form, puxa as varieveis direto do formulario



