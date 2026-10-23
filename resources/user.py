from flask import Flask
from flask_restful import Resource,reqparse
from models.user import UserModel


class User(Resource):
    
    def get(self, username):
        user = UserModel.find_hotel(username)#ou devolve o user ou nada
        if user is not None:
            return user.json(), 200
        return{"mensagem": "User não foi encontrado"}
    
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
    argumentos.add_argument("userna,e",type=str, required = True, help="O nome do user é obrigatório")
    argumentos.add_argument("password",type=float, required = True, help="Passwod obrigatória")

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

