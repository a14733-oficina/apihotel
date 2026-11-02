from flask import Flask
from flask_restful import Resource,reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from blocklist import BLOCKLIST


class User(Resource):
    
    def get(self, username):
        user = UserModel.find_hotel(username)#ou devolve o user ou nada
        if user is not None:
            return user.json(), 200
        return{"mensagem": "User não foi encontrado"}
    @jwt_required()
    def delete(self,username):
        user =UserModel.find_user(username)
        if user is not None:
            try:
                user.delete_hotel()
            except:
                return{"mensagem": "Um erro interno do server aconteceu"},500
            
            return {"Mensagem": "utilizador removido"},200
        return {"Mensagem": "Hotel n encontrado"},404

class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username",type=str, required = True, help="O nome do user é obrigatório")
    argumentos.add_argument("password",type=str, required = True, help="Passwod obrigatória")

    def post(self):
        dados = UserRegister.argumentos.parse_args()
        if UserModel.find_user(dados["username"]):
            return {"mensagem": "Já existe um utilizador com este username"},400
        novo_utilizador = UserModel(**dados)
        try:
            novo_utilizador.save_user()
            return {"mensagem": "utilizador criado com sucesso"},201
        except:
            return {"mensagem": "Erro interno ocorreu......."},500


class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username",type=str, required = True, help="O nome do user é obrigatório")
    argumentos.add_argument("password",type=str, required = True, help="Passwod obrigatória")

    def post(self):
        dados= UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["username"])
        if user and compare_digest(user.password,dados["password"]):
            token= create_access_token(identity=user.username)
            return {"access_token":token},200
        return {"mensagem": "user ou password errados"},401

class Userlogout(Resource):
    @jwt_required
    def post(self):
        #pegar token e invalidar
        jwt_id =get_jwt()["jti"]#obter o identifucardor do token
        #anexar este identificador a minhga lista de toen revogados(desativar)
        BLOCKLIST.add(jwt_id)#adiconat a minha lista de tokens invaldios o atual
        return {"mensagem":"Logour do user efetuado com sucesos"},200

    
