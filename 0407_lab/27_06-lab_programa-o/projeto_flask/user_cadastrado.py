from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

USUARIO_CADASTRADO="admin"
SENHA_CADASTRADO="123"

@app.route("/login", methods=['GET', 'POST'])
def login():
    mensagem = ""

    if request.method=="POST":

        usuario = request.form.get('nome_login')
        senha = request.form.get('pass_login')

        if usuario == USUARIO_CADASTRADO and senha == SENHA_CADASTRADO:
            resposta = make_response(redirect(url_for('bemvindo')))
            resposta.set_cookie('username', usuario, max_age = 60*10)

            return resposta
        else:
            #'texto com aspas/'simples/''+'/''
            mensagem = "Usuario ou senha inválidos. Tente novamente."

    return render_template('login1.html', erro=mensagem) 

@app.route('/bemvindo', methods=['GET', 'POST'])
def bemvindo():
   username = request.cookies.get('username')
   novacor="#00FF00"
   if not username:
      return redirect(url_for('login'))
   return render_template('bemvindo_form.html', user=username, novacor="#00FF00")


@app.route('/logout')
def logout():
    resposta=make_response(redirect(url_for('login')))

    resposta.set_cookie('username', '', expires=0)
    #deixar de existir agr, nesse ponto

    return resposta

@app.route('/cor', methods=['GET', 'POST'])
def cor():
   username = request.cookies.get('username')
   novacor=request.form.get('cor')
   if not username:
      return redirect(url_for('login'))
   
   return render_template('bemvindo_form.html', user=username, novacor=novacor)




if __name__ == '__main__':
    app.run(debug=True)



# cookie é uma variavel local, experiencias do usuario

# tela login, bem vindo

#requwst.form, puxa as varieveis direto do formulario



