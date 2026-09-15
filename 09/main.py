from num2words import num2words
from rich.console import Console
from rich.table import Table
import operacoes_db
import opcoes
import consulta_API

console = Console()

def main():
    operacoes_db.conectar()  # Conecta ao banco de dados e cria tabelas se não existirem
    
    while True:
        print("\n--- Consultor FIPE ---")
        print("Opções: ")
        print("1 - Consultar preço por código FIPE")
        print("2 - Listar marcas por tipo de veículo")
        print("3 - Listar modelos por marca")
        print("4 - Comparar preços de dois veículos")
        print("5 - Histórico de consultas")
        print("6 - Sair")
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

        if opcao == 1:    
            opcoes.consultar_preco()
        elif opcao == 2:
            opcoes.listar_marcas()
        elif opcao == 3:
            opcoes.listar_marcas_detalhado()  # Modelos por marca
        elif opcao == 4:
            opcoes.comparar_veiculos()
        elif opcao == 5:
            opcoes.listar_historico()
        elif opcao == 6:
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida, retornando ao menu principal.")

if __name__ == "__main__":
    main()