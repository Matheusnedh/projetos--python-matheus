import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any


class Produto:
    """Classe para representar um produto"""
   
    def __init__(self, numero: int, preco_unitario: float, refrigeracao: bool, categoria: str):
        self.numero = numero
        self.preco_unitario = preco_unitario
        self.refrigeracao = refrigeracao
        self.categoria = categoria
        self.custo_estocagem = 0.0
        self.imposto = 0.0
        self.preco_final = 0.0
        self.classificacao = ""
       
        self._calcular_valores()
   
    def _calcular_valores(self):
        """Calcula custo de estocagem, imposto, preço final e classificação"""
        self.custo_estocagem = self._calcular_custo_estocagem()
        self.imposto = self._calcular_imposto()
        self.preco_final = self.preco_unitario + self.custo_estocagem + self.imposto
        self.classificacao = self._classificar_produto()
   
    def _calcular_custo_estocagem(self) -> float:
        """Calcula o custo de estocagem baseado nas regras de negócio"""
        if self.preco_unitario < 20:
            custos = {"A": 5.0, "L": 2.0, "V": 4.0}
            return custos.get(self.categoria, 0.0)
        elif 20 <= self.preco_unitario < 100:
            return 6.0 if self.refrigeracao else 0.0
        else:  # preco_unitario >= 100
            if self.refrigeracao:
                return 8.0 if self.categoria == "A" else 5.0
            else:
                return 1.0 if self.categoria == "L" else 0.0
   
    def _calcular_imposto(self) -> float:
        """Calcula o imposto baseado nas regras de negócio"""
        if self.categoria == "A" and self.refrigeracao:
            return self.preco_unitario * 0.04
        else:
            return self.preco_unitario * 0.02
   
    def _classificar_produto(self) -> str:
        """Classifica o produto baseado no preço final"""
        if self.preco_final <= 20:
            return "Barato"
        elif self.preco_final <= 100:
            return "Normal"
        else:
            return "Caro"


class SistemaAnaliseProdutos:
    """Sistema principal de análise de produtos com interface TKinter"""
   
    def __init__(self):
        self.root = tk.Tk()
        self.produtos: List[Produto] = []
        self.max_produtos = 12
       
        # Variáveis de controle
        self.var_preco = tk.StringVar()
        self.var_refrigeracao = tk.BooleanVar()
        self.var_categoria = tk.StringVar(value="A")
       
        # Variáveis para estatísticas
        self.var_contador = tk.StringVar(value="0/12")
        self.var_media_adicionais = tk.StringVar(value="R$ 0,00")
        self.var_maior_preco = tk.StringVar(value="R$ 0,00")
        self.var_menor_preco = tk.StringVar(value="R$ 0,00")
        self.var_total_impostos = tk.StringVar(value="R$ 0,00")
        self.var_count_barato = tk.StringVar(value="0")
        self.var_count_normal = tk.StringVar(value="0")
        self.var_count_caro = tk.StringVar(value="0")
       
        self.criar_interface()
   
    def criar_interface(self):
        """Cria a interface gráfica principal"""
        self.root.title("Sistema de Análise de Produtos")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
       
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
       
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Análise de Produtos",
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
       
        # Frame de cadastro (esquerda)
        self.criar_frame_cadastro(main_frame)
       
        # Frame de visualização (direita)
        self.criar_frame_visualizacao(main_frame)
       
        # Frame de estatísticas (embaixo)
        self.criar_frame_estatisticas(main_frame)
       
        # Frame de controles (embaixo)
        self.criar_frame_controles(main_frame)
   
    def criar_frame_cadastro(self, parent):
        """Cria o frame de cadastro de produtos"""
        frame_cadastro = ttk.LabelFrame(parent, text="Cadastro de Produto", padding="10")
        frame_cadastro.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
       
        # Contador de produtos
        contador_label = ttk.Label(frame_cadastro, text="Produtos cadastrados:")
        contador_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
       
        contador_valor = ttk.Label(frame_cadastro, textvariable=self.var_contador,
                                  font=("Arial", 12, "bold"))
        contador_valor.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
       
        # Preço unitário
        ttk.Label(frame_cadastro, text="Preço Unitário (R$):").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_preco = ttk.Entry(frame_cadastro, textvariable=self.var_preco, width=15)
        entry_preco.grid(row=1, column=1, sticky=tk.W, pady=5)
       
        # Refrigeração
        check_refrigeracao = ttk.Checkbutton(frame_cadastro, text="Necessita refrigeração",
                                           variable=self.var_refrigeracao)
        check_refrigeracao.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
       
        # Categoria
        ttk.Label(frame_cadastro, text="Categoria:").grid(row=3, column=0, sticky=tk.W, pady=5)
       
        frame_categoria = ttk.Frame(frame_cadastro)
        frame_categoria.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
       
        ttk.Radiobutton(frame_categoria, text="Alimentação", variable=self.var_categoria,
                       value="A").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(frame_categoria, text="Limpeza", variable=self.var_categoria,
                       value="L").grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Radiobutton(frame_categoria, text="Vestuário", variable=self.var_categoria,
                       value="V").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
       
        # Botão adicionar
        btn_adicionar = ttk.Button(frame_cadastro, text="Adicionar Produto",
                                  command=self.adicionar_produto)
        btn_adicionar.grid(row=5, column=0, columnspan=2, pady=20)
       
        # Bind Enter key to add product
        entry_preco.bind('<Return>', lambda e: self.adicionar_produto())
   
    def criar_frame_visualizacao(self, parent):
        """Cria o frame de visualização dos produtos"""
        frame_viz = ttk.LabelFrame(parent, text="Produtos Cadastrados", padding="10")
        frame_viz.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_viz.columnconfigure(0, weight=1)
        frame_viz.rowconfigure(0, weight=1)
       
        # Treeview para mostrar produtos
        columns = ("Produto", "Preço", "Refrig.", "Categ.", "Custo Est.", "Imposto", "Preço Final", "Classif.")
        self.tree = ttk.Treeview(frame_viz, columns=columns, show="headings", height=15)
       
        # Configurar colunas
        column_widths = [60, 80, 60, 60, 80, 80, 90, 80]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER)
       
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_viz, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
       
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
       
        # Configurar cores por classificação
        self.tree.tag_configure("Barato", background="#d4edda")
        self.tree.tag_configure("Normal", background="#fff3cd")
        self.tree.tag_configure("Caro", background="#f8d7da")
   
    def criar_frame_estatisticas(self, parent):
        """Cria o frame de estatísticas"""
        frame_stats = ttk.LabelFrame(parent, text="Estatísticas", padding="10")
        frame_stats.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
       
        # Organizar em duas colunas
        # Coluna 1
        ttk.Label(frame_stats, text="Média valores adicionais:").grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_media_adicionais, font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=tk.W, padx=(0, 40))
       
        ttk.Label(frame_stats, text="Maior preço final:").grid(row=1, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_maior_preco, font=("Arial", 10, "bold")).grid(row=1, column=1, sticky=tk.W, padx=(0, 40))
       
        ttk.Label(frame_stats, text="Menor preço final:").grid(row=2, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_menor_preco, font=("Arial", 10, "bold")).grid(row=2, column=1, sticky=tk.W, padx=(0, 40))
       
        # Coluna 2
        ttk.Label(frame_stats, text="Total de impostos:").grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_total_impostos, font=("Arial", 10, "bold")).grid(row=0, column=3, sticky=tk.W, padx=(0, 40))
       
        ttk.Label(frame_stats, text="Produtos baratos:").grid(row=1, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_count_barato, font=("Arial", 10, "bold")).grid(row=1, column=3, sticky=tk.W, padx=(0, 40))
       
        ttk.Label(frame_stats, text="Produtos normais:").grid(row=2, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_count_normal, font=("Arial", 10, "bold")).grid(row=2, column=3, sticky=tk.W, padx=(0, 40))
       
        # Coluna 3
        ttk.Label(frame_stats, text="Produtos caros:").grid(row=1, column=4, sticky=tk.W, padx=(0, 20))
        ttk.Label(frame_stats, textvariable=self.var_count_caro, font=("Arial", 10, "bold")).grid(row=1, column=5, sticky=tk.W)
   
    def criar_frame_controles(self, parent):
        """Cria o frame de controles"""
        frame_controles = ttk.Frame(parent)
        frame_controles.grid(row=3, column=0, columnspan=2, pady=(20, 0))
       
        ttk.Button(frame_controles, text="Limpar Tudo", command=self.limpar_dados).grid(row=0, column=0, padx=5)
        ttk.Button(frame_controles, text="Gerar Relatório", command=self.gerar_relatorio).grid(row=0, column=1, padx=5)
        ttk.Button(frame_controles, text="Sair", command=self.root.quit).grid(row=0, column=2, padx=5)
   
    def adicionar_produto(self):
        """Adiciona um novo produto à lista"""
        if len(self.produtos) >= self.max_produtos:
            messagebox.showwarning("Limite atingido", f"Máximo de {self.max_produtos} produtos permitido!")
            return
       
        # Validar entrada
        try:
            preco = float(self.var_preco.get().replace(",", "."))
            if preco <= 0:
                raise ValueError("Preço deve ser positivo")
        except ValueError:
            messagebox.showerror("Erro", "Digite um preço válido (número positivo)")
            return
       
        # Criar produto
        numero = len(self.produtos) + 1
        produto = Produto(numero, preco, self.var_refrigeracao.get(), self.var_categoria.get())
        self.produtos.append(produto)
       
        # Adicionar à treeview
        self.tree.insert("", "end", values=(
            f"#{produto.numero}",
            f"R$ {produto.preco_unitario:.2f}",
            "Sim" if produto.refrigeracao else "Não",
            produto.categoria,
            f"R$ {produto.custo_estocagem:.2f}",
            f"R$ {produto.imposto:.2f}",
            f"R$ {produto.preco_final:.2f}",
            produto.classificacao
        ), tags=(produto.classificacao,))
       
        # Limpar campos
        self.var_preco.set("")
        self.var_refrigeracao.set(False)
        self.var_categoria.set("A")
       
        # Atualizar estatísticas
        self.atualizar_estatisticas()
       
        messagebox.showinfo("Sucesso", f"Produto #{numero} adicionado com sucesso!")
   
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas exibidas"""
        if not self.produtos:
            return
       
        # Contadores
        self.var_contador.set(f"{len(self.produtos)}/{self.max_produtos}")
       
        # Cálculos
        total_custo_estocagem = sum(p.custo_estocagem for p in self.produtos)
        total_impostos = sum(p.imposto for p in self.produtos)
        media_adicionais = (total_custo_estocagem + total_impostos) / len(self.produtos)
       
        precos_finais = [p.preco_final for p in self.produtos]
        maior_preco = max(precos_finais)
        menor_preco = min(precos_finais)
       
        # Contadores por classificação
        count_barato = sum(1 for p in self.produtos if p.classificacao == "Barato")
        count_normal = sum(1 for p in self.produtos if p.classificacao == "Normal")
        count_caro = sum(1 for p in self.produtos if p.classificacao == "Caro")
       
        # Atualizar variáveis
        self.var_media_adicionais.set(f"R$ {media_adicionais:.2f}")
        self.var_maior_preco.set(f"R$ {maior_preco:.2f}")
        self.var_menor_preco.set(f"R$ {menor_preco:.2f}")
        self.var_total_impostos.set(f"R$ {total_impostos:.2f}")
        self.var_count_barato.set(str(count_barato))
        self.var_count_normal.set(str(count_normal))
        self.var_count_caro.set(str(count_caro))
   
    def limpar_dados(self):
        """Limpa todos os dados"""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todos os dados?"):
            self.produtos.clear()
            self.tree.delete(*self.tree.get_children())
           
            # Resetar variáveis
            self.var_contador.set("0/12")
            self.var_media_adicionais.set("R$ 0,00")
            self.var_maior_preco.set("R$ 0,00")
            self.var_menor_preco.set("R$ 0,00")
            self.var_total_impostos.set("R$ 0,00")
            self.var_count_barato.set("0")
            self.var_count_normal.set("0")
            self.var_count_caro.set("0")
           
            messagebox.showinfo("Sucesso", "Dados limpos com sucesso!")
   
    def gerar_relatorio(self):
        """Gera um relatório detalhado em nova janela"""
        if not self.produtos:
            messagebox.showwarning("Aviso", "Nenhum produto cadastrado para gerar relatório!")
            return
       
        # Criar nova janela
        janela_relatorio = tk.Toplevel(self.root)
        janela_relatorio.title("Relatório Detalhado")
        janela_relatorio.geometry("600x500")
       
        # Texto do relatório
        frame_texto = ttk.Frame(janela_relatorio, padding="10")
        frame_texto.pack(fill=tk.BOTH, expand=True)
       
        text_widget = tk.Text(frame_texto, wrap=tk.WORD, font=("Courier", 10))
        scrollbar_relatorio = ttk.Scrollbar(frame_texto, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_relatorio.set)
       
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_relatorio.pack(side=tk.RIGHT, fill=tk.Y)
       
        # Gerar conteúdo do relatório
        relatorio = self._gerar_conteudo_relatorio()
        text_widget.insert(tk.END, relatorio)
        text_widget.configure(state=tk.DISABLED)
       
        # Botão para fechar
        ttk.Button(janela_relatorio, text="Fechar",
                  command=janela_relatorio.destroy).pack(pady=10)
   
    def _gerar_conteudo_relatorio(self) -> str:
        """Gera o conteúdo textual do relatório"""
        relatorio = "=" * 60 + "\n"
        relatorio += "           RELATÓRIO DE ANÁLISE DE PRODUTOS\n"
        relatorio += "=" * 60 + "\n\n"
       
        # Produtos individuais
        relatorio += "PRODUTOS CADASTRADOS:\n"
        relatorio += "-" * 60 + "\n"
       
        for produto in self.produtos:
            relatorio += f"Produto #{produto.numero}:\n"
            relatorio += f"  Preço Unitário: R$ {produto.preco_unitario:.2f}\n"
            relatorio += f"  Refrigeração: {'Sim' if produto.refrigeracao else 'Não'}\n"
            relatorio += f"  Categoria: {produto.categoria}\n"
            relatorio += f"  Custo de Estocagem: R$ {produto.custo_estocagem:.2f}\n"
            relatorio += f"  Imposto: R$ {produto.imposto:.2f}\n"
            relatorio += f"  Preço Final: R$ {produto.preco_final:.2f}\n"
            relatorio += f"  Classificação: {produto.classificacao}\n"
            relatorio += "-" * 40 + "\n"
       
        # Estatísticas
        relatorio += "\nESTATÍSTICAS GERAIS:\n"
        relatorio += "-" * 60 + "\n"
        relatorio += f"Total de produtos: {len(self.produtos)}\n"
        relatorio += f"Média dos valores adicionais: {self.var_media_adicionais.get()}\n"
        relatorio += f"Maior preço final: {self.var_maior_preco.get()}\n"
        relatorio += f"Menor preço final: {self.var_menor_preco.get()}\n"
        relatorio += f"Total de impostos: {self.var_total_impostos.get()}\n\n"
       
        relatorio += "DISTRIBUIÇÃO POR CLASSIFICAÇÃO:\n"
        relatorio += f"  Produtos Baratos: {self.var_count_barato.get()}\n"
        relatorio += f"  Produtos Normais: {self.var_count_normal.get()}\n"
        relatorio += f"  Produtos Caros: {self.var_count_caro.get()}\n"
       
        relatorio += "\n" + "=" * 60 + "\n"
        relatorio += "Relatório gerado pelo Sistema de Análise de Produtos\n"
        relatorio += "=" * 60
       
        return relatorio
   
    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()


def main():
    """Função principal"""
    app = SistemaAnaliseProdutos()
    app.executar()


if __name__ == "__main__":
    main()
