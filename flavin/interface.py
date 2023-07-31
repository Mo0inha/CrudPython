import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from post import criar_filme
from get import exibir_filmes, selecionar_filme
from put import salvar_modificacoes
from delete import deletar_filme


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD de Filmes")
        self.root.geometry("800x500")

        self.frame_cadastro = ttk.LabelFrame(self.root, text="Cadastro de Filmes")
        self.frame_cadastro.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.frame_exibicao = ttk.LabelFrame(self.root, text="Filmes Cadastrados")
        self.frame_exibicao.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(self.frame_cadastro, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.entry_titulo = ttk.Entry(self.frame_cadastro, width=30)
        self.entry_titulo.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(self.frame_cadastro, text="Diretor:").grid(row=1, column=0, sticky=tk.W)
        self.entry_diretor = ttk.Entry(self.frame_cadastro, width=30)
        self.entry_diretor.grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(self.frame_cadastro, text="Ano:").grid(row=2, column=0, sticky=tk.W)
        self.entry_ano = ttk.Entry(self.frame_cadastro, width=10)
        self.entry_ano.grid(row=2, column=1, sticky=tk.W, padx=5)

        ttk.Button(self.frame_cadastro, text="Selecionar Imagem", command=self.selecionar_imagem).grid(
            row=3, column=0, columnspan=2, pady=5
        )

        self.button_cadastrar = ttk.Button(self.frame_cadastro, text="Cadastrar", command=self.criar_filme)
        self.button_cadastrar.grid(row=4, column=0, columnspan=2, pady=5)

        self.entry_busca = ttk.Entry(self.frame_exibicao, width=30)
        self.entry_busca.pack(side=tk.LEFT, padx=5)

        self.button_pesquisar = ttk.Button(self.frame_exibicao, text="Pesquisar", command=self.exibir_filmes)
        self.button_pesquisar.pack(side=tk.LEFT)

        self.listbox_filmes = tk.Listbox(self.frame_exibicao, width=60)
        self.listbox_filmes.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.listbox_filmes.bind("<<ListboxSelect>>", self.mostrar_detalhes_filme)

        scrollbar = tk.Scrollbar(self.frame_exibicao)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_filmes.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_filmes.yview)

        self.frame_detalhes = ttk.LabelFrame(self.root, text="Detalhes do Filme")
        self.frame_detalhes.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(self.frame_detalhes, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.label_titulo = ttk.Label(self.frame_detalhes, text="")
        self.label_titulo.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.frame_detalhes, text="Diretor:").grid(row=1, column=0, sticky=tk.W)
        self.label_diretor = ttk.Label(self.frame_detalhes, text="")
        self.label_diretor.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.frame_detalhes, text="Ano:").grid(row=2, column=0, sticky=tk.W)
        self.label_ano = ttk.Label(self.frame_detalhes, text="")
        self.label_ano.grid(row=2, column=1, sticky=tk.W)

        self.label_imagem = ttk.Label(self.frame_detalhes)
        self.label_imagem.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        self.button_modificar = ttk.Button(
            self.frame_detalhes, text="Modificar", command=self.abrir_janela_modificar_filme
        )
        self.button_modificar.grid(row=3, column=0, pady=5)

        self.button_deletar = ttk.Button(self.frame_detalhes, text="Deletar", command=self.deletar_filme)
        self.button_deletar.grid(row=3, column=1, pady=5)

    def criar_filme(self):
        titulo = self.entry_titulo.get().strip()
        diretor = self.entry_diretor.get().strip()
        ano = self.entry_ano.get().strip()

        if not titulo or not diretor or not ano:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        criar_filme(titulo, diretor, ano, self.imagem_path)

        self.entry_titulo.delete(0, tk.END)
        self.entry_diretor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)

        self.exibir_filmes()


    def exibir_filmes(self):
        self.listbox_filmes.delete(0, tk.END)

        filmes = exibir_filmes(self.entry_busca.get().strip())

        for filme in filmes:
            self.listbox_filmes.insert(
                tk.END,
                f"ID: {filme['id']}, Título: {filme['titulo']}, Diretor: {filme['diretor']}, Ano: {filme['ano']}",
            )

    def mostrar_detalhes_filme(self, event):
        selection = event.widget.curselection()

        if selection:
            index = selection[0]
            filme_id = self.listbox_filmes.get(index).split("ID: ")[1].split(",")[0]
            filme = selecionar_filme(filme_id)

            self.label_titulo.config(text=filme["titulo"])
            self.label_diretor.config(text=filme["diretor"])
            self.label_ano.config(text=filme["ano"])

            imagem_path = filme["imagem"]
            imagem = Image.open(imagem_path)
            imagem.thumbnail((200, 300))
            imagem = ImageTk.PhotoImage(imagem)

            self.label_imagem.config(image=imagem)
            self.label_imagem.image = imagem

    def abrir_janela_modificar_filme(self):
        selection = self.listbox_filmes.curselection()

        if selection:
            index = selection[0]
            filme_id = self.listbox_filmes.get(index).split("ID: ")[1].split(",")[0]

            janela_modificar_filme = tk.Toplevel(self.root)
            janela_modificar_filme.title("Modificar Filme")

            self.modificar_filme(filme_id, janela_modificar_filme)

    def modificar_filme(self, filme_id, janela_modificar_filme):
        titulo = ttk.Label(janela_modificar_filme, text="Título:")
        titulo.grid(row=0, column=0, sticky=tk.W)
        entry_titulo = ttk.Entry(janela_modificar_filme, width=30)
        entry_titulo.grid(row=0, column=1, sticky=tk.W)

        diretor = ttk.Label(janela_modificar_filme, text="Diretor:")
        diretor.grid(row=1, column=0, sticky=tk.W)
        entry_diretor = ttk.Entry(janela_modificar_filme, width=30)
        entry_diretor.grid(row=1, column=1, sticky=tk.W)

        ano = ttk.Label(janela_modificar_filme, text="Ano:")
        ano.grid(row=2, column=0, sticky=tk.W)
        entry_ano = ttk.Entry(janela_modificar_filme, width=10)
        entry_ano.grid(row=2, column=1, sticky=tk.W)

        filme = selecionar_filme(filme_id)

        entry_titulo.insert(tk.END, filme["titulo"])
        entry_diretor.insert(tk.END, filme["diretor"])
        entry_ano.insert(tk.END, filme["ano"])

        button_salvar = ttk.Button(
            janela_modificar_filme,
            text="Salvar",
            command=lambda: self.salvar_modificacoes(filme_id, entry_titulo.get(), entry_diretor.get(), entry_ano.get()),
        )
        button_salvar.grid(row=3, column=0, columnspan=2, pady=5)

    def salvar_modificacoes(self, filme_id, titulo, diretor, ano):
        if not titulo or not diretor or not ano:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        salvar_modificacoes(filme_id, titulo, diretor, ano)

        messagebox.showinfo("Sucesso", "Modificações salvas com sucesso.")

        self.exibir_filmes()

    def deletar_filme(self):
        selection = self.listbox_filmes.curselection()

        if selection:
            index = selection[0]
            filme_id = self.listbox_filmes.get(index).split("ID: ")[1].split(",")[0]

            confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar o filme?")

            if confirmar:
                deletar_filme(filme_id)

                messagebox.showinfo("Sucesso", "Filme deletado com sucesso.")

                self.exibir_filmes()

    def selecionar_imagem(self):
        imagem_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.jpeg;*.png")])

        if imagem_path:
            self.imagem_path = imagem_path


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
