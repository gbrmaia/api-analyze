from fastapi import FastAPI, HTTPException
from typing import Dict
from datetime import datetime, timezone, timedelta
import unidecode
import numpy as np
import asyncio
# Criação da aplicação FastAPI
app = FastAPI()

# Função para carregar os arrays a partir do arquivo de texto
def carregar_arrays() -> Dict[str, np.ndarray]:
    arrays = {}
    array_names = ['array1', 'array2', 'array3', 'array4']

    for array_name in array_names:
        try:
            with open(f"{array_name}.txt", "r") as file:
                lines = file.read().splitlines()
                arrays[array_name] = np.array(lines)
        except FileNotFoundError:
            arrays[array_name] = np.array([])

    return arrays

# Função para salvar os arrays no arquivo de texto
def salvar_arrays(arrays: Dict[str, np.ndarray]):
    for array_name, array_values in arrays.items():
        with open(f"{array_name}.txt", "w") as file:
            for value in array_values:
                file.write(f"{value}\n")

# Definição dos arrays preenchidos com dados
arrays = carregar_arrays()

def formatar_input(user_input: str) -> str:
    input_formatado = unidecode.unidecode(user_input).lower()
    return input_formatado

# Função para analisar o input do usuário
def analyze_input(user_input: str) -> Dict[str, str]:
    result = {}
    
    input_formatado = formatar_input(user_input)

    found = False
    for array_name in arrays:
        try:
            with open(f"{array_name}.txt", "r") as file:
                array_values = file.read().splitlines()
                if input_formatado in array_values:
                    result["arrayfound"] = f"{array_name}"
                    found = True
                    break
        except FileNotFoundError:
            pass

    if not found:
        result["inputnotfound"] = "O número não está em nenhum dos arrays."

    return result

# Endpoint para análise do input do usuário
@app.get("/analyze/")
async def analyze_number(user_input: str):
    return analyze_input(user_input)

# Função para adicionar valor ao array e escrever no arquivo
@app.post("/add_value/{array_name}/{new_value}")
async def add_value(array_name: str, new_value: str):
    global arrays
    
    array_name = array_name.lower()
    if array_name not in arrays:
        raise HTTPException(status_code=404, detail="Array não encontrado")

    formatted_value = formatar_input(new_value)
    
    # Remove o valor se já estiver presente no array
    arrays[array_name] = np.setdiff1d(arrays[array_name], [formatted_value], assume_unique=True)
    
    # Adiciona o valor ao array
    arrays[array_name] = np.append(arrays[array_name], formatted_value)
    
    salvar_arrays(arrays)

    return {"arrayadd": f"Valor '{new_value}' adicionado ou atualizado com sucesso no {array_name} e registrado no arquivo."}

def hora_exata(hora_certa: int) -> str:
    local_timezone = timezone(timedelta(hours=-3))
    datahora = datetime.now(local_timezone)
    hora_certa = datahora.hour
    if hora_certa < 6:
        return "Boa noite"
    elif hora_certa < 12:
        return "Bom dia"
    elif hora_certa < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

# Endpoint para obter a hora exata
@app.get("/hour/")
def analyze_hora():
    datahora = datetime.now()
    hora_certa = datahora.hour
    message = hora_exata(hora_certa)
    return {"messagehora": message}

def analyze_input_partial(user_input: str) -> Dict[str, str]:
    result = {}

    input_formatado = formatar_input(user_input)

    found_values = []
    for array_name, array_values in arrays.items():
        keywords_array = [formatar_input(value.replace(" ", "")) for value in array_values]
        if any(keyword in input_formatado for keyword in keywords_array):
            found_values.append(array_name)
            result["keywordfound"] = f"{array_name}"

    if not found_values:
        result["keywordnotfound"] = "Nenhuma palavra-chave encontrada nos arrays."
    return result


@app.get("/api/endpoint_com_atraso")
async def endpoint_com_atraso():
    resultado_temporizador = await temporizador_10_segundos()
    return resultado_temporizador

# Variável global para verificar se o temporizador está em execução
timer_running = False

# Função para iniciar o temporizador
async def start_timer():
    global timer_running
    timer_running = True
    await asyncio.sleep(1800)  # 30 minutos de espera
    timer_running = False
    return "Tempo finalizado!"

# Endpoint para iniciar o temporizador
@app.get("/iniciar_timer/")
async def start_timer_endpoint():
    global timer_running
    if timer_running:
        return "O temporizador já está em execução."
    else:
        asyncio.create_task(start_timer())
        return "Temporizador iniciado por 30 minutos."
        
@app.get("/tempo_finalizado/")
async def tempo_finalizado():
    global timer_running
    if timer_running:
        return "O temporizador ainda está em execução."
    else:
        return "Tempo finalizado!"
        asyncio.create_task(start_timer())
        return "Temporizador iniciado por 30 minutos."



