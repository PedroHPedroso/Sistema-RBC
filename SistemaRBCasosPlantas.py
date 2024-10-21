import json
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Carregar a base de dados de casos
df_casos = pd.read_excel('Base de dados de doença de planta CASOS.xlsx', sheet_name='plantas IA(Planilha1)')

# Criar listas de opções com base nas colunas do DataFrame
opcoes_doenca = ['cancro do caule diaporthe', 'podridão de carvão', 'podridão da raiz da rizoctonia', 'podridão de fitóftora', 'podridão parda', 'oídio', 'míldio', 'mancha marrom', 'praga bacteriana', 'pústula bacteriana', 'mancha de semente roxa', 'antracnose', 'mancha-folha-phyllosticta', 'mancha de folha alternaria', 'mancha-olho-de-rã', 'diaporthe-pod-&-stem-blight', 'nematóide de cisto', 'Lesão 2-4-d', 'lesão por herbicida']
opcoes_area_danificada = ['áreas baixas', 'espalhado', 'campo inteiro', 'áreas superiores', 'Desconhecido']
opcoes_lesao = ['Marrom', 'ADN', 'bronzeado', 'dk-marrom-preto', 'Desconhecido']
opcoes_hist_colheita = ['mesmo primeiro ano', 'mesmo-último-dois anos', 'mesmo-lst-sev-anos', 'dif-1º ano', 'Desconhecido']
opcoes_gravidade = ['pode-severo', 'forte', 'Menor']
opcoes_murchando = ['Ausente', 'Presente']
opcoes_tronco = ['Anormal', 'Norma']
opcoes_cancro = ['Acima do segundo', 'Ausente', 'abaixo do solo', 'Acima do solo']
opcoes_temperatura = ['norma', 'norma gt', 'lt-norma']

# Transformar a base de dados em JSON para simular o arquivo de casos anteriores
casos_json = df_casos.to_dict(orient='records')

# Função para salvar os casos no formato JSON
def salvar_casos_json(casos, caminho='casos_novos.json'):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(casos, f, ensure_ascii=False, indent=4)

# Função para calcular similaridade entre casos
def calcular_similaridade(novo_caso, caso_anterior):
    total_caracteristicas = len(novo_caso)
    correspondencias = sum(1 for key in novo_caso if novo_caso[key] == caso_anterior.get(key, None))
    return (correspondencias / total_caracteristicas) * 100 if total_caracteristicas > 0 else 0

# Função para recuperar casos com base na similaridade
def recuperar_casos(novo_caso, porcentagem_similaridade):
    casos_relevantes = []
    for caso in casos_json:
        similaridade = calcular_similaridade(novo_caso, caso)
        if similaridade >= porcentagem_similaridade:
            casos_relevantes.append((caso, similaridade))
    return casos_relevantes

# Função para adicionar novo caso
def adicionar_caso():
    novo_caso = {
        "DescDoenca": combo_doenca.get(),
        "área danificada": combo_area_danificada.get(),
        "lesão cancerígena": combo_lesao.get(),
        "histórico de colheita": combo_hist_colheita.get(),
        "gravidade": combo_gravidade.get(),
        "murchando": combo_murchando.get(),
        "tronco": combo_tronco.get(),
        "cancro do caule": combo_cancro.get(),
        "temperatura": combo_temperatura.get()
    }
    casos_json.append(novo_caso)
    salvar_casos_json(casos_json)
    messagebox.showinfo("Informação", "Novo caso adicionado com sucesso!")

# Função para procurar casos semelhantes
def procurar_casos():
    novo_caso = {
        "DescDoenca": combo_doenca.get(),
        "área danificada": combo_area_danificada.get(),
        "lesão cancerígena": combo_lesao.get(),
        "histórico de colheita": combo_hist_colheita.get(),
        "gravidade": combo_gravidade.get(),
        "murchando": combo_murchando.get(),
        "tronco": combo_tronco.get(),
        "cancro do caule": combo_cancro.get(),
        "temperatura": combo_temperatura.get()
    }
    porcentagem_similaridade = int(entry_similaridade.get())
    casos_encontrados = recuperar_casos(novo_caso, porcentagem_similaridade)
    
    if casos_encontrados:
        resultados = "\n".join([f"Similaridade: {sim:.2f}% - Doença: {caso.get('DescDoenca', 'Chave DescDoenca Ausente')}" for caso, sim in casos_encontrados])
        messagebox.showinfo("Casos encontrados", resultados)
    else:
        messagebox.showinfo("Nenhum caso encontrado", "Nenhum caso similar foi encontrado.")

# Interface gráfica (Tkinter)
root = tk.Tk()
root.title("Sistema RBC - Doenças de Plantas")

# Campos de entrada para um novo caso com Combobox para opções
tk.Label(root, text="DescDoenca").grid(row=0, column=0)
combo_doenca = ttk.Combobox(root, values=opcoes_doenca)
combo_doenca.grid(row=0, column=1)

tk.Label(root, text="Área Danificada").grid(row=1, column=0)
combo_area_danificada = ttk.Combobox(root, values=opcoes_area_danificada)
combo_area_danificada.grid(row=1, column=1)

tk.Label(root, text="Lesão Cancerígena").grid(row=2, column=0)
combo_lesao = ttk.Combobox(root, values=opcoes_lesao)
combo_lesao.grid(row=2, column=1)

tk.Label(root, text="Histórico de Colheita").grid(row=3, column=0)
combo_hist_colheita = ttk.Combobox(root, values=opcoes_hist_colheita)
combo_hist_colheita.grid(row=3, column=1)

tk.Label(root, text="Gravidade").grid(row=4, column=0)
combo_gravidade = ttk.Combobox(root, values=opcoes_gravidade)
combo_gravidade.grid(row=4, column=1)

tk.Label(root, text="Murchando").grid(row=5, column=0)
combo_murchando = ttk.Combobox(root, values=opcoes_murchando)
combo_murchando.grid(row=5, column=1)

tk.Label(root, text="Tronco").grid(row=6, column=0)
combo_tronco = ttk.Combobox(root, values=opcoes_tronco)
combo_tronco.grid(row=6, column=1)

tk.Label(root, text="Cancro do Caule").grid(row=7, column=0)
combo_cancro = ttk.Combobox(root, values=opcoes_cancro)
combo_cancro.grid(row=7, column=1)

tk.Label(root, text="Temperatura").grid(row=8, column=0)
combo_temperatura = ttk.Combobox(root, values=opcoes_temperatura)
combo_temperatura.grid(row=8, column=1)

# Campo para porcentagem de similaridade
tk.Label(root, text="Porcentagem de Similaridade").grid(row=9, column=0)
entry_similaridade = tk.Entry(root)
entry_similaridade.grid(row=9, column=1)

# Botões de adicionar caso e procurar caso
btn_adicionar = tk.Button(root, text="Adicionar Novo Caso", command=adicionar_caso)
btn_adicionar.grid(row=10, column=0)

btn_procurar = tk.Button(root, text="Procurar Casos Similares", command=procurar_casos)
btn_procurar.grid(row=10, column=1)

# Executar a interface
root.mainloop()