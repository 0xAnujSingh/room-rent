from flask import Blueprint, request
from sqlalchemy.orm import Session
from sqlalchemy import select, update 

from src.db import engine
from src.model import Transaction

from datetime import datetime

blueprint = Blueprint('transacation', 'transaction')

def convertDate(date_str):
    date_format = "%d/%m/%y"

    return datetime.strptime(date_format, date_str)

@blueprint.route('/transaction', methods = ['GET'])
def  tenantTransaction():
    pass

@blueprint.route('/transaction/<transactionId>', methods = ['GET'])
def getTransactionById(transactionId):
    pass

@blueprint.route('/transaction/', methods = ['POST'])
def transactionDesc():
    pass