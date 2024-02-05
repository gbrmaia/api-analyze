from fastapi import FastAPI
from typing import Dict
from datetime import datetime
import unidecode

import numpy as np

# Criação da aplicação FastAPI
app = FastAPI()

# Definição dos arrays preenchidos com dados
array1 = np.array(['1', 'opcao 1', 'opcao um', 'um'])
array2 = np.array(['2', 'opcao 2', 'opcao dois', 'dois'])
array3 = np.array(['3', 'opcao 3', 'opcao tres', 'tres'])

def preprocess_input(user_input: str) -> str:
    return unidecode.unidecode(user_input.lower())

# Função para analisar o input do usuário
def analyze_input(user_input: str) -> Dict[str, str]:
    result = {}
    
    processed_input = preprocess_input(user_input)

    arrays = [(array1, 'array 1'), (array2, 'array 2'), (array3, 'array 3')]
    found = False
    for array, name in arrays:
        if processed_input in array:
            result["message"] = f"{name}."
            found = True
            break

    if not found:
        result["message"] = "O número não está em nenhum dos arrays."

    return result

# Definição do endpoint para análise do input do usuário
@app.get("/analyze/")
async def analyze_number(user_input: str):
    return analyze_input(user_input)

def hora_exata(hora_certa: int) -> str:
    if hora_certa < 6:
        return "Boa noite"
    elif hora_certa < 12:
        return "Bom dia"
    elif hora_certa < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

@app.get("/hour/")
def analyze_hora():
    datahora = datetime.now()
    hora_certa = datahora.hour
    message = hora_exata(hora_certa)
    return{"message": message}

