#coding:utf-8
from flask import Flask 
from config.config import config # 引入字典


def create_app():  
    app=Flask(__name__)  
    app.config.from_object(config["default"])  

    return app  
app = create_app()


# 从视图引入路由
import application.view




