bind = "0.0.0.0:5010"
wsgi_app = "api:app"
reload = True
accesslog = '-'
workers = 3
graceful_timeout = 30
timeout = 30

