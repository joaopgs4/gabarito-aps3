from flask import Flask, request
from bson.objectid import ObjectId
import pymongo
import os

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['USER']}:{os.environ['PASSWORD']}@aps3-2024-2.ocny2.mongodb.net/")
app = Flask(__name__)
db = client["aps3"]
db_usuarios = db["users"]
db_bikes = db["bikes"]

@app.route("/", methods = ["GET"])
def index():
    return {"mensagem": "Sucesso"}, 200

################################################################################################################
########################################### Código à baixo #####################################################
################################################################################################################


# Aviso: Todos os returns são realiados em forma de dicionario, pois o FRAMEWORK do Flask (e a maioria dos framworks python, como FastAPI e Sanic)
# São capazes de identificar que um retorno em dicionario é para ser convertido em JSON, assim não precisamos do Jsonify.
#E NTENDA por que podemos ignorar esta função, por que ela existe e por que ela é util em certos casos ou outras linguagens


############# Rotas de Usuario #############

@app.route("/usuarios", methods=["POST", "GET"]) #Podemos dividir em multiplas funções, mas prefiro dividir por rotas
def users_root():    
    try:
        #Rota de Get
        if request.method == "GET":
            users = list(db_usuarios.find())
            for user in users:
                user["_id"] = str(user["_id"]) #Transforma object_id em id (str)
            return {"Users": users}, 200

        #Rota de Post
        if request.method == "POST":
            data = request.json
            mandatory_fields = ['nome', 'cpf', "data-nascimento"]
            if not all(field in data for field in mandatory_fields):
                return {"Erro: ": "Campos obrigatórios pendentes"}, 400
            if db_usuarios.find_one({"cpf": data['cpf']}):
                return {"Erro: ": "CPF já cadastrado"}, 400
            data['emprestimos'] = {}
            new_user_id = db_usuarios.insert_one(data).inserted_id
            return {"Sucesso: ": f"Usuario de id {new_user_id} criado com sucesso"}, 201
            
        #Rotas invalidas
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Exception as e:
        return {"Erro: ": e}, 500
        

#interagimos com o ID como string, por ser UUID, ou cpf or ser campo unico de identificação
@app.route("/usuarios/<string:id>", methods=["GET", "PUT", "DELETE"]) 
def user_by_id(id : str):    
    try:
        if ObjectId.is_valid(id):
            user = db_usuarios.find_one({"_id": ObjectId(id)})
        else:
            user = db_usuarios.find_one({"cpf": id})
        if not user: 
            return {"Erro: ": f"Usuario de ID {id} inexistente"}, 400
        user["_id"] = str(user["_id"])

        if request.method == "GET":
            return {"Usuario: ": user}, 200

        if request.method == "PUT":
            data = request.json
            for field in data:
                if field == "cpf" or field == "_id":
                    return {"Erro: ": "Campo não editável"}, 400
                if field in user:
                    user[field] = data[field]
            # https://www.mongodb.com/docs/manual/reference/operator/update/set/
            db_usuarios.update_one({"_id": ObjectId(user["_id"])}, {"$set": user})
            return {"Sucesso: ": f"Usuario de ID {id} editado com sucesso"}, 200

        if request.method == "DELETE":
            db_usuarios.delete_one({"_id": ObjectId(user["_id"])})
            return {"Sucesso: ": f"Usuario de ID {id} deletado com sucesso"}, 200
                
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Exception as e:
        return {"Erro: ": e}, 500
        


############# Rotas de Bikes #############
@app.route("/bikes", methods=["POST", "GET"]) #Podemos dividir em multiplas funções, mas prefiro dividir por rotas
def bikes_root():    
    try:
        #Rota de Get
        if request.method == "GET":
            bikes = list(db_bikes.find())
            for bike in bikes:
                bike["_id"] = str(bike["_id"]) #Transforma object_id em id (str)
            return {"Bikes": bikes}, 200

        #Rota de Post
        if request.method == "POST":
            data = request.json
            mandatory_fields = ['marca', 'modelo', "cidade"]
            if not all(field in data for field in mandatory_fields):
                return {"Erro: ": "Campos obrigatórios pendentes"}, 400
            data['disponibilidade'] = "disponivel"
            new_bike_id = db_bikes.insert_one(data).inserted_id
            return {"Sucesso: ": f"Bike de id {new_bike_id} criado com sucesso"}, 201
            
        #Rotas invalidas
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Exception as e:
        return {"Erro: ": e}, 500
        

#interagimos com o ID como string, por ser UUID, ou cpf or ser campo unico de identificação
@app.route("/bikes/<string:id>", methods=["GET", "PUT", "DELETE"]) 
def bike_by_id(id : str):    
    try:
        if ObjectId.is_valid(id):
            bike = db_bikes.find_one({"_id": ObjectId(id)})
        if not bike: 
            return {"Erro: ": f"Bike de ID {id} inexistente"}, 400

        if request.method == "GET":
            bike["_id"] = str(bike["_id"])
            return {"Bike: ": bike}, 200

        if request.method == "PUT":
            data = request.json
            for field in data:
                if field == "disponibilidade" or field == "_id":
                    return {"Erro: ": "Campo não editável"}, 400
                if field in bike:
                    bike[field] = data[field]
            # https://www.mongodb.com/docs/manual/reference/operator/update/set/
            db_bikes.update_one({"_id": ObjectId(bike["_id"])}, {"$set": bike})
            return {"Sucesso: ": f"Bike de ID {id} editado com sucesso"}, 200

        if request.method == "DELETE":
            db_bikes.delete_one({"_id": ObjectId(bike["_id"])})
            return {"Sucesso: ": f"Bike de ID {id} deletado com sucesso"}, 200
                
        return {"Erro: ": "Método de Acesso Invalido"}, 405
    
    except Exception as e:
        return {"Erro: ": e}, 500

############# Rotas de Empréstimos #############
@app.route("/emprestimos", methods=["GET"])
def emprestimos_root():
    try:
        #Filtra todos os usuarios que possuem emprestimos
        # https://www.mongodb.com/docs/manual/reference/operator/query/exists/
        # https://www.mongodb.com/docs/manual/reference/operator/query/ne/
        users = db_usuarios.find({"emprestimos": {"$exists": True, "$ne": {}}})
        emprestimos = []
        for user in users:
            user["_id"] = str(user["_id"])
            for bike_id, data in user['emprestimos'].items():
                emprestimos.append({
                    "id_usuario": user["_id"],
                    "id_bike": bike_id,
                    "data_emprestimo": data["data_emprestimo"]
                })
        return {"emprestimos": emprestimos}, 200
    
    except Exception as e:
        return {"Erro: ": e}, 500


@app.route("/emprestimos/usuarios/<string:id_usuario>/bikes/<string:id_bike>", methods=["POST"])
def registrar_emprestimo(id_usuario, id_bike):
    try:
        data = request.json
        if "data_emprestimo" not in data:
            return {"Erro: ": "Campo obrigatório pendente"}, 400
        # Verificar se a bike existe e está disponível
        bike = db_bikes.find_one({"_id": ObjectId(id_bike)})
        if not bike:
            return {"Erro: ": "Bike não encontrada"}, 404
        if bike["disponibilidade"] != "disponivel":
            return {"Erro: ": "Bike já está em uso"}, 400

        # Verificar se o usuário existe
        user = db_usuarios.find_one({"_id": ObjectId(id_usuario)})
        if not user:
            return {"Erro: ": "Usuário não encontrado"}, 404

        # Registrar o empréstimo no documento do usuário
        emprestimo = {id_bike: {"data_emprestimo": data["data_emprestimo"]}}

        #Utilizamos concatenação de string como alvo do set para mudar o valor do emprestimo correto
        # https://www.mongodb.com/docs/manual/reference/operator/update/set/
        db_usuarios.update_one({"_id": ObjectId(id_usuario)}, {"$set": {"emprestimos." + id_bike: emprestimo[id_bike]}}) 
        
        # Atualizar a bike como não disponível
        # https://www.mongodb.com/docs/manual/reference/operator/update/set/
        db_bikes.update_one({"_id": ObjectId(id_bike)}, {"$set": {"disponibilidade": "em uso", "id_usuario": id_usuario}})
        
        return {"Sucesso: ": f"Empréstimo da bike {id_bike} registrado para o usuário {id_usuario}. ID do Empréstimo: {id_bike}"}, 201
    except Exception as e:
        return {"Erro: ": e}, 500


#Utilizo o ID da bike alugada como id do emprestimo ao invés de criar um novo id 
@app.route("/emprestimos/<string:id_emprestimo>", methods=["DELETE"])
def deletar_emprestimo(id_emprestimo):
    try:
        # Encontrar o usuário que tem esse empréstimo
        # https://www.mongodb.com/docs/manual/reference/operator/query/exists/
        user = db_usuarios.find_one({"emprestimos." + id_emprestimo: {"$exists": True}})
        if not user:
            return {"Erro: ": "Empréstimo não encontrado"}, 404
        
        # Remover o empréstimo do documento do usuário
        # https://www.mongodb.com/docs/manual/reference/operator/update/unset/
        db_usuarios.update_one({"_id": user["_id"]}, {"$unset": {"emprestimos." + id_emprestimo: ""}})
        
        # Atualizar a bike como disponível
        # https://www.mongodb.com/docs/manual/reference/operator/update/set/
        db_bikes.update_one({"_id": ObjectId(id_emprestimo)}, {"$set": {"disponibilidade": "disponivel", "id_usuario": None}})
        
        return {"Sucesso: ": f"Empréstimo {id_emprestimo} deletado com sucesso"}, 200
    except Exception as e:
        return {"Erro: ": e}, 500
    
if __name__ == '__main__':
    app.run(debug=True)