from . import db

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', back_populates='pedidos')
    
    # Relacionamento com DetalhamentoPedido
    detalhamentos = db.relationship('DetalhamentoPedido', back_populates='pedido', cascade='all, delete-orphan', lazy=True)
