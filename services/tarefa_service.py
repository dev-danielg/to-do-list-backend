from models import Tarefa
from repositories import TarefaRepository
from typing import Sequence
from models import Tarefa


class TarefaService:
    
    def __init__(self, repository: TarefaRepository) -> None:
        self.repository = repository
    
    
    def cadastrar(self, dados: dict, id_usuario: int) -> Tarefa:
        titulo = dados.get("titulo")
        descricao = dados.get("descricao")
        descricao = descricao.strip() if descricao else descricao
        
        if not titulo:
            raise ValueError("Tarefa deve conter ao menos o título.")
        
        tarefa = Tarefa(titulo=titulo.strip(),
                        descricao=descricao,
                        concluida=False,
                        id_usuario=id_usuario)
        
        try:
            self.repository.cadastrar(tarefa)
            self.repository.commit()
            return tarefa
        
        except Exception:
            self.repository.rollback()
            raise
        
        
    def buscar_todos(self, titulo: str | None, concluida: str | None, id_usuario: int) -> Sequence[Tarefa]:
        titulo = titulo.strip() if titulo else None
        integer_concluida = int(concluida.strip()) if concluida else None
        tarefas = self.repository.buscar_todos(titulo, integer_concluida, id_usuario)
        
        if not tarefas:
            raise LookupError("Tarefas específicas não encontradas.")
        
        return tarefas
        
        
    
    def buscar_por_id(self, id_tarefa: int, id_usuario: int) -> Tarefa:
        tarefa = self.repository.buscar_por_id(id_tarefa)
        
        if not tarefa:
            raise LookupError("Tarefa específica não encontrada.")
        
        if tarefa.id_usuario != id_usuario:
            raise ValueError("Acesso negado.")
        
        return tarefa
    
    
    def deletar(self, id_tarefa: int, id_usuario: int):
        tarefa = self.buscar_por_id(id_tarefa, id_usuario)
        
        try:
            self.repository.deletar(tarefa)
            self.repository.commit()
            return tarefa
        
        except Exception:
            self.repository.rollback()
            raise
        
    
    def atualizar(self, id_tarefa, dados: dict, id_usuario: int):
        tarefa = self.buscar_por_id(id_tarefa, id_usuario)
        titulo = dados.get("titulo")
        descricao = dados.get("descricao")
        concluida = dados.get("concluida")
        
        if titulo:
            tarefa.titulo = titulo.strip()
        if descricao:
            tarefa.descricao = descricao.strip()
        if concluida:
            tarefa.concluida = concluida
        
        try:
            self.repository.atualizar(tarefa)
            self.repository.commit()
            return tarefa
        
        except Exception:
            self.repository.rollback()
            raise