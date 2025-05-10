import re
import os
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
from lark import Lark, Transformer


# cria a arvore xml como: palavras -> documentos -> quantia da palavra
def saveIndexacaoXML(index: dict, path: str):
    root = ET.Element("indexTerms")
    for palavra in index:
        word = ET.SubElement(root, "palavra", value=palavra)
        for doc in index[palavra]:
            documento = ET.SubElement(word, "documento", value=doc)
            ET.SubElement(documento, "frequencia", value=str(index[palavra][doc]))

    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def saveIndexacaoBoolXML(index: dict, path: str):
    root = ET.Element("indexTerms")
    for palavra in index:
        word = ET.SubElement(root, "palavra", value=palavra)
        for doc in index[palavra]:
            documento = ET.SubElement(word, "documento", value=doc)
            ET.SubElement(
                documento, "ocorrencia", value=str(1 if index[palavra][doc] else 0)
            )

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
            quantia = documento.find("frequencia")
            if quantia is not None:
                file[documento.attrib["value"]] = quantia.attrib["value"]

        words[palavra.attrib["value"]] = file
    return words


def indexacao(value_filter: int):

    dir_path = "./documentos"
    words = defaultdict(lambda: defaultdict(int))
    total_words = Counter()  # Usando Counter para contagem total

    # Filtra apenas arquivos (ignora diretórios)
    arquivos = [
        f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
    ]

    for nome_arquivo in arquivos:
        try:
            with open(os.path.join(dir_path, nome_arquivo), "r", encoding="utf-8") as f:
                conteudo = f.read()
                # Extrai palavras usando regex mais eficiente
                palavras = re.findall(r"\b[a-z0-9_]{3,}\b", conteudo.lower())

                for palavra in palavras:
                    # Filtra palavras não desejadas
                    if (
                        not any(caractere in palavra for caractere in ("-", "_"))
                        and palavra != "não"
                        and len(palavra) > 2
                    ):
                        words[palavra][nome_arquivo] += 1
                        total_words[palavra] += 1  # Incrementa contador total

        except (IOError, UnicodeDecodeError) as e:
            print(f"Erro ao processar {nome_arquivo}: {str(e)}")

    # filtra os 50 mais frequentes palavras do dicionario:
    words = dict(
        sorted(words.items(), key=lambda item: sum(item[1].values()), reverse=True)[
            :value_filter
        ]
    )

    # seta como 0 o index da palavra que não está presente naquele documento
    for palavra in words:
        for arquivo in arquivos:
            if arquivo not in words[palavra]:
                words[palavra][arquivo] = 0

    saveIndexacaoXML(words, "indexacao_freq.xml")
    saveIndexacaoBoolXML(words, "indexacao_ocorrencia.xml")

    return words


def imprime_vocabulario(words: dict):
    palavras = words.keys()
    count = 1
    for palavra in palavras:
        print("{} - {}".format(count, palavra), end="")
        if count % 10 == 0:
            print()
        else:
            print(" | ", end="")

        count += 1
    print()


def imprime_matriz_ocorrencia(words: dict):
    for palavra, documentos in words.items():
        print(f"\nPalavra: {palavra}")
        for doc, count in documentos.items():
            if count > 0:
                print(f"  - {doc}: 1 ")
            else:
                print(f"  - {doc}: 0 ")


def imprime_matriz_frequencia(words: dict):
    for palavra, documentos in words.items():
        print(f"\nPalavra: {palavra}")
        for doc, count in documentos.items():
            print(f"  - {doc}: {count} ocorrências")


def contar_operadores(expressao):
    operadores = [" and ", " or "]
    total = 0
    for op in operadores:
        total += expressao.lower().count(op)
    return total


class BooleanSearch(Transformer):
    def __init__(self, index, all_docs):
        self.index = index
        self.all_docs = all_docs

    def term(self, args):
        word = args[0].value.lower()
        return self.index.get(word, set())

    def and_(self, args):
        return args[0] & args[1]

    def or_(self, args):
        return args[0] | args[1]

    def not_(self, args):
        return self.all_docs - args[0]


def busca_logica(index: dict, query: str):
    # definindo a gramatica a ser usada
    grammar = """
    ?start: expr
    ?expr: expr "OR" term     -> or_
        | term
    ?term: term "AND" factor  -> and_
        | factor
    ?factor: "NOT" factor     -> not_
        | "(" expr ")"
        | WORD             -> term

    %import common.WORD
    %ignore " "
    """

    # diicionario que vincula as palavras aos documentos somente
    presence = {
        # pega as palavras chave do dicionario
        term: set(doc_freq.keys())
        for term, doc_freq in index.items()
    }

    # itera por todos os valores do dicionario tentando adicionar o arquivo ao set de arquivos
    all_docs = set()
    for doc_freq in index.values():
        all_docs.update(doc_freq)

    parser = Lark(grammar, parser="lalr", transformer=BooleanSearch(presence, all_docs))
    return parser.parse(query)


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
        print("***** 5 - PARA IMPORTAR A MATRIZ DE FREQUÊNCIAS ***************")
        print("***** 6 - PARA REALIZAR BUSCA DE DOCUMENTOS     ***************")
        print("***** 0 - PARA SAIR                             ***************")
        print("***************************************************************")
        opcao = input("\nDIGITE A OPÇÃO DESEJADA: ")

        if opcao == "1":
            words_filtered = indexacao(50)

        elif opcao == "2":
            if words_filtered:
                imprime_vocabulario(words_filtered)
            else:
                print(
                    "* Arquivos ainda não foram indexados!                            *"
                )

        elif opcao == "3":
            if words_filtered:
                imprime_matriz_ocorrencia(words_filtered)
            else:
                print(
                    "* Arquivos ainda não foram indexados!                            *"
                )

        elif opcao == "4":
            if words_filtered:
                imprime_matriz_frequencia(words_filtered)
            else:
                print(
                    "* Arquivos ainda não foram indexados!                            *"
                )

        elif opcao == "5":
            words_filtered = readIndexacaoXML("indexacao_freq.xml")

        elif opcao == "6":
            if words_filtered:
                print("\n" + "*" * 70)
                print(
                    "* CAMPO DE CONSULTA                                              *"
                )
                print("*" * 70)
                print(
                    "* Você pode realizar consultas utilizando termos e operadores    *"
                )
                print(
                    "* booleanos. Os operadores permitidos são:                       *"
                )
                print(
                    "*                                                                *"
                )
                print(
                    "*   - AND: para buscar documentos que contenham ambos os termos  *"
                )
                print(
                    "*   - OR : para buscar documentos que contenham pelo menos um    *"
                )
                print(
                    "*          dos termos                                            *"
                )
                print(
                    "*   - NOT: para buscar documentos que não contenham o termo      *"
                )
                print(
                    "*          posterior a ele                                       *"
                )
                print(
                    "*                                                                *"
                )
                print(
                    "* Exemplo de consultas válidas:                                  *"
                )
                print(
                    "*   gato AND cachorro                                            *"
                )
                print(
                    "*   carro OR moto                                                *"
                )
                print(
                    "*   livro AND autor OR editora                                   *"
                )
                print(
                    "*   NOT planta AND NOT animal                                    *"
                )
                print(
                    "*                                                                *"
                )
                print(
                    "* ATENÇÃO: Só é permitida a combinação de no máximo dois         *"
                )
                print(
                    "* operadores booleanos por consulta.                             *"
                )
                print("*" * 70)

                expressao = input("\nDIGITE A EXPRESSÃO: ")

                # Verifica se há no máximo 2 operadores 'and'/'or'
                if contar_operadores(expressao) > 2:
                    print(
                        "\nErro: A expressão deve conter no máximo **dois operadores booleanos** (and/or)."
                    )

                # realiza a busca busca_logica
                result = busca_logica(words_filtered, expressao)
                if result:
                    print(f"{expressao} -> {result}")
                else:
                    print(f"{expressao} -> Nenhum documento que satisfaça a busca!")
            else:
                print(
                    "* Arquivos ainda não foram indexados!                            *"
                )

        elif opcao == "0":
            break
