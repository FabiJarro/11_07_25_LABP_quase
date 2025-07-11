from flask import Flask, render_template
app = Flask(__name__)

@app.route("/user/<username>")
def profile(username):
    return render_template("profile.html", user=username)
if __name__=='__main__':
    app.run(debug=True)

