# esrutura de dicionario para indexação ex: palavra{doc1, frequencia}, {doc2, frequencia}

# passar por todos os documentos

# ler documento palavra a palavra

# excluir palavras proibidas na indexação ex: não, separadas por hifen, tamanho menor que 2

# contabilizando numero de repetição de cada palavra
import re
import os


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
                    # linha = re.split(r"\W+", linha)
                    linha = linha.split(" ")
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

    save = open("index.txt", "w")
    save.write("{}".format(words))
    save.close()


if __name__ == "__main__":
    indexacao()
