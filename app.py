from flask import Flask, render_template, session, json

from blueprints.auth.route import auth_blueprint
from blueprints.report.route import report_blueprint
from blueprints.menu.route import menu_blueprint
from blueprints.query.route import query_blueprint
from blueprints.testing.route import testing_blueprint
# from blueprints.client.route import client_blueprint

app = Flask(__name__)

with open("./data/dbaccess.json") as f:
    app.config['db_access'] = json.load(f)

app.secret_key = 'janfckjnjswJCFkjnkj'

app.register_blueprint(query_blueprint, url_prefix='/query')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(report_blueprint, url_prefix='/report')
app.register_blueprint(menu_blueprint, url_prefix='/')
app.register_blueprint(testing_blueprint, url_prefix='/testing')

@app.route('/logout')
def exit_func():
    session.clear()
    return render_template("logout.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)