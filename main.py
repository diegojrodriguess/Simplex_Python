import tkinter as tk
from tkinter import ttk, messagebox
from scipy.optimize import linprog
import numpy as np

class LinearProgrammingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação de Programação Linear")

        self.num_vars_label = tk.Label(root, text="Número de Variáveis:")
        self.num_vars_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.num_vars_entry = tk.Entry(root)
        self.num_vars_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.num_vars_button = tk.Button(root, text="Confirmar", command=self.get_variables)
        self.num_vars_button.grid(row=0, column=2, padx=10, pady=10)

    def get_variables(self):
        try:
            self.num_vars = int(self.num_vars_entry.get())
            if self.num_vars > 0:
                self.display_variable_inputs()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido de variáveis.")

    def display_variable_inputs(self):
        self.variable_labels = []
        self.variable_entries = []
        self.profit_entries = []

        for i in range(self.num_vars):
            var_label = tk.Label(self.root, text=f"Nome da Variável {i+1}:")
            var_label.grid(row=i+1, column=0, padx=10, pady=5)
            
            var_entry = tk.Entry(self.root)
            var_entry.grid(row=i+1, column=1, padx=10, pady=5)
            
            profit_label = tk.Label(self.root, text=f"Valor de Lucro {i+1}:")
            profit_label.grid(row=i+1, column=2, padx=10, pady=5)
            
            profit_entry = tk.Entry(self.root)
            profit_entry.grid(row=i+1, column=3, padx=10, pady=5)
            
            self.variable_labels.append(var_label)
            self.variable_entries.append(var_entry)
            self.profit_entries.append(profit_entry)
        
        self.num_restrictions_label = tk.Label(self.root, text="Número de Restrições:")
        self.num_restrictions_label.grid(row=self.num_vars + 1, column=0, padx=10, pady=10)
        
        self.num_restrictions_entry = tk.Entry(self.root)
        self.num_restrictions_entry.grid(row=self.num_vars + 1, column=1, padx=10, pady=10)
        
        self.num_restrictions_button = tk.Button(self.root, text="Confirmar", command=self.get_restrictions)
        self.num_restrictions_button.grid(row=self.num_vars + 1, column=2, padx=10, pady=10)

    def get_restrictions(self):
        try:
            self.num_restrictions = int(self.num_restrictions_entry.get())
            if self.num_restrictions > 0:
                self.display_restriction_inputs()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido de restrições.")

    def display_restriction_inputs(self):
        self.restriction_labels = []
        self.restriction_entries = []
        self.quantity_entries = []
        self.max_entries = []

        for i in range(self.num_restrictions):
            rest_label = tk.Label(self.root, text=f"Nome da Restrição {i+1}:")
            rest_label.grid(row=self.num_vars + 2 + i, column=0, padx=10, pady=5)
            
            rest_entry = tk.Entry(self.root)
            rest_entry.grid(row=self.num_vars + 2 + i, column=1, padx=10, pady=5)
            
            quantities = []
            for j in range(self.num_vars):
                qty_label = tk.Label(self.root, text=f"Qtd. para {self.variable_entries[j].get()}:")
                qty_label.grid(row=self.num_vars + 2 + i, column=2 + j*2, padx=10, pady=5)
                
                qty_entry = tk.Entry(self.root)
                qty_entry.grid(row=self.num_vars + 2 + i, column=3 + j*2, padx=10, pady=5)
                quantities.append(qty_entry)
            
            max_label = tk.Label(self.root, text="Valor Máximo:")
            max_label.grid(row=self.num_vars + 2 + i, column=2 + self.num_vars*2, padx=10, pady=5)
            
            max_entry = tk.Entry(self.root)
            max_entry.grid(row=self.num_vars + 2 + i, column=3 + self.num_vars*2, padx=10, pady=5)
            
            self.restriction_labels.append(rest_label)
            self.restriction_entries.append(rest_entry)
            self.quantity_entries.append(quantities)
            self.max_entries.append(max_entry)
        
        self.alter_button = tk.Button(self.root, text="Inserir Alterações", command=self.alter_quantities)
        self.alter_button.grid(row=self.num_vars + 2 + self.num_restrictions, column=0, columnspan=2, padx=10, pady=10)

    def alter_quantities(self):
        self.alteration_labels = []
        self.alteration_entries = []

        for i in range(self.num_restrictions):
            alt_label = tk.Label(self.root, text=f"Alteração na Quantidade da Restrição {self.restriction_entries[i].get()}:")
            alt_label.grid(row=self.num_vars + 3 + self.num_restrictions + i, column=0, padx=10, pady=5)
            
            alt_entry = tk.Entry(self.root)
            alt_entry.grid(row=self.num_vars + 3 + self.num_restrictions + i, column=1, padx=10, pady=5)
            
            self.alteration_labels.append(alt_label)
            self.alteration_entries.append(alt_entry)
        
        self.confirm_button = tk.Button(self.root, text="Confirmar Tudo", command=self.confirm_all)
        self.confirm_button.grid(row=self.num_vars + 4 + self.num_restrictions + len(self.alteration_labels), column=0, columnspan=2, padx=10, pady=10)

    def confirm_all(self):
        # Arrays para armazenar os dados
        self.c = []
        self.A = []
        self.b = []
        self.alterations = []

        # Captura de coeficientes da função objetivo
        for profit_entry in self.profit_entries:
            profit_value = -float(profit_entry.get())  # Multiplicar por -1 para maximização
            self.c.append(profit_value)

        # Captura de restrições e quantidades
        for quantities, max_entry in zip(self.quantity_entries, self.max_entries):
            rest_quantities = [float(qty_entry.get()) for qty_entry in quantities]
            max_value = float(max_entry.get())
            self.A.append(rest_quantities)
            self.b.append(max_value)

        # Captura de alterações
        for alt_entry in self.alteration_entries:
            alt_value = float(alt_entry.get())
            self.alterations.append(alt_value)

        # Resolver o problema com linprog
        res = linprog(self.c, A_ub=self.A, b_ub=self.b, bounds=(0, None), method='highs')

        if res.success:
            # Calcular preços sombra usando a solução dual
            shadow_prices = res.get('ineqlin', {}).get('marginals', np.zeros(len(self.b)))

            # Exibir resultados em uma única janela
            self.display_results(res, shadow_prices)

            # Verificar se há alterações
            if any(self.alterations):
                self.check_alterations(res, shadow_prices)
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar uma solução ótima.")

    def display_results(self, res, shadow_prices):
        # Exibição dos valores das variáveis, lucro ótimo e preços sombra em uma única janela
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Resultados da Otimização")

        row = 0
        tk.Label(self.result_window, text="Valores Ótimos das Variáveis:").grid(row=row, column=0, padx=10, pady=10)
        row += 1
        for i, x in enumerate(res.x):
            tk.Label(self.result_window, text=f"{self.variable_entries[i].get()}: {x:.2f}").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        tk.Label(self.result_window, text=f"Lucro Ótimo: {res.fun * -1:.2f}").grid(row=row, column=0, padx=10, pady=10)
        row += 1

        tk.Label(self.result_window, text="Preços Sombra:").grid(row=row, column=0, padx=10, pady=10)
        row += 1
        for i, shadow_price in enumerate(shadow_prices):
            text = f"Restrição {self.restriction_entries[i].get()}: {shadow_price:.2f}" if shadow_price is not None else "Preço sombra não calculável"
            tk.Label(self.result_window, text=text).grid(row=row, column=0, padx=10, pady=5)
            row += 1

    def check_alterations(self, res, shadow_prices):
        row = 0
        tk.Label(self.result_window, text="Verificação de Alterações nas Restrições:").grid(row=row, column=1, padx=10, pady=10)
        row += 1

        alterations_viable = True

        for i, (alter_value, shadow_price) in enumerate(zip(self.alterations, shadow_prices)):
            feasible = alter_value * shadow_price >= 0
            if not feasible:
                alterations_viable = False
            status = "Viável" if feasible else "Inviável"
            tk.Label(self.result_window, text=f"Alteração na Restrição {self.restriction_entries[i].get()}: {alter_value:.2f} - {status}").grid(row=row, column=1, padx=10, pady=5)
            row += 1

        if alterations_viable:
            # Aplicar alterações nas restrições
            new_b = [b + alteration for b, alteration in zip(self.b, self.alterations)]
            # Resolver novamente o problema com as novas restrições
            new_res = linprog(self.c, A_ub=self.A, b_ub=new_b, bounds=(0, None), method='highs')
            if new_res.success:
                # Exibir novos resultados na mesma janela
                tk.Label(self.result_window, text=f"Novo Lucro Ótimo: {new_res.fun * -1:.2f}").grid(row=row, column=1, padx=10, pady=10)
                row += 1
                for i, x in enumerate(new_res.x):
                    tk.Label(self.result_window, text=f"{self.variable_entries[i].get()}: {x:.2f}").grid(row=row, column=1, padx=10, pady=5)
                    row += 1
            else:
                messagebox.showerror("Erro", "Não foi possível encontrar uma solução ótima após as alterações.")
        else:
            tk.Label(self.result_window, text="Nenhuma alteração viável.").grid(row=row, column=1, padx=10, pady=10)
            row += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearProgrammingApp(root)
    root.mainloop()
