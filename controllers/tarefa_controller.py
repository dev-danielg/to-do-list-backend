from services import TarefaService
from repositories import TarefaRepository
from flask import request
from flask_jwt_extended import get_jwt_identity


class TarefaController:
    
    def __init__(self, repository: TarefaRepository, service: TarefaService) -> None:
        self.repository = repository
        self.service = service
    
    
    def cadastrar(self) -> tuple[dict[str, str | object], int]:
        try:
            tarefa = self.service.cadastrar(request.get_json(), int(get_jwt_identity()))
            
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
            
        except Exception:
            return {
                "success": False,
                "message": "Erro interno no servidor."
            }, 500
        
        return {
            "success": True,
            "message": "Tarefa criada com sucesso.",
            "data": {
                "id": tarefa.id,
                "id_usuario": tarefa.id_usuario,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "concluida": tarefa.concluida
            }
        }, 201
    
        
    def buscar_todos(self) -> tuple[dict[str, str | object], int]:
        titulo = request.args.get("titulo")
        concluida = request.args.get("concluida")
        
        try:
            tarefas = self.service.buscar_todos(titulo, concluida, int(get_jwt_identity()))
            
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }, 403
            
        except LookupError as e:
            return {
                "success": False,
                "message": str(e)
            },  404
            
        except Exception:
            return {
                "success": False,
                "message": f"Erro interno no servidor.",
            }, 500
        
        return {
            "success": True,
            "message": "Busca realizada com sucesso.",
            "data": [{
                "id": tarefa.id,
                "id_usuario": tarefa.id_usuario,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "concluida": tarefa.concluida
            } for tarefa in tarefas]
        }, 200
        
    
    def deletar(self, id_tarefa: int) -> tuple[dict[str, str | object], int]:
        try:
            tarefa = self.service.deletar(id_tarefa, int(get_jwt_identity()))
            
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }, 403
        
        except LookupError as e:
            return {
                "success": False,
                "message": str(e)
            }, 404
            
        except Exception:
            return {
                "success": False,
                "message": "Erro interno no servidor."
            }, 500
        
        return {
            "success": True,
            "message": "Tarefa deletada com sucesso.",
            "data": {
                "id": tarefa.id,
                "id_usuario": tarefa.id_usuario,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "concluida": tarefa.concluida
            }
        }, 200
    
    
    def atualizar(self, id_tarefa) -> tuple[dict[str, str | object], int]:
        try:
            tarefa = self.service.atualizar(id_tarefa, request.get_json(), int(get_jwt_identity()))
            
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }, 403
        
        except LookupError as e:
            return {
                "success": False,
                "message": str(e)
            }, 404
            
        except Exception:
            return {
                "success": False,
                "message": "Erro interno no servidor."
            }, 500
        
        return {
            "success": True,
            "message": "Tarefa atualizada com sucesso.",
            "data": {
                "id": tarefa.id,
                "id_usuario": tarefa.id_usuario,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "concluida": tarefa.concluida
            }
        }, 200