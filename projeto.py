# esrutura de dicionario para indexação ex: palavra{doc1, frequencia}, {doc2, frequencia}

# passar por todos os documentos

# ler documento palavra a palavra

# excluir palavras proibidas na indexação ex: não, separadas por hifen, tamanho menor que 2

# contabilizando numero de repetição de cada palavra
import re
import os
import xml.etree.ElementTree as ET


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
    dir = "./documentos"
    words = dict()

    # itera por todos nomes de arquivos na pasta
    for nome_arquivo in os.listdir(dir):
        path = os.path.join(dir, nome_arquivo)
        # abre arquivos 1 a 1
        with open(path, "r", encoding="utf-8") as f:
            conteudo = f.read()
            for linha in conteudo.splitlines():
                if linha != "\n":
                    # divide usando a regex (a-z A-Z 0-9 _)
                    linha = re.split(r"\W+", linha)
                    for palavra in linha:
                        palavra = palavra.lower()
                        if (
                            ("-" or "_" not in palavra)
                            and (len(palavra) > 2)
                            and (palavra != "não")
                        ):
                            if palavra not in words.keys():
                                # cria add palavra como chave do dict e um subdicionario como resultado, onde este tem nome do arquivo: frequencia
                                words[palavra] = {nome_arquivo: 1}
                            else:
                                # add 1 na frequencia daquela palavra naquele arquivo
                                words[palavra][nome_arquivo] += 1

    # save = open("index.txt", "w")
    # save.write("{}".format(words))
    # save.close()
    # escreve num documento .xml
    saveIndexacaoXML(words, "indexacao.xml")
    readIndexacaoXML("indexacao.xml")


if __name__ == "__main__":
    indexacao()
