from . import transactions_blp
from services.paystack import pay_stack
from flask import request
from logger import logger
from connections.redis_connection import redis_conn
import json


# resolve account
@transactions_blp.route("/resolve_account", methods=["POST"])
def resolve_account():
    data = request.get_json()
    account_number = data.get("account_number")
    bank_code = data.get("bank_code")
    logger.info(f"Account number: {account_number}, Bank code: {bank_code}")
    res = pay_stack.resolve_account(account_number, bank_code)
    logger.info(f"Resolved account: {res}")
    redis_conn.set(bank_code, json.dumps(res), 200)
    return res
