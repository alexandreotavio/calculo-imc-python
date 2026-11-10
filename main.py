import tkinter as tk
from tkinter import ttk

# Faixas de IMC: (limite superior, classificação)
FAIXAS_IMC = [
    (17.0, "Muito abaixo do peso"),
    (18.5, "Abaixo do peso"),
    (25.0, "Peso normal"),
    (30.0, "Acima do peso"),
    (35.0, "Obesidade I"),
    (40.0, "Obesidade II (severa)"),
]


def calcular_imc(altura_cm, peso_kg):
    altura_m = altura_cm / 100
    return peso_kg / (altura_m ** 2)


def classificar_imc(imc):
    for limite, classificacao in FAIXAS_IMC:
        if imc < limite:
            return classificacao
    return "Obesidade III (mórbida)"


def ler_numero(texto):
    """Converte o texto em número positivo, aceitando vírgula decimal."""
    valor = float(texto.strip().replace(",", "."))
    if not 0 < valor < float("inf"):
        raise ValueError
    return valor


class TelaIMC(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo do IMC - Índice de Massa Corporal")
        self.resizable(False, False)

        quadro = ttk.Frame(self, padding=16)
        quadro.grid()
        quadro.columnconfigure(2, weight=1)

        ttk.Label(quadro, text="Nome do Paciente:").grid(row=0, column=0, sticky="w", pady=4)
        self.nome = ttk.Entry(quadro, width=50)
        self.nome.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(quadro, text="Endereço Completo:").grid(row=1, column=0, sticky="w", pady=4)
        self.endereco = ttk.Entry(quadro, width=50)
        self.endereco.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(quadro, text="Altura (cm):").grid(row=2, column=0, sticky="w", pady=4)
        self.altura = ttk.Entry(quadro, width=16)
        self.altura.grid(row=2, column=1, sticky="w", pady=4)

        ttk.Label(quadro, text="Peso (Kg):").grid(row=3, column=0, sticky="nw", pady=4)
        self.peso = ttk.Entry(quadro, width=16)
        self.peso.grid(row=3, column=1, sticky="nw", pady=4)

        caixa = tk.Frame(quadro, bd=1, relief="solid", bg="white", width=260, height=110)
        caixa.grid(row=2, column=2, rowspan=2, sticky="nsew", padx=(12, 0), pady=4)
        caixa.grid_propagate(False)
        caixa.columnconfigure(0, weight=1)
        caixa.rowconfigure(0, weight=1)
        self.resultado = tk.Label(caixa, text="Resultado", bg="white", wraplength=240, justify="center")
        self.resultado.grid(sticky="nsew")

        botoes = ttk.Frame(quadro)
        botoes.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(14, 0))
        botoes.columnconfigure(2, weight=1)
        self.botao_calcular = ttk.Button(botoes, text="Calcular", command=self.calcular)
        self.botao_calcular.grid(row=0, column=0, padx=(0, 6))
        self.botao_reiniciar = ttk.Button(botoes, text="Reiniciar", command=self.reiniciar)
        self.botao_reiniciar.grid(row=0, column=1)
        ttk.Button(botoes, text="Sair", command=self.destroy).grid(row=0, column=2, sticky="e")

        self.nome.focus()

    def mostrar_erro(self, mensagem):
        self.resultado.config(text=mensagem, fg="#b00020")

    def calcular(self):
        nome = self.nome.get().strip()
        if not nome or not self.endereco.get().strip():
            self.mostrar_erro("Preencha o nome e o endereço do paciente.")
            return

        try:
            altura = ler_numero(self.altura.get())
            peso = ler_numero(self.peso.get())
        except ValueError:
            self.mostrar_erro("Informe altura e peso com números maiores que zero.")
            return

        imc = calcular_imc(altura, peso)
        imc_formatado = f"{imc:.2f}".replace(".", ",")
        self.resultado.config(
            text=f"{nome}\nIMC: {imc_formatado}\n{classificar_imc(imc)}",
            fg="black",
        )

    def reiniciar(self):
        for campo in (self.nome, self.endereco, self.altura, self.peso):
            campo.delete(0, tk.END)
        self.resultado.config(text="Resultado", fg="black")
        self.nome.focus()


if __name__ == "__main__":
    TelaIMC().mainloop()
