from flask import Blueprint

blueprint = Blueprint(
    'crypto_blueprint',
    __name__,
    url_prefix='/crypto',
    template_folder='templates',
    static_folder='static'
)
