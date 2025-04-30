# esrutura de dicionario para indexação ex: palavra{doc1, frequencia}, {doc2, frequencia}

# passar por todos os documentos

# ler documento palavra a palavra

# excluir palavras proibidas na indexação ex: não, separadas por hifen, tamanho menor que 2

# contabilizando numero de repetição de cada palavra
import sys
import re
import os

def indexacao():
    dir = "pasta"
    words = dict()

    for nome_arquivo in os.listdir(dir):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read() 
            for linha in conteudo:
                if linha != "\n":
                    linha = re.split(r"\W+", linha)
                    for palavra in linha :
                        palavra.lower()
                        if palavra not in words.key():
                            words = {palavra: dict()}
                            aux = {palavra}
                            aux = {nome_arquivo: 1}
                        else:
                            aux = words[palavra]
                            aux[nome_arquivo] = (aux[nome_arquivo] + 1)

    
    
