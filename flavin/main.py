import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from interface import Interface

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
