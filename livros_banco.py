import os
import sqlite3

# Caminho para o banco de dados
caminho_banco = 'E:/SCHAEDLER/PythonSenac/biblioteca.db'

# Criação do diretório e banco de dados, se ainda não existir
os.makedirs(os.path.dirname(caminho_banco), exist_ok=True)

def conectar():
    """Conecta ao banco de dados e retorna a conexão e o cursor."""
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    return conexao, cursor

def criar_tabelas():
    """Cria as tabelas de livros e usuários se não existirem."""
    conexao, cursor = conectar()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        isbn TEXT UNIQUE,
        status TEXT DEFAULT "Disponível"
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT,
        cidade TEXT,
        bairro TEXT,
        telefone TEXT,
        email TEXT
    )
    ''')
    conexao.commit()
    conexao.close()

def adicionar_livro(titulo, autor, isbn):
    """Adiciona um novo livro ao banco de dados."""
    conexao, cursor = conectar()
    try:
        cursor.execute("INSERT INTO livros (titulo, autor, isbn) VALUES (?, ?, ?)", (titulo, autor, isbn))
        conexao.commit()
    except sqlite3.IntegrityError:
        print(f"Livro '{titulo}' já existe no banco de dados.")
    finally:
        conexao.close()

def inicializar_livros():
    """Inicializa o banco com pelo menos 20 livros."""
    livros_iniciais = [
        ("Dom Quixote", "Miguel de Cervantes", "978-0060934347"),
        ("Um Conto de Duas Cidades", "Charles Dickens", "978-0141439600"),
        ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "978-0156012195"),
        # Adicione mais livros aqui
        ("1984", "George Orwell", "978-0451524935"),
        ("A Revolução dos Bichos", "George Orwell", "978-0451526342"),
        ("Cem Anos de Solidão", "Gabriel García Márquez", "978-0307389732"),
        ("O Senhor dos Anéis", "J.R.R. Tolkien", "978-0544003415"),
        ("Orgulho e Preconceito", "Jane Austen", "978-1503290563"),
        ("Crime e Castigo", "Fiódor Dostoiévski", "978-0143058144"),
        ("O Grande Gatsby", "F. Scott Fitzgerald", "978-0743273565"),
        ("Guerra e Paz", "Liev Tolstói", "978-0140447934"),
        ("Moby Dick", "Herman Melville", "978-1503280786"),
        ("A Odisséia", "Homero", "978-0140268867"),
        ("Ilíada", "Homero", "978-0140275360"),
        ("O Morro dos Ventos Uivantes", "Emily Brontë", "978-0141439556"),
        ("As Aventuras de Sherlock Holmes", "Arthur Conan Doyle", "978-1508475311"),
        ("Frankenstein", "Mary Shelley", "978-0486282114"),
        ("Drácula", "Bram Stoker", "978-0486411095"),
        ("O Retrato de Dorian Gray", "Oscar Wilde", "978-0141439570"),
        ("A Divina Comédia", "Dante Alighieri", "978-0142437223")
    ]
    
    for titulo, autor, isbn in livros_iniciais:
        adicionar_livro(titulo, autor, isbn)

# Executa a criação das tabelas e inicialização dos livros
criar_tabelas()
inicializar_livros()
