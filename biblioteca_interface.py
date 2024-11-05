import sys

from PyQt5.QtWidgets import (QApplication, QComboBox, QDateEdit, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QMessageBox,
                             QPushButton, QTextEdit, QVBoxLayout, QWidget)

# Dados iniciais: lista de livros e usuários
livros_mais_vendidos = [
    {"titulo": "Dom Quixote", "autor": "Miguel de Cervantes", "isbn": "978-0060934347", "status": "Disponível"},
    {"titulo": "Um Conto de Duas Cidades", "autor": "Charles Dickens", "isbn": "978-0141439600", "status": "Disponível"},
    {"titulo": "O Pequeno Príncipe", "autor": "Antoine de Saint-Exupéry", "isbn": "978-0156012195", "status": "Disponível"},
    {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "isbn": "978-0544003415", "status": "Disponível"}
]

usuarios_registrados = []

# Função para buscar livro por título ou autor
def buscar_livro(titulo_procurado, criterio):
    if criterio == "Título":
        return [livro for livro in livros_mais_vendidos if titulo_procurado.lower() in livro["titulo"].lower()]
    elif criterio == "Autor":
        return [livro for livro in livros_mais_vendidos if titulo_procurado.lower() in livro["autor"].lower()]

# Classe da Interface Gráfica
class BibliotecaApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configurações iniciais da janela
        self.setWindowTitle("Biblioteca - Gerenciamento")
        self.setGeometry(300, 300, 600, 500)
        
        # Layout principal
        layout_principal = QVBoxLayout()
        
        # Entrada de título ou autor para busca
        layout_busca = QHBoxLayout()
        self.label_criterio = QLabel("Buscar por:")
        self.criterio_busca = QComboBox()
        self.criterio_busca.addItems(["Título", "Autor"])
        
        self.label_titulo = QLabel("Buscar:")
        self.input_titulo = QLineEdit()
        self.botao_buscar = QPushButton("Buscar")
        self.botao_buscar.clicked.connect(self.mostrar_resultados_busca)
        
        layout_busca.addWidget(self.label_criterio)
        layout_busca.addWidget(self.criterio_busca)
        layout_busca.addWidget(self.label_titulo)
        layout_busca.addWidget(self.input_titulo)
        layout_busca.addWidget(self.botao_buscar)
        
        # Lista de resultados
        self.lista_resultados = QListWidget()
        self.lista_resultados.itemClicked.connect(self.exibir_detalhes_livro)
        
        # Seção de detalhes do livro
        self.label_detalhes = QLabel("Detalhes do Livro:")
        self.detalhes_texto = QTextEdit()
        self.detalhes_texto.setReadOnly(True)
        
        # Seção de Empréstimo
        layout_emprestimo = QHBoxLayout()
        self.label_usuario = QLabel("Usuário:")
        self.input_usuario = QLineEdit()
        self.botao_emprestar = QPushButton("Emprestar Livro")
        self.botao_emprestar.clicked.connect(self.emprestar_livro)
        
        layout_emprestimo.addWidget(self.label_usuario)
        layout_emprestimo.addWidget(self.input_usuario)
        layout_emprestimo.addWidget(self.botao_emprestar)
        
        # Botão para cadastrar novo usuário
        self.botao_cadastrar_usuario = QPushButton("Cadastrar Novo Usuário")
        self.botao_cadastrar_usuario.clicked.connect(self.cadastrar_usuario)
        
        # Adiciona componentes ao layout principal
        layout_principal.addLayout(layout_busca)
        layout_principal.addWidget(self.lista_resultados)
        layout_principal.addWidget(self.label_detalhes)
        layout_principal.addWidget(self.detalhes_texto)
        layout_principal.addLayout(layout_emprestimo)
        layout_principal.addWidget(self.botao_cadastrar_usuario)
        
        self.setLayout(layout_principal)

    def mostrar_resultados_busca(self):
        # Limpa a lista de resultados
        self.lista_resultados.clear()
        
        # Busca o título na lista de livros pelo critério selecionado
        titulo_procurado = self.input_titulo.text()
        criterio = self.criterio_busca.currentText()
        resultados = buscar_livro(titulo_procurado, criterio)
        
        # Exibe os resultados
        if resultados:
            for livro in resultados:
                self.lista_resultados.addItem(f"{livro['titulo']} - {livro['autor']} ({livro['status']})")
        else:
            QMessageBox.information(self, "Resultado da Busca", "Nenhum livro encontrado com o critério escolhido.")
    
    def exibir_detalhes_livro(self, item):
        # Exibe detalhes do livro selecionado
        titulo = item.text().split(" - ")[0]  # Pega o título a partir do item clicado
        livro = next((livro for livro in livros_mais_vendidos if livro["titulo"] == titulo), None)
        
        if livro:
            detalhes = f"Título: {livro['titulo']}\nAutor: {livro['autor']}\nISBN: {livro['isbn']}\nStatus: {livro['status']}"
            self.detalhes_texto.setText(detalhes)
    
    def emprestar_livro(self):
        # Empresta o livro selecionado para um usuário
        titulo = self.lista_resultados.currentItem().text().split(" - ")[0]
        usuario_nome = self.input_usuario.text().strip()
        
        # Verifica se o usuário existe
        usuario = next((user for user in usuarios_registrados if user["nome"].lower() == usuario_nome.lower()), None)
        
        if not usuario:
            QMessageBox.warning(self, "Usuário não encontrado", "Usuário não cadastrado. Por favor, cadastre o usuário.")
            return
        
        livro = next((livro for livro in livros_mais_vendidos if livro["titulo"] == titulo), None)
        
        if livro and livro["status"] == "Disponível":
            livro["status"] = f"Emprestado para {usuario['nome']}"
            QMessageBox.information(self, "Empréstimo", f"Você emprestou o livro '{livro['titulo']}' para {usuario['nome']}.")
            self.mostrar_resultados_busca()  # Atualiza a lista
        else:
            QMessageBox.warning(self, "Indisponível", "Este livro já está emprestado ou não foi selecionado.")
    
    def cadastrar_usuario(self):
        # Cadastra um novo usuário
        nome, ok = QInputDialog.getText(self, "Cadastrar Usuário", "Digite o nome do usuário:")
        if not ok or not nome.strip():
            return
        
        data_nascimento, ok = QInputDialog.getText(self, "Data de Nascimento", "Digite a data de nascimento (DD/MM/AAAA):")
        cidade, ok = QInputDialog.getText(self, "Cidade", "Digite a cidade:")
        bairro, ok = QInputDialog.getText(self, "Bairro", "Digite o bairro:")
        
        usuario = {"nome": nome, "data_nascimento": data_nascimento, "cidade": cidade, "bairro": bairro}
        usuarios_registrados.append(usuario)
        QMessageBox.information(self, "Cadastro", f"Usuário '{nome}' cadastrado com sucesso.")

# Execução do aplicativo
app = QApplication(sys.argv)
biblioteca_app = BibliotecaApp()
biblioteca_app.show()
sys.exit(app.exec_())

