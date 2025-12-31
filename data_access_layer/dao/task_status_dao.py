from abc import ABC, abstractmethod
from typing import Tuple, Union


from entities.task_status import TaskStatus


class TaskStatusDAO(ABC):

    """
    'Data Access Object' da entidade status da tarefa, que realiza interface com o banco de dados
    """

    @abstractmethod
    def list_all(self) -> Union[Tuple[TaskStatus], None]:

        """Lista todos os status das tarefas do banco de dados

        Returns
        -------
        Union[Tuple[entities.task_status.TaskStatus], None] 
            Objetos TaskStatus com os dados armazenados no banco de dados
        """

        pass

    @abstractmethod
    def get_by_name(self, status_name: str) -> Union[TaskStatus, None]:

        """Obtém um status da tarefa do banco de dados, a partir do seu nome

        Parameters
        ----------
        status_name: str
            Nome do status da tarefa a ser obtida

        Returns
        -------
        Union[entities.task_status.TaskStatus, None] 
            Objeto TaskStatus com o nome especificado
        """

        pass