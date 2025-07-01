import tkinter as tk


def infohelp(center_frame):
    # Limpa o conteúdo atual do frame central
    for widget in center_frame.winfo_children():
        widget.destroy()

    # ---------- Conteúdo da Ajuda ----------
    titulo = tk.Label(center_frame, text="🛟 AJUDA E SUPORTE",
                       font=("Arial", 20, "bold"), bg="white", fg="black")
    titulo.pack(pady=15)

    texto = (
        "✔️ Para registrar ponto, clique no botão 'Registrar Ponto'.\n\n"
        "✔️ Para cadastrar um novo funcionário, clique em 'Cadastro'.\n\n"
        "✔️ As informações são salvas automaticamente no banco de dados.\n\n"
        "✔️ Em caso de dúvidas técnicas, procure o setor de TI.\n\n"
        "✔️ Este sistema foi desenvolvido para fins educacionais no SENAC.\n\n"

        "Versão: 1.0.0\n\n"
        "\n\n"
        
        "          Uma parceria de Hexa & Aluv"
    )

    label_texto = tk.Label(center_frame, text=texto, font=("Arial", 12),
                            bg="white", fg="black", justify="left")
    label_texto.pack(padx=40, pady=15, anchor="w")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cadastro de Funcionário")
    root.geometry("800x400")
    root.configure(bg='#FFFFFF')

    app = infohelp(root)
    root.mainloop()