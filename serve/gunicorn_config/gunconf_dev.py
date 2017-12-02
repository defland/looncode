#coding:utf-8
import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '127.0.0.1:8888' # dev的端口
pidfile = 'application/doc/tmp/gunicorn.pid'
logfile = 'application/doc/tmp/debug.log'
errorlog = "application/doc/tmp/error.log"

timeout = 60

#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1 
worker_class = '' 
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
