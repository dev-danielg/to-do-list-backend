from models import Tarefa
from sqlalchemy import select
from sqlalchemy.orm import scoped_session
from typing import Sequence


class TarefaRepository:
    
    def __init__(self, session: scoped_session) -> None:
        self.session = session
        
    
    def buscar_por_id(self, id_tarefa: int) -> Tarefa | None:
        query = select(Tarefa).where(Tarefa.id == id_tarefa)
        return self.session.execute(query).scalar_one_or_none()
    
    
    def buscar_todos(self, titulo: str | None, concluida: int | None, id_usuario: int) -> Sequence[Tarefa]:
        query = select(Tarefa).where(Tarefa.id_usuario == id_usuario)
        
        if titulo:
            query = query.where(Tarefa.titulo.ilike(titulo))
        if concluida is not None:
            query = query.where(Tarefa.concluida == concluida)
            
        return self.session.execute(query).scalars().all()
    
    
    def cadastrar(self, tarefa: Tarefa) -> None:
        self.session.add(tarefa)
    
    
    def deletar(self, tarefa: Tarefa) -> None:
        self.session.delete(tarefa)
    
    
    def atualizar(self, tarefa: Tarefa) -> None:
        self.session.merge(tarefa)
    
    
    def commit(self) -> None:
        self.session.commit()
    
    
    def rollback(self) -> None:
        self.session.rollback()
        