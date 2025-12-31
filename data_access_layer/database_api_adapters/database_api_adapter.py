from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union, Any

class DatabaseAPIAdapter(ABC):

    """
    Adaptador da API de um SGBD (Sistema de Gerenciamento de Banco de Dados) genérico
    """

    @abstractmethod
    def connect(self) -> None:

        """Estabelece uma conexão com o banco de dados
        """

        pass

    @abstractmethod
    def execute(self, query: str, parameters: Tuple[Any]=()) -> None:

        """Executa um comando DML que não retorna instâncias (INSERT, UPDATE ou DELETE)

        Parameters
        ----------
        query: str
            Comando DML. Pode ou não conter placeholders, os quais são identificados pelo caractere '?' (interrogação)
        parameters: Tuple[Any]
            Valores passados ao comando DML nos placeholders (?), conforme a ordem da sequência

        """

        pass
    
    @abstractmethod
    def fetch_all(self, query: str, parameters: Tuple[Any]=()) -> Union[List[Dict[str, Any]], None]:

        """Realiza uma consulta (SELECT) que retorna múltiplas instâncias

        Parameters
        ----------
        query: str
            Comando DML. Pode ou não conter placeholders, os quais são identificados pelo caractere '?' (interrogação)
        parameters: Tuple[Any]
            Valores passados ao comando DML nos placeholders (?), conforme a ordem da sequência

        Returns
        -------
        Union[List[Dict[str, Any]], None]
            Sequência de dicionários com os dados de cada instância, sendo os campos (colunas) da tabela as chaves do dicionário
        """

        pass
    
    @abstractmethod
    def fetch_one(self, query: str, parameters: Tuple[Any]=()) -> Union[Dict[str, Any], None]:

        """Realiza uma consulta (SELECT) que retorna uma única instância

        Parameters
        ----------
        query: str
            Comando DML. Pode ou não conter placeholders, os quais são identificados pelo caractere '?' (interrogação)
        parameters: Tuple[Any]
            Valores passados ao comando DML nos placeholders (?), conforme a ordem da sequência

        Returns
        -------
        Union[Dict[str, Any], None]
            Dados da instância, sendo os campos (colunas) da tabela as chaves do dicionário
        """

        pass
    
    @abstractmethod
    def close_connection(self) -> None:

        """Fecha a conexão com o banco de dados
        """

        pass