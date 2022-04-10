from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import __version__ as sql_version

from src.blueprints.room import blueprint as room_blueprint
from src.blueprints.tenant import blueprint as tenant_blueprint
from src.blueprints.transaction import blueprint as transaction_blueprint

load_dotenv()
app = Flask(__name__)

app.register_blueprint(room_blueprint)
app.register_blueprint(tenant_blueprint)
app.register_blueprint(transaction_blueprint)

@app.route('/')
def greet():
    return {
        "msg": "Jai shree ram 🙏",
        "sql": sql_version
    }    
