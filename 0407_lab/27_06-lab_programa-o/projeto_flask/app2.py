from flask import Flask, render_template
app = Flask(__name__)

@app.route("/produtos")
def home():
    produtos = ["maçã","banana","laranja"]
    logado = True
    return render_template ("home2.html", produtos = produtos, logado=logado)

if __name__ =='__main__':
    app.run(debug=True)

