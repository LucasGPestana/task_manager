from typing import List, Optional
from service_layer.task_service import TaskService
from service_layer.task_status_service import TaskStatusService


class ControladorTarefas:
    
    
    def __init__(self) -> None:
        
        self.servico_tarefas = TaskService()
        self.servico_status = TaskStatusService()
        self.executando = True
    
    def executar(self) -> None:
        
        self.mostrar_cabecalho()
        
        while self.executando:
            self.mostrar_menu_principal()
            opcao = self.obter_opcao_usuario("Escolha uma opção (1-5): ", 1, 5)
            self.processar_opcao(opcao)
    
    def mostrar_cabecalho(self) -> None:
        
        print("\n" + "="*60)
        print("           GERENCIADOR DE TAREFAS - CLI")
        print("="*60)
        print("Sistema para gerenciamento de tarefas pessoais")
        print("="*60 + "\n")
    
    def mostrar_menu_principal(self) -> None:
        
        print("\n" + "-"*40)
        print("MENU PRINCIPAL")
        print("-"*40)
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Remover Tarefa")
        print("4. Alterar Status da Tarefa")
        print("5. Sair")
        print("-"*40)
    
    def obter_opcao_usuario(self, mensagem: str, minimo: int, maximo: int) -> int:
        
        while True:
            try:
                entrada = input(mensagem).strip()
                if not entrada:
                    print("ERRO: Entrada não pode ser vazia. Tente novamente.")
                    continue
                
                opcao = int(entrada)
                
                if minimo <= opcao <= maximo:
                    return opcao
                else:
                    print(f"ERRO: Opção deve estar entre {minimo} e {maximo}. Tente novamente.")
            
            except ValueError:
                print("ERRO: Entrada inválida. Digite um número.")
    
    def processar_opcao(self, opcao: int) -> None:
        
        acoes = {
            1: self.adicionar_tarefa,
            2: self.listar_tarefas,
            3: self.remover_tarefa,
            4: self.alterar_status_tarefa,
            5: self.sair
        }
        
        if opcao in acoes:
            acoes[opcao]()
    
    
    #  ADICIONAR TAREFA
       
    def adicionar_tarefa(self) -> None:
        """Implementa a funcionalidade de adicionar nova tarefa."""
        print("\n" + "="*40)
        print("ADICIONAR NOVA TAREFA")
        print("="*40)
        
        # Obter nome da tarefa
        nome = self.obter_entrada_texto("Nome da tarefa: ")
        if nome is None:
            return
        
        # Obter descrição da tarefa
        descricao = self.obter_entrada_texto("Descrição (opcional - pressione Enter para pular): ", opcional=True)
        if descricao is None:
            descricao = ""  # Descrição pode ser vazia
        
        # Obter status da tarefa
        status = self.selecionar_status()
        if status is None:
            return
        
        # Tentar criar a tarefa
        try:
            self.servico_tarefas.create_task(nome, descricao, status)
            print(f"\nSUCESSO: Tarefa '{nome}' adicionada com sucesso!")
            print(f"   Status: {status}")
        
        except ValueError as erro:
            print(f"\nERRO ao adicionar tarefa: {erro}")
    
    def obter_entrada_texto(self, mensagem: str, opcional: bool = False) -> Optional[str]:
       
        while True:
            entrada = input(mensagem).strip()
            
            if not entrada:
                if opcional:
                    return ""
                print("ERRO: Esta informação é obrigatória. Tente novamente.")
                continue
            
            return entrada
    
    def selecionar_status(self) -> Optional[str]:
        
        try:
            # Obter status disponíveis
            status_disponiveis = self.servico_status.get_available_status_names()
            
            if not status_disponiveis:
                print("ERRO: Não foi possível carregar os status disponíveis.")
                return None
            
            print("\nStatus disponíveis:")
            for i, status in enumerate(status_disponiveis, 1):
                print(f"  {i}. {status}")
            
            # Obter seleção do usuário
            escolha = self.obter_opcao_usuario(
                f"Selecione o status (1-{len(status_disponiveis)}): ",
                1,
                len(status_disponiveis)
            )
            
            return status_disponiveis[escolha - 1]
        
        except Exception as erro:
            print(f"ERRO ao selecionar status: {erro}")
            return None
    
    
    #  LISTAR TAREFAS
        
    def listar_tarefas(self) -> None:
        
        print("\n" + "="*40)
        print("LISTA DE TAREFAS")
        print("="*40)
        
        try:
            tarefas = self.servico_tarefas.list_all_tasks()
            
            if not tarefas:
                print("\nNenhuma tarefa cadastrada.")
                return
            
            print(f"\nTotal de tarefas: {len(tarefas)}")
            print("-"*70)
            print(f"{'ID':<5} {'NOME':<25} {'STATUS':<15} {'DESCRIÇÃO':<25}")
            print("-"*70)
            
            for tarefa in tarefas:
                # Truncar textos longos para melhor visualização
                nome = tarefa.name[:22] + "..." if len(tarefa.name) > 25 else tarefa.name
                descricao = tarefa.description[:22] + "..." if len(tarefa.description) > 25 else tarefa.description
                
                print(f"{tarefa.id:<5} {nome:<25} {tarefa.status.name:<15} {descricao:<25}")
            
            print("-"*70)
        
        except Exception as erro:
            print(f"ERRO ao listar tarefas: {erro}")
    
    
    #  REMOVER TAREFA
        
    def remover_tarefa(self) -> None:
        
        print("\n" + "="*40)
        print("REMOVER TAREFA")
        print("="*40)
        
        # Primeiro listar as tarefas para o usuário ver os IDs
        try:
            tarefas = self.servico_tarefas.list_all_tasks()
            
            if not tarefas:
                print("\nNenhuma tarefa cadastrada para remover.")
                return
            
            self.listar_tarefas()  # Reutiliza o método de listagem
            
            # Obter ID da tarefa a ser removida
            id_tarefa = self.obter_opcao_usuario(
                "\nDigite o ID da tarefa que deseja remover (ou 0 para cancelar): ",
                0,
                max(tarefa.id for tarefa in tarefas)
            )
            
            if id_tarefa == 0:
                print("Operação cancelada.")
                return
            
            # Confirmar remoção
            confirmar = input(f"Tem certeza que deseja remover a tarefa ID {id_tarefa}? (S/N): ").strip().upper()
            
            if confirmar == 'S':
                try:
                    self.servico_tarefas.delete_task(id_tarefa)
                    print(f"SUCESSO: Tarefa ID {id_tarefa} removida com sucesso!")
                
                except ValueError as erro:
                    print(f"ERRO ao remover tarefa: {erro}")
            
            else:
                print("Operação cancelada.")
        
        except Exception as erro:
            print(f"ERRO: {erro}")
    
    
    # FUNCIONALIDADE 4: ALTERAR STATUS DA TAREFA
        
    def alterar_status_tarefa(self) -> None:
        
        print("\n" + "="*40)
        print("ALTERAR STATUS DA TAREFA")
        print("="*40)
        
        # Primeiro listar as tarefas
        try:
            tarefas = self.servico_tarefas.list_all_tasks()
            
            if not tarefas:
                print("\nNenhuma tarefa cadastrada.")
                return
            
            self.listar_tarefas()  # Reutiliza o método de listagem
            
            # Obter ID da tarefa
            id_tarefa = self.obter_opcao_usuario(
                "\nDigite o ID da tarefa para alterar status (ou 0 para cancelar): ",
                0,
                max(tarefa.id for tarefa in tarefas)
            )
            
            if id_tarefa == 0:
                print("Operação cancelada.")
                return
            
            # Obter novo status
            print(f"\nAlterando status da tarefa ID {id_tarefa}")
            novo_status = self.selecionar_status()
            
            if novo_status is None:
                return
            
            # Confirmar alteração
            confirmar = input(
                f"Alterar status da tarefa ID {id_tarefa} para '{novo_status}'? (S/N): "
            ).strip().upper()
            
            if confirmar == 'S':
                try:
                    self.servico_tarefas.update_task_status(id_tarefa, novo_status)
                    print(f"SUCESSO: Status da tarefa ID {id_tarefa} alterado para '{novo_status}'!")
                
                except ValueError as erro:
                    print(f"ERRO ao alterar status: {erro}")
            
            else:
                print("Operação cancelada.")
        
        except Exception as erro:
            print(f"ERRO: {erro}")
    
    
    #  SAIR
        
    def sair(self) -> None:
        """Finaliza a execução do programa."""
        print("\n" + "="*60)
        print("Obrigado por usar o Gerenciador de Tarefas!")
        print("Encerrando o programa...")
        print("="*60)
        self.executando = False



# PONTO DE ENTRADA DO PROGRAMA

def main() -> None:
    
    try:
        controlador = ControladorTarefas()
        controlador.executar()
    
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    
    except Exception as erro:
        print(f"\nERRO inesperado: {erro}")
        print("Por favor, informe ao desenvolvedor.")


if __name__ == "__main__":
    main()