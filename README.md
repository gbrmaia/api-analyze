**Api fornencendo os endpoints**

GET XXXXX/hour/ - - irá fornecer o resultado de uma variavel como "Bom dia", "Boa tarde" e "Boa noite" útil para humanização do chatbot.

GET XXXXX/analyze/?user_input="var" - - analisa se o valor var está presente nos arrays.txt

GET XXXXX/analyze_keyword/?user_input="var" - - vai informar em qual array contém a variavel, funcionando como uma busca por palavra-chave.

POST XXXXX/add_value/"array_name"/"valor"  - - insere no array escolhido um valor

Além disso 4 arquivos txt's. 

Onde o array1 é para primeiras opções e assim por diante.

Array 4 ficando exclusivo para demais saudações ou frases inseridas pelo usuário.
