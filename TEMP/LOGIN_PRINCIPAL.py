import tkinter as tk
from tkinter import *
from registro_funcionario import RegistroFuncionario  # <- Nome do arquivo onde está a classe

def main():
    root = tk.Tk()
    root.title("Menu Principal")
    root.geometry("500x300")

    Label(root, text="MENU PRINCIPAL", font=("Arial", 18, "bold")).pack(pady=20)

    Button(root, text="Cadastrar Funcionário", width=25, height=2,
           command=lambda: RegistroFuncionario(master=root)).pack(pady=10)

    Button(root, text="Sair", width=25, height=2, command=root.destroy).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()


'''
SEPARA A ABAS POR USUARIO:

SEPARA, ANALISANDO O REGISTRO NO BANCO DE DADOS, E REDIRECIONA PARA AS DEVIDAS PERMISSOES

SENDO ADM PUXA PAGINA PRINCIAPL COM MULTIPLAS OPÇOES

E USUARIO, PARA REGISTRO DE PONTO


***

PAGINA MUDA PRA UMA MENSAGEM DE LOGIM, ADM OU USER




'''