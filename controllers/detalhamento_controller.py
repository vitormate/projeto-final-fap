from flask import Blueprint, request, jsonify
from models import db, DetalhamentoPedido, Usuario, Produto

detalhamento_pedido_bp = Blueprint('detalhamento_pedido', __name__)

@detalhamento_pedido_bp.route('/criar_detalhamento_pedido', methods=['POST'])
def criar_detalhamento_pedido():
    data = request.json
    try:
        novo_detalhamento = DetalhamentoPedido(
            produto_id=data['produto_id'],
            quantidade=data['quantidade'],
            preco_unitario=data['preco_unitario'],
            usuario_id=data['usuario_id']
        )
        db.session.add(novo_detalhamento)
        db.session.commit()
        return jsonify({
            'id': novo_detalhamento.id,
            'produto_id': novo_detalhamento.produto_id,
            'quantidade': novo_detalhamento.quantidade,
            'preco_unitario': novo_detalhamento.preco_unitario,
            'usuario_id': novo_detalhamento.usuario_id
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Campo necessário {str(e)} está faltando.'}), 400

@detalhamento_pedido_bp.route('/detalhamentos_pedido', methods=["GET"])
def lista_de_detalhamentos_pedido():
    detalhamentos = DetalhamentoPedido.query.all()
    return jsonify([{
        'id': d.id,
        'produto_id': d.produto_id,
        'quantidade': d.quantidade,
        'preco_unitario': d.preco_unitario,
        'usuario_id': d.usuario_id
    } for d in detalhamentos]), 200

@detalhamento_pedido_bp.route('/detalhamentos_pedido/<int:id>', methods=["PUT"])
def atualizar_detalhamento_pedido(id):
    data = request.json
    detalhamento = DetalhamentoPedido.query.get(id)
    if not detalhamento:
        return jsonify({'Message':'Detalhamento de pedido não encontrado'}), 404
    
    detalhamento.produto_id = data['produto_id']
    detalhamento.quantidade = data['quantidade']
    detalhamento.preco_unitario = data['preco_unitario']
    detalhamento.usuario_id = data['usuario_id']
    db.session.commit()
    return jsonify({
        'id': detalhamento.id,
        'produto_id': detalhamento.produto_id,
        'quantidade': detalhamento.quantidade,
        'preco_unitario': detalhamento.preco_unitario,
        'usuario_id': detalhamento.usuario_id
    }), 200

@detalhamento_pedido_bp.route('/detalhamentos_pedido/<int:id>', methods=["DELETE"])
def deletar_detalhamento_pedido(id):
    detalhamento = DetalhamentoPedido.query.get(id)
    if not detalhamento:
        return jsonify({'Message':'Detalhamento de pedido não encontrado'}), 404
    
    db.session.delete(detalhamento)
    db.session.commit()
    return jsonify({'Message':'Detalhamento de pedido deletado com sucesso'}), 200
