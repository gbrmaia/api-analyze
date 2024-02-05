from fastapi import FastAPI
from typing import Dict
from datetime import datetime

import numpy as np

# Criação da aplicação FastAPI
app = FastAPI()

# Definição dos arrays preenchidos com dados
array1 = np.array([1, 2, 3, 4, 5])
array2 = np.array([6, 7, 8, 9, 10])
array3 = np.array([11, 12, 13, 14, 15])

# Função para analisar o input do usuário
def analyze_input(user_input: int) -> Dict[str, str]:
    result = {}

    arrays = [(array1, 'array 1'), (array2, 'array 2'), (array3, 'array 3')]
    found = False
    for array, name in arrays:
        if user_input in array:
            result["message"] = f"O número está no {name}."
            found = True
            break

    if not found:
        result["message"] = "O número não está em nenhum dos arrays."

    return result

# Definição do endpoint para análise do input do usuário
@app.get("/analyze/")
async def analyze_number(user_input: int):
    return analyze_input(user_input)

def hora_exata(hora_certa: int) -> str:
    if hora_certa <= 12:
        return "Bom dia"
    elif hora_certa <= 18:
        return "Boa noite"
    elif hora_certa <= 6:
        return "Boa noite"

@app.get("/hour/")
def analyze_hora():
    datahora = datetime.now()
    hora_certa = datahora.hour
    message = hora_exata(hora_certa)
    return{"message": message}

