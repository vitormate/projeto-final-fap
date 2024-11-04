from flask import Blueprint, request, jsonify
from models import db, Usuario

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    data = request.json
    
    # Inicializando o objeto com todos os dados ao mesmo tempo
    novo_usuario = Usuario(
        nome=data.get('nome'),
        segundo_nome=data.get('segundo_nome'),
        login=data.get('login'),
        senha=data.get('senha')
    )

    # Verificando se os campos obrigatórios estão presentes
    if not all([novo_usuario.nome, novo_usuario.login, novo_usuario.senha]):
        return jsonify({"error": "Campos 'nome', 'login' e 'senha' são obrigatórios"}), 400

    # Adiciona o novo usuário ao banco de dados
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        'id': novo_usuario.id,
        'nome': novo_usuario.nome,
        'login': novo_usuario.login,
        'senha': novo_usuario.senha
    }), 201

@usuario_bp.route('/usuarios', methods=["GET"])
def lista_de_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nome': u.nome} for u in usuarios]), 200

@usuario_bp.route('/usuario/<int:id>', methods=["PUT"])
def atualizar_usuario(id):
    data = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'Message':'Usuario não encontrado'}), 404
    
    # Atualizando o nome do usuário
    usuario.nome = data.get('nome', usuario.nome)
    db.session.commit()

    return jsonify({'id': usuario.id, 'nome': usuario.nome}), 200

@usuario_bp.route('/usuario/<int:id>', methods=["DELETE"])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'Message':'Usuario não encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'Message':'Usuario deletado com sucesso'}), 200
