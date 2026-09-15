from num2words import num2words
from rich.console import Console # Importar Console daqui
from rich.table import Table     # Table vem daqui
import operacoes_db
import consulta_API
console = Console() # Instanciamos o objeto console aqui

from num2words import num2words
import consulta_API
import operacoes_db

def consultar_preco():
    # Opcional: o parâmetro 'tipo' não é estritamente obrigatório pela API do parallelum para busca direta por código FIPE,
    # mas mantemos a captura para seguir o fluxo se necessário.
    tipo = input("Tipo (carros, motos, caminhoes): ").lower()
    fipe = input("Digite o código FIPE: ").strip()
    
    # 1. Verificar se já existe no banco de dados usando is_no_banco()
    if operacoes_db.is_no_banco(fipe):
        print("\n[Banco de Dados] Dados recuperados do cache local!")
        cache = operacoes_db.buscar_por_fipe(fipe)
        
        # Estrutura da tupla retornada pelo banco: 
        # (id, codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso)
        _, codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso = cache
        
        print(f"Código FIPE: {codigo_fipe}")
        print(f"Marca: {marca}")
        print(f"Modelo: {modelo}")
        print(f"Ano Modelo: {ano_modelo}")
        print(f"Preço: R$ {preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"Valor por extenso: {preco_extenso}")
        
    else:
        print("\n[API FIPE] Código não encontrado no banco. Consultando API externa...")
        consulta = consulta_API.get_valor(fipe)
        
        # Como consulta_API.get_valor já retorna o dicionário via .json(), 
        # verificamos se a chave 'Preco' existe para validar o retorno.
        if not consulta or 'Preco' not in consulta:
            print("Erro ao buscar o valor ou código FIPE inválido.")
            return
        
        marca = consulta.get('Marca', 'Desconhecida')
        modelo = consulta.get('Modelo', 'Desconhecido')
        ano_modelo = consulta.get('AnoModelo', 0)
        valor_str = consulta.get('Preco', 'R$ 0,00')
        
        # Tratamento do preço recebido da API (ex: "R$ 45.000,00" -> 45000.00)
        try:
            preco_limpo = valor_str.replace('R$ ', '').replace('.', '').replace(',', '.')
            preco = float(preco_limpo)
        except ValueError:
            preco = 0.0
            
        preco_extenso = num2words(preco, lang='pt_BR', to='currency', currency='BRL')
        
        # Salva no banco de dados (a ordem da tupla deve bater com o INSERT em operacoes_db)
        dados = (fipe, marca, modelo, ano_modelo, preco, preco_extenso)
        operacoes_db.salvar_consulta(dados)
        print("Dados salvos no banco com sucesso!")
        
        # Exibe os dados obtidos da API
        print(f"Código FIPE: {fipe}")
        print(f"Marca: {marca}")
        print(f"Modelo: {modelo}")
        print(f"Ano Modelo: {ano_modelo}")
        print(f"Preço: {valor_str}")
        print(f"Valor por extenso: {preco_extenso}")

def obter_dados_veiculo(codigo):
    # Tenta buscar no banco
    cache = operacoes_db.buscar_por_fipe(codigo)
    if cache:
        return {'marca': cache[2], 'modelo': cache[3], 'ano': cache[4], 'preco': cache[5], 'extenso': cache[6]}
    
    # Se não tiver, busca na API
    dados = consulta_API.get_valor(codigo)
    if dados:
        preco = float(dados[0]['valor'].replace('R$ ', '').replace('.', '').replace(',', '.'))
        extenso = num2words(preco, lang='pt_BR', to='currency', currency='BRL')
        operacoes_db.salvar_consulta((codigo, dados[0]['marca'], dados[0]['modelo'], dados[0]['anoModelo'], preco, extenso))
        return {'marca': dados[0]['marca'], 'modelo': dados[0]['modelo'], 'ano': dados[0]['anoModelo'], 'preco': preco, 'extenso': extenso}
    return None

def comparar_veiculos():
    cod1 = input("Código FIPE 1: ").strip()
    cod2 = input("Código FIPE 2: ").strip()
    
    def obter_ou_buscar_dados(fipe):
        """Função auxiliar para buscar no banco (cache) ou consumir a API e salvar."""
        if operacoes_db.is_no_banco(fipe):
            console.print(f"[dim][Banco] Veículo {fipe} recuperado do cache local.[/dim]")
            cache = operacoes_db.buscar_por_fipe(fipe)
            # Estrutura da tupla: (id, codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso)
            _, codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso = cache
            return {
                'codigo_fipe': codigo_fipe,
                'marca': marca,
                'modelo': modelo,
                'ano_modelo': ano_modelo,
                'preco': preco,
                'preco_extenso': preco_extenso
            }
        else:
            console.print(f"[dim][API] Veículo {fipe} não encontrado no banco. Consultando API...[/dim]")
            consulta = consulta_API.get_valor(fipe)
            
            if not consulta or 'Preco' not in consulta:
                return None
            
            marca = consulta.get('Marca', 'Desconhecida')
            modelo = consulta.get('Modelo', 'Desconhecido')
            ano_modelo = consulta.get('AnoModelo', 0)
            valor_str = consulta.get('Preco', 'R$ 0,00')
            
            try:
                preco_limpo = valor_str.replace('R$ ', '').replace('.', '').replace(',', '.')
                preco = float(preco_limpo)
            except ValueError:
                preco = 0.0
                
            preco_extenso = num2words(preco, lang='pt_BR', to='currency', currency='BRL')
            
            # Salva no banco de dados
            dados = (fipe, marca, modelo, ano_modelo, preco, preco_extenso)
            operacoes_db.salvar_consulta(dados)
            
            return {
                'codigo_fipe': fipe,
                'marca': marca,
                'modelo': modelo,
                'ano_modelo': ano_modelo,
                'preco': preco,
                'preco_extenso': preco_extenso
            }

    v1 = obter_ou_buscar_dados(cod1)
    v2 = obter_ou_buscar_dados(cod2)
    
    if not v1 or not v2:
        console.print("[red]Erro ao buscar um dos veículos (código FIPE inválido ou erro na API).[/red]")
        return

    dif = abs(v1['preco'] - v2['preco'])
    dif_extenso = num2words(dif, lang='pt_BR', to='currency', currency='BRL')
    
    mais_caro = "Veículo 1" if v1['preco'] > v2['preco'] else "Veículo 2"
    if v1['preco'] == v2['preco']:
        mais_caro = "Os dois veículos"
    
    table = Table(title="Comparação de Preços")
    table.add_column("Atributo", style="dim")
    table.add_column(f"Veículo 1 ({v1['modelo']})", style="cyan")
    table.add_column(f"Veículo 2 ({v2['modelo']})", style="magenta")
    
    table.add_row("Marca", v1['marca'], v2['marca'])
    table.add_row("Ano", str(v1['ano_modelo']), str(v2['ano_modelo']))
    table.add_row("Preço", f"R$ {v1['preco']:,.2f}", f"R$ {v2['preco']:,.2f}")
    table.add_row("Diferença", "-", f"{dif_extenso} (R$ {dif:,.2f})")
    
    console.print(table)
    if v1['preco'] != v2['preco']:
        console.print(f"[bold green]Resultado:[/bold green] O {mais_caro} é mais caro.")
    else:
        console.print("[bold green]Resultado:[/bold green] Os veículos possuem o mesmo preço.")

def listar_marcas():
    tipo = input("Tipo (carros, motos, caminhoes): ").lower()
    
    # Busca e salva no DB
    marcas = consulta_API.buscar_marcas(tipo)
    if not marcas:
        console.print("[red]Erro ao buscar marcas ou tipo inválido.[/red]")
        return
        
    operacoes_db.salvar_marcas(tipo, marcas)
    dados = operacoes_db.listar_marcas_com_historico(tipo)
    
    # Exibe em Rich
    table = Table(title=f"Marcas de {tipo.capitalize()}")
    table.add_column("Código", style="dim")
    table.add_column("Nome", style="cyan")
    table.add_column("Modelos no Histórico", style="green")
    
    for cod, nome, count in dados:
        table.add_row(str(cod), nome, str(count))
        
    console.print(table)

def listar_historico():
    dados = operacoes_db.listar_consultas()

    table = Table(title=f"Dados")
    table.add_column("Código", style="dim")
    table.add_column("Nome", style="cyan")
    table.add_column("Modelo", style="green")
    table.add_column("Marca", style="yellow")
    table.add_column("Ano", style="blue")
    table.add_column("Preço", style="red")
    
    for cod, nome, count in dados:
        table.add_row(str(cod), nome, str(count))
        
    console.print(table)

def listar_marcas_detalhado(): # Renomeei para não conflitar com a anterior
    dados = operacoes_db.listar_marca()
    table = Table(title="Dados de Marcas")
    
    # Corrigido: add_column (um 'l' só)
    table.add_column("Preço", style="orange")
    table.add_column("Nome", style="red")
    table.add_column("Código", style="yellow")

    for cod, nome, preco in dados:
        table.add_row(str(preco), nome, str(cod))
        
    console.print(table)