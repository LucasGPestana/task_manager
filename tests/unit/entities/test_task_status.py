import pytest


from entities.task_status import TaskStatus


class TestTaskStatus:

    def test_set_id(self):

        data = {
            "id": 1,
            "name": "Disponível",
        }

        task_status = TaskStatus(**data)

        # Inteiro
        task_status.set_id(3)

        # Inteiro negativo
        with pytest.raises(ValueError):

            task_status.set_id(-1)

        # String
        with pytest.raises(ValueError):

            task_status.set_id("3")

        # Float
        with pytest.raises(ValueError):
            
            task_status.set_id(3.4)

        # Sequência
        with pytest.raises(ValueError):
            
            task_status.set_id([1, 2, 3])
    
    def test_set_name(self):

        data = {
            "id": 1,
            "name": "Disponível",
        }

        task_status = TaskStatus(**data)

        # String
        task_status.set_name("Fazendo")

        # String vazia
        with pytest.raises(ValueError):

            task_status.set_name("")

        # Inteiro
        with pytest.raises(ValueError):

            task_status.set_name(1)

        # Float
        with pytest.raises(ValueError):
            
            task_status.set_name(3.4)

        # Sequência
        with pytest.raises(ValueError):
            
            task_status.set_name([1, 2, 3])
    
    def test_get_id(self):

        data = {
            "id": 1,
            "name": "Disponível",
        }

        task_status = TaskStatus(**data)

        assert task_status.id == 1
    
    def test_get_name(self):

        data = {
            "id": 1,
            "name": "Disponível",
        }

        task_status = TaskStatus(**data)

        assert task_status.name == "Disponível"