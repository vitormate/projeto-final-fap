from flask import Blueprint, request, jsonify
from models import db, Pedido, Usuario, DetalhamentoPedido

pedido_bp = Blueprint('pedidos', __name__)

@pedido_bp.route('/criar_pedido', methods=['POST'])
def criar_pedido():
    data = request.json
    try:
        novo_pedido = Pedido(
            descricao=data.get('descricao'),
            usuario_id=data['usuario_id']
        )
        db.session.add(novo_pedido)
        db.session.commit()
        
        # Adicionar detalhamentos de pedido, se houver
        detalhamentos = data.get('detalhamentos', [])
        for detalhamento in detalhamentos:
            novo_detalhamento = DetalhamentoPedido(
                produto_id=detalhamento['produto_id'],
                quantidade=detalhamento['quantidade'],
                preco_unitario=detalhamento['preco_unitario'],
                pedido_id=novo_pedido.id
            )
            db.session.add(novo_detalhamento)
        
        db.session.commit()
        
        return jsonify({
            'id': novo_pedido.id,
            'descricao': novo_pedido.descricao,
            'usuario_id': novo_pedido.usuario_id,
            'detalhamentos': [{
                'id': d.id,
                'produto_id': d.produto_id,
                'quantidade': d.quantidade,
                'preco_unitario': d.preco_unitario
            } for d in novo_pedido.detalhamentos]
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Campo necessário {str(e)} está faltando.'}), 400

@pedido_bp.route('/pedidos', methods=["GET"])
def lista_de_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([{
        'id': p.id,
        'descricao': p.descricao,
        'usuario_id': p.usuario_id,
        'detalhamentos': [{
            'id': d.id,
            'produto_id': d.produto_id,
            'quantidade': d.quantidade,
            'preco_unitario': d.preco_unitario
        } for d in p.detalhamentos]
    } for p in pedidos]), 200

@pedido_bp.route('/pedidos/<int:id>', methods=["PUT"])
def atualizar_pedido(id):
    data = request.json
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'Message':'Pedido não encontrado'}), 404
    
    pedido.descricao = data.get('descricao', pedido.descricao)
    pedido.usuario_id = data.get('usuario_id', pedido.usuario_id)
    
    # Atualizar detalhamentos, se houver
    detalhamentos = data.get('detalhamentos', [])
    for detalhamento_data in detalhamentos:
        detalhamento_id = detalhamento_data.get('id')
        if detalhamento_id:
            detalhamento = DetalhamentoPedido.query.get(detalhamento_id)
            if detalhamento:
                detalhamento.produto_id = detalhamento_data.get('produto_id', detalhamento.produto_id)
                detalhamento.quantidade = detalhamento_data.get('quantidade', detalhamento.quantidade)
                detalhamento.preco_unitario = detalhamento_data.get('preco_unitario', detalhamento.preco_unitario)
            else:
                novo_detalhamento = DetalhamentoPedido(
                    produto_id=detalhamento_data['produto_id'],
                    quantidade=detalhamento_data['quantidade'],
                    preco_unitario=detalhamento_data['preco_unitario'],
                    pedido_id=id
                )
                db.session.add(novo_detalhamento)
    
    db.session.commit()
    
    return jsonify({
        'id': pedido.id,
        'descricao': pedido.descricao,
        'usuario_id': pedido.usuario_id,
        'detalhamentos': [{
            'id': d.id,
            'produto_id': d.produto_id,
            'quantidade': d.quantidade,
            'preco_unitario': d.preco_unitario
        } for d in pedido.detalhamentos]
    }), 200

@pedido_bp.route('/pedidos/<int:id>', methods=["DELETE"])
def deletar_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({'Message':'Pedido não encontrado'}), 404
    
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'Message':'Pedido deletado com sucesso'}), 200
