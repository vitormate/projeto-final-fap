from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .produto import Produto, db
from .usuario import Usuario, db
from .detalhamento_pedido import DetalhamentoPedido, db
from .pedido import Pedido, db