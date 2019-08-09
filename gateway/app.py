#!/usr/bin/env python3

from flask import Flask
from apis.blueprint import blueprint as bp_apis
from index.blueprint import blueprint as bp_index
from core.nameko import rpc
from core.limiter import limiter
from dynaconf import settings

# Flask setup
app = Flask(__name__)
app.config.update(dict(NAMEKO_AMQP_URI=settings["rabbit_uri"],
                       NAMEKO_POOL_RECYCLE=settings["pool_recycle"]))

# Register Blueprints
app.register_blueprint(bp_apis)
app.register_blueprint(bp_index)

# Flask Limiter setup
limiter.init_app(app)

# Nameko setup
rpc.init_app(app)
