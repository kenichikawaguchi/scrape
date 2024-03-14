import sqlalchemy
from sqlalchemy import select
from setting import Inspector, session
from company import Company
from flask import Flask, render_template, request

from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    result = session.query(Company).all()
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 10
    pagination =Pagination(page=page, per_page=per_page, total=len(result))
    start = (page - 1) * per_page
    end = start + per_page
    params = result[start:end]
    return render_template('index.html', params=params, pagination=pagination)


@app.route("/info", methods=["GET"])
def info():
    result = session.query(Company).all()
    page = int(request.args.get(get_page_parameter(), 1))
    per_page = 100
    pagination =Pagination(page=page, per_page=per_page, total=len(result))
    start = (page - 1) * per_page
    end = start + per_page
    params = result[start:end]
    return render_template('info.html', params=params, pagination=pagination)
