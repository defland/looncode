# !/usr/bin/python
# coding:utf-8
from application import app


if __name__=='__main__':
    app.run(debug=app.config['DEBUG'])

