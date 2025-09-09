# Sistema de Ranking de Jogadores (Versão Web)

Este projeto implementa um sistema de ranking de jogadores com uma interface web. Ele utiliza Python com Flask para o backend e HTML, CSS e JavaScript para o frontend.

## Requisitos

- Python 3.x
- Flask (biblioteca Python)

## Como Executar

1.  **Instale o Flask:**
    Abra um terminal ou prompt de comando e execute o seguinte comando:
    ```bash
    pip install Flask
    ```

2.  **Organize os Arquivos:**
    Crie a estrutura de pastas e arquivos exatamente como descrito abaixo:
    ```
    /seu_projeto/
    |-- app.py
    |-- jogadores.csv
    |-- README.md
    |
    |-- /templates/
    |   |-- index.html
    |
    |-- /static/
        |-- style.css
        |-- script.js
    ```

3.  **Execute o Servidor:**
    Navegue com o terminal até a pasta principal (`/seu_projeto/`) e execute o comando:
    ```bash
    python app.py
    ```
    O terminal irá mostrar uma mensagem indicando que o servidor está rodando, algo como `Running on http://127.0.0.1:5000/`.

4.  **Acesse a Interface:**
    - Abra seu navegador de internet (Chrome, Firefox, etc.).
    - Acesse o endereço: **http://127.0.0.1:5000/**
    - A interface do sistema de ranking será exibida.

5.  **Utilizando a Aplicação:**
    - Para carregar um novo ranking, clique no botão "Escolher arquivo", selecione seu arquivo `jogadores.csv` e clique em "Enviar CSV".
    - A página irá recarregar e a nova lista de pontuação aparecerá no menu de seleção.
    - [cite_start]Selecione uma lista no menu para visualizar o ranking correspondente, com os 3 primeiros colocados destacados. [cite: 16]
