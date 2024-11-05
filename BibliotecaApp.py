import sys

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (QAction, QApplication, QDateEdit, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QMainWindow,
                             QMenuBar, QMessageBox, QPushButton,
                             QStackedWidget, QVBoxLayout, QWidget)


# Classe para representar o Usuário
class Usuario:
    def __init__(self, nome, data_nascimento, cidade, bairro):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cidade = cidade
        self.bairro = bairro

# Interface da Biblioteca com Estilo Atualizado
class BibliotecaApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Biblioteca - Sistema de Gerenciamento")
        self.usuarios = [
            Usuario("Carlos", "1990-05-10", "São Paulo", "Centro"),
            Usuario("Maria", "1985-02-15", "Rio de Janeiro", "Botafogo")
        ]
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Configurações de estilo
        self.setStyleSheet("background-color: #1c1c1c; color: #09c0ff;")
        
        # Fonte estilo "neon"
        fonte_neon = QFont("Arial", 10, QFont.Bold)
        data_fonte = QFont("Arial", 12, QFont.Bold)

        # Exibir a data atual de forma destacada
        data_atual = QDate.currentDate().toString("dd MMMM yyyy")
        data_label = QLabel(data_atual)
        data_label.setFont(data_fonte)
        data_label.setStyleSheet("color: #09c0ff; padding: 10px;")
        layout.addWidget(data_label, alignment=Qt.AlignCenter)

        # Botão de Voltar
        voltar_btn = QPushButton("Voltar")
        voltar_btn.setFont(fonte_neon)
        voltar_btn.setStyleSheet("background-color: #09c0ff; color: #1c1c1c; padding: 5px; border-radius: 10px;")
        voltar_btn.clicked.connect(self.voltar)
        layout.addWidget(voltar_btn, alignment=Qt.AlignLeft)

        # Campos para pesquisa de usuário
        layout.addWidget(QLabel("Pesquisar Usuário:", font=fonte_neon))
        self.nome_usuario_input = QLineEdit()
        self.nome_usuario_input.setPlaceholderText("Nome do Usuário")
        self.data_nascimento_input = QLineEdit()
        self.data_nascimento_input.setPlaceholderText("Data de Nascimento (AAAA-MM-DD)")
        self.cidade_input = QLineEdit()
        self.cidade_input.setPlaceholderText("Cidade")
        self.bairro_input = QLineEdit()
        self.bairro_input.setPlaceholderText("Bairro")
        
        layout.addWidget(self.nome_usuario_input)
        layout.addWidget(self.data_nascimento_input)
        layout.addWidget(self.cidade_input)
        layout.addWidget(self.bairro_input)
        
        # Botão de pesquisa de usuário
        buscar_usuario_btn = QPushButton("Buscar Usuário")
        buscar_usuario_btn.setFont(fonte_neon)
        buscar_usuario_btn.setStyleSheet("background-color: #09c0ff; color: #1c1c1c; padding: 10px; border-radius: 10px;")
        buscar_usuario_btn.clicked.connect(self.buscar_usuario)
        layout.addWidget(buscar_usuario_btn)

        # Campo para pesquisa de livro
        layout.addWidget(QLabel("Pesquisar Livro:", font=fonte_neon))
        self.busca_livro_input = QLineEdit()
        self.busca_livro_input.setPlaceholderText("Título ou Autor")
        layout.addWidget(self.busca_livro_input)
        
        # Botão de pesquisa de livro
        buscar_livro_btn = QPushButton("Buscar Livro")
        buscar_livro_btn.setFont(fonte_neon)
        buscar_livro_btn.setStyleSheet("background-color: #09c0ff; color: #1c1c1c; padding: 10px; border-radius: 10px;")
        buscar_livro_btn.clicked.connect(self.buscar_livro)
        layout.addWidget(buscar_livro_btn)

        # Seletor de data para entrega do livro
        layout.addWidget(QLabel("Data de Entrega do Livro:", font=fonte_neon))
        self.data_entrega = QDateEdit()
        self.data_entrega.setCalendarPopup(True)
        self.data_entrega.setFont(fonte_neon)
        self.data_entrega.setStyleSheet("color: #09c0ff; background-color: #333333; border: 1px solid #09c0ff; padding: 5px; border-radius: 5px;")
        layout.addWidget(self.data_entrega)
        
        # Lista de resultados
        self.resultados_lista = QListWidget()
        self.resultados_lista.setStyleSheet("background-color: #333333; color: #09c0ff;")
        layout.addWidget(self.resultados_lista)

        self.setLayout(layout)

    def buscar_usuario(self):
        nome = self.nome_usuario_input.text().lower()
        data_nascimento = self.data_nascimento_input.text()
        cidade = self.cidade_input.text().lower()
        bairro = self.bairro_input.text().lower()
        
        resultados = [
            usuario for usuario in self.usuarios
            if (not nome or nome in usuario.nome.lower()) and
               (not data_nascimento or data_nascimento == usuario.data_nascimento) and
               (not cidade or cidade in usuario.cidade.lower()) and
               (not bairro or bairro in usuario.bairro.lower())
        ]
        
        self.resultados_lista.clear()
        if resultados:
            for usuario in resultados:
                self.resultados_lista.addItem(
                    f"Nome: {usuario.nome}, Nascimento: {usuario.data_nascimento}, Cidade: {usuario.cidade}, Bairro: {usuario.bairro}"
                )
        else:
            self.resultados_lista.addItem("Nenhum usuário encontrado.")

    def buscar_livro(self):
        termo = self.busca_livro_input.text().lower()
        livros = [
            {"titulo": "Dom Quixote", "autor": "Miguel de Cervantes"},
            {"titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry"}
        ]
        
        resultados = [
            livro for livro in livros
            if termo in livro["titulo"].lower() or termo in livro["autor"].lower()
        ]
        
        self.resultados_lista.clear()
        if resultados:
            for livro in resultados:
                self.resultados_lista.addItem(f"Título: {livro['titulo']}, Autor: {livro['autor']}")
        else:
            self.resultados_lista.addItem("Nenhum livro encontrado.")

    def voltar(self):
        self.main_window.mostrar_menu_principal()

# Janela Principal com Menu para alternar entre as janelas
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerenciamento - Biblioteca")
        self.setGeometry(300, 200, 800, 600)

        # Menu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        
        view_menu = menu_bar.addMenu("Visualizar")
        
        biblioteca_action = QAction("Biblioteca", self)
        biblioteca_action.triggered.connect(self.mostrar_biblioteca)
        view_menu.addAction(biblioteca_action)

        # Stack de Widgets
        self.stacked_widget = QStackedWidget()
        self.biblioteca_app = BibliotecaApp(self)
        
        self.stacked_widget.addWidget(self.biblioteca_app)
        
        self.setCentralWidget(self.stacked_widget)
        self.mostrar_biblioteca()

    def mostrar_biblioteca(self):
        self.stacked_widget.setCurrentWidget(self.biblioteca_app)

    def mostrar_menu_principal(self):
        # Função para exibir o menu principal (se houver)
        self.mostrar_biblioteca()

# Execução do aplicativo
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
