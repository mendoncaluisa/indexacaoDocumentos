
import re
import os
import copy
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter

from numpy.ma.core import append


# cria a arvore xml como: palavras -> documentos -> quantia da palavra
def saveIndexacaoXML(index: dict, path: str):
    root = ET.Element("indexTerms")
    for palavra in index:
        word = ET.SubElement(root, "palavra", value=palavra)
        for doc in index[palavra]:
            documento = ET.SubElement(word, "documento", value=doc)
            ET.SubElement(documento, "quantia", value=str(index[palavra][doc]))

    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def readIndexacaoXML(path: str) -> dict:
    words = dict()
    tree = ET.parse(path)
    root = tree.getroot()

    palavras = root.findall("palavra")

    for palavra in palavras:
        documentos = palavra.findall("documento")
        file = dict()
        for documento in documentos:
            quantia = documento.find("quantia")
            if quantia is not None:
                file[documento.attrib["value"]] = quantia.attrib["value"]

        words[palavra.attrib["value"]] = file
    return words


def indexacao():

    dir_path = "./documentos"
    words = defaultdict(lambda: defaultdict(int))
    total_words = Counter()  # Usando Counter para contagem total

    # Filtra apenas arquivos (ignora diretórios)
    arquivos = [f for f in os.listdir(dir_path)
                if os.path.isfile(os.path.join(dir_path, f))]

    for nome_arquivo in arquivos:
        try:
            with open(os.path.join(dir_path, nome_arquivo), "r", encoding="utf-8") as f:
                conteudo = f.read()
                # Extrai palavras usando regex mais eficiente
                palavras = re.findall(r"\b[a-z0-9_]{3,}\b", conteudo.lower())

                for palavra in palavras:
                    # Filtra palavras não desejadas
                    if not any(caractere in palavra for caractere in ("-", "_")) \
                            and palavra != "não" and len(palavra) > 2:
                        words[palavra][nome_arquivo] += 1
                        total_words[palavra] += 1  # Incrementa contador total

        except (IOError, UnicodeDecodeError) as e:
            print(f"Erro ao processar {nome_arquivo}: {str(e)}")


    # save = open("index.txt", "w")
    # save.write("{}".format(words))
    # save.close()
    # escreve num documento .xml
    saveIndexacaoXML(words_filtered, "indexacao.xml")
    readIndexacaoXML("indexacao.xml")
    return words_filtered

def imprime_vocabulario(words: dict) :
    print(words)

def imprime_matriz_ocorrências(words: dict) :
    for palavra, documentos in words.items():
        print(f"\nPalavra: {palavra}")
        for doc, count in documentos.items():
            print(f"  - {doc}: {count} ocorrências")


if __name__ == "__main__":

    opcao = 1
    words_filtered = defaultdict(lambda: defaultdict(int))

    while opcao != "0":

        print("***************************************************************")
        print("***** TRABALHO DE RECUPERAÇÃO DE INFORMAÇÃO     ***************")
        print("***************************************************************")
        print("***** ALUNOS: IVAN MARCELINO OLIVEIRA           ***************")
        print("*****         MARIA LUÍSA MENDONÇA OLIVEIRA     ***************")
        print("***************************************************************")
        print("************************ MENU *********************************")
        print("***** 1 - PARA INDEXAR A COLEÇÃO                ***************")
        print("***** 2 - PARA IMPRIMIR O VOCABULÁRIO           ***************")
        print("***** 3 - PARA IMPRIMIR A MATRIZ DE OCORRÊNCIAS ***************")
        print("***** 4 - PARA IMPRIMIR A MATRIZ DE FREQUÊNCIAS ***************")
        print("***** 0 - PARA SAIR                             ***************")
        print("***************************************************************")
        opcao = input("\nDIGITE A OPÇÃO DESEJADA: ")

        if opcao == "1":
            words_filtered = indexacao()

        elif opcao == "2":
            imprime_vocabulario(words_filtered)

        elif opcao == "0":
            break


