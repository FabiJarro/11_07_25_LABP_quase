from flask import Flask, render_template, request, session, redirect, url_for
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# --- Lógica do Jogo Adivinhar o Número ---

LIMITE_INFERIOR = 1
LIMITE_SUPERIOR = 100

def inicializar_adivinhar_numero():
    """Inicializa ou reinicia o estado do jogo Adivinhar o Número."""
    session['numero_secreto_an'] = random.randint(LIMITE_INFERIOR, LIMITE_SUPERIOR)
    session['tentativas_an'] = 0
    session['mensagem_an'] = f"Adivinhe um número entre {LIMITE_INFERIOR} e {LIMITE_SUPERIOR}."
    session['jogo_an_terminado'] = False
    session['ultimo_palpite_an'] = None # Para mostrar o último palpite

@app.route('/adivinhar_numero', methods=['GET', 'POST'])
def adivinhar_numero():
    """Rota principal para o jogo Adivinhar o Número."""
    if 'numero_secreto_an' not in session or request.form.get('novo_jogo_an'):
        inicializar_adivinhar_numero()
        if request.form.get('novo_jogo_an'):
            return redirect(url_for('adivinhar_numero')) # Redireciona para limpar o POST

    if request.method == 'POST' and not session.get('jogo_an_terminado'):
        if 'palpite_usuario' in request.form:
            try:
                palpite = int(request.form['palpite_usuario'])
                session['ultimo_palpite_an'] = palpite
                session['tentativas_an'] += 1
                
                numero_secreto = session.get('numero_secreto_an')

                if palpite < LIMITE_INFERIOR or palpite > LIMITE_SUPERIOR:
                    session['mensagem_an'] = f"Por favor, insira um número entre {LIMITE_INFERIOR} e {LIMITE_SUPERIOR}."
                elif palpite < numero_secreto:
                    session['mensagem_an'] = f"O número {palpite} é muito baixo. Tente um maior!"
                elif palpite > numero_secreto:
                    session['mensagem_an'] = f"O número {palpite} é muito alto. Tente um menor!"
                else: # Acertou!
                    session['mensagem_an'] = f"Parabéns! Você acertou o número {numero_secreto} em {session['tentativas_an']} tentativa(s)!"
                    session['jogo_an_terminado'] = True
                
            except ValueError:
                session['mensagem_an'] = "Entrada inválida. Por favor, insira um número inteiro."
                session['ultimo_palpite_an'] = request.form.get('palpite_usuario', '') # Mantém o valor inválido para mostrar
            
            session.modified = True
            return redirect(url_for('adivinhar_numero')) # Redireciona para GET

    # Para GET request ou após redirect
    # Consome a mensagem para não a mostrar repetidamente se o utilizador atualizar a página sem jogar
    # No entanto, para este jogo, é útil manter a mensagem da última tentativa.
    # Se preferir limpar, pode usar session.pop('mensagem_an', "...")

    return render_template('adivinhar_numero.html',
                           mensagem=session.get('mensagem_an'),
                           jogo_terminado=session.get('jogo_an_terminado', False),
                           tentativas=session.get('tentativas_an', 0),
                           limite_inferior=LIMITE_INFERIOR,
                           limite_superior=LIMITE_SUPERIOR,
                           ultimo_palpite=session.get('ultimo_palpite_an'))

if __name__ == '__main__':
    # Para executar:
    # 1. Flask instalado (pip install Flask).
    # 2. Pasta 'templates' com 'adivinhar_numero.html'.
    # 3. Execute este arquivo Python.
    # 4. Navegador: http://127.0.0.1:5000/adivinhar_numero
    app.run(debug=True) # Porta diferente
