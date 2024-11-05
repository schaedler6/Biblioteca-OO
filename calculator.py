import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Erro: Divisão por zero"

def power(x, y):
    return x ** y

def square_root(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return "Erro: Número negativo"

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def show_menu():
    print("\nCalculadora Científica")
    print("Escolha uma operação:")
    print("1. Soma")
    print("2. Subtração")
    print("3. Multiplicação")
    print("4. Divisão")
    print("5. Potência")
    print("6. Raiz Quadrada")
    print("7. Seno")
    print("8. Cosseno")
    print("9. Tangente")
    print("0. Sair")

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Digite o número da operação desejada: ")

        if choice == '0':
            print("Encerrando a calculadora.")
            break

        if choice in ['1', '2', '3', '4', '5']:
            x = float(input("Digite o primeiro número: "))
            y = float(input("Digite o segundo número: "))

            if choice == '1':
                print("Resultado:", add(x, y))
            elif choice == '2':
                print("Resultado:", subtract(x, y))
            elif choice == '3':
                print("Resultado:", multiply(x, y))
            elif choice == '4':
                print("Resultado:", divide(x, y))
            elif choice == '5':
                print("Resultado:", power(x, y))

        elif choice == '6':
            x = float(input("Digite o número: "))
            print("Resultado:", square_root(x))

        elif choice in ['7', '8', '9']:
            x = float(input("Digite o ângulo em graus: "))
            if choice == '7':
                print("Resultado:", sin(x))
            elif choice == '8':
                print("Resultado:", cos(x))
            elif choice == '9':
                print("Resultado:", tan(x))

        else:
            print("Opção inválida. Tente novamente.")
