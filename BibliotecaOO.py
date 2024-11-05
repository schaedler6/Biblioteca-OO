import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QDateEdit, QTextEdit
)
from PyQt5.QtCore import Qt
import sqlite3

# Função para conectar ao banco de dados
def conectar():
    caminho_banco = 'E:/SCHAEDLER/PythonSenac/biblioteca.db'
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    return conexao, cursor

class BibliotecaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerenciamento - Biblioteca")
        self.setGeometry(300, 300, 600, 800)
        self.setStyleSheet("background-color: #333333; color: #00BFFF;")

        # Layout principal
        layout_principal = QVBoxLayout()
        
        # Data Atual
        data_atual = QLabel(datetime.now().strftime("%d %B %Y"))
        data_atual.setAlignment(Qt.AlignCenter)
        data_atual.setStyleSheet("background-color: #000000; color: #00BFFF; font-size: 20px; padding: 10px;")
        layout_principal.addWidget(data_atual)
        
        # Botão Voltar
        botao_voltar = QPushButton("Voltar")
        botao_voltar.setStyleSheet("background-color: #00BFFF; color: #000000; font-weight: bold;")
        layout_principal.addWidget(botao_voltar)

        # Seção de Pesquisa de Usuário
        secao_usuario_widget = QWidget()
        secao_usuario_layout = self.criar_secao_usuario()
        secao_usuario_widget.setLayout(secao_usuario_layout)
        layout_principal.addWidget(secao_usuario_widget)
        
        # Seção de Pesquisa de Livro
        secao_livro_widget = QWidget()
        secao_livro_layout = self.criar_secao_livro()
        secao_livro_widget.setLayout(secao_livro_layout)
        layout_principal.addWidget(secao_livro_widget)

        # Data de Entrega do Livro
        data_entrega = QDateEdit()
        data_entrega.setDate(datetime.now())  # Define a data atual como padrão
        data_entrega.setStyleSheet("background-color: #333333; color: #00BFFF;")
        layout_principal.addWidget(data_entrega)

        # Widget para mostrar os resultados
        self.resultado_busca = QTextEdit()
        self.resultado_busca.setReadOnly(True)
        self.resultado_busca.setStyleSheet("background-color: #000000; color: #00BFFF;")
        layout_principal.addWidget(self.resultado_busca)

        # Define o layout principal na janela
        self.setLayout(layout_principal)

    def criar_secao_usuario(self):
        secao_usuario = QVBoxLayout()

        label_usuario = QLabel("Pesquisar Usuário:")
        label_usuario.setStyleSheet("font-weight: bold; color: #00BFFF;")
        secao_usuario.addWidget(label_usuario)

        campos_usuario = [
            "Nome do Usuário", "Data de Nascimento (AAAA-MM-DD)", "Cidade", 
            "Bairro", "Telefone", "E-mail"
        ]
        for campo in campos_usuario:
            entrada = QLineEdit()
            entrada.setPlaceholderText(campo)
            entrada.setStyleSheet("background-color: #000000; color: #00BFFF;")
            secao_usuario.addWidget(entrada)

        botao_pesquisar_usuario = QPushButton("Buscar Usuário")
        botao_pesquisar_usuario.setStyleSheet("background-color: #00BFFF; color: #000000; font-weight: bold;")
        botao_pesquisar_usuario.clicked.connect(self.mostrar_usuarios)
        secao_usuario.addWidget(botao_pesquisar_usuario)

        return secao_usuario

    def criar_secao_livro(self):
        secao_livro = QVBoxLayout()

        label_livro = QLabel("Pesquisar Livro:")
        label_livro.setStyleSheet("font-weight: bold; color: #00BFFF;")
        secao_livro.addWidget(label_livro)

        entrada_titulo_autor = QLineEdit()
        entrada_titulo_autor.setPlaceholderText("Título ou Autor")
        entrada_titulo_autor.setStyleSheet("background-color: #000000; color: #00BFFF;")
        secao_livro.addWidget(entrada_titulo_autor)

        botao_pesquisar_livro = QPushButton("Buscar Livro")
        botao_pesquisar_livro.setStyleSheet("background-color: #00BFFF; color: #000000; font-weight: bold;")
        botao_pesquisar_livro.clicked.connect(self.mostrar_livros)
        secao_livro.addWidget(botao_pesquisar_livro)

        return secao_livro

    def mostrar_usuarios(self):
        """Mostra todos os usuários cadastrados, no mínimo 20."""
        conexao, cursor = conectar()
        cursor.execute("SELECT * FROM usuarios LIMIT 20")
        usuarios = cursor.fetchall()
        conexao.close()

        # Limpa o campo de resultado e exibe a lista de usuários
        self.resultado_busca.clear()
        self.resultado_busca.append("Usuários Cadastrados:\n")
        for usuario in usuarios:
            self.resultado_busca.append(f"ID: {usuario[0]}, Nome: {usuario[1]}, Telefone: {usuario[4]}, Email: {usuario[5]}")

    def mostrar_livros(self):
        """Mostra todos os livros disponíveis."""
        conexao, cursor = conectar()
        cursor.execute("SELECT * FROM livros WHERE status = 'Disponível'")
        livros = cursor.fetchall()
        conexao.close()

        # Limpa o campo de resultado e exibe a lista de livros
        self.resultado_busca.clear()
        self.resultado_busca.append("Livros Disponíveis:\n")
        for livro in livros:
            self.resultado_busca.append(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, ISBN: {livro[3]}")

# Configuração do aplicativo
app = QApplication(sys.argv)
janela = BibliotecaApp()
janela.show()
sys.exit(app.exec_())
