# app.py
import os
import csv
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'

DB_PATH = 'ranking.db'

def inicializar_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            pontuacao REAL NOT NULL,
            lista_id INTEGER,
            FOREIGN KEY(lista_id) REFERENCES listas(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class Jogador:
    def __init__(self, nome, nivel, pontuacao):
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome inválido")
        if not isinstance(nivel, int) or nivel <= 0:
            raise ValueError("Nível inválido")
        if not isinstance(pontuacao, float) or pontuacao < 0:
            raise ValueError("Pontuação inválida")
        self.nome = nome
        self.nivel = nivel
        self.pontuacao = pontuacao

    def to_tuple(self):
        return (self.nome, self.nivel, self.pontuacao)

def processar_csv(file_path):
    jogadores = []
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_path = os.path.join('logs', 'erros.log')

    try:
        with open(file_path, mode='r', encoding='utf-8') as infile, \
             open(log_path, 'a', encoding='utf-8') as logfile:
            reader = csv.reader(infile)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logfile.write(f"--- Log de Erros em {timestamp} ---\n")
            next(reader)
            for i, row in enumerate(reader, 1):
                if len(row) != 3:
                    logfile.write(f"Linha {i+1}: Formato inválido - {row}\n")
                    continue
                try:
                    nome = row[0]
                    nivel = int(row[1])
                    pontuacao = float(row[2])
                    jogador = Jogador(nome, nivel, pontuacao)
                    jogadores.append(jogador)
                except (ValueError, IndexError) as e:
                    logfile.write(f"Linha {i+1}: Dados inválidos - {row} | Erro: {e}\n")
    except Exception as e:
        with open(log_path, 'a', encoding='utf-8') as logfile:
            logfile.write(f"Erro ao processar o arquivo: {e}\n")
        return None

    if jogadores:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO listas (timestamp) VALUES (?)", (timestamp,))
        lista_id = cursor.lastrowid
        jogadores_data = [j.to_tuple() + (lista_id,) for j in jogadores]
        cursor.executemany("INSERT INTO jogadores (nome, nivel, pontuacao, lista_id) VALUES (?, ?, ?, ?)", jogadores_data)
        conn.commit()
        conn.close()
    return True

@app.route('/')
def index():
    return render_template('interface.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        processar_csv(filepath)
        os.remove(filepath)
    return redirect(url_for('index'))

@app.route('/api/listas')
def get_listas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp FROM listas ORDER BY timestamp DESC")
    listas = [{'id': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(listas)

@app.route('/api/ranking/<int:lista_id>')
def get_ranking(lista_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, nivel, pontuacao FROM jogadores WHERE lista_id = ? ORDER BY pontuacao DESC", (lista_id,))
    ranking = [{'nome': row[0], 'nivel': row[1], 'pontuacao': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(ranking)

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)