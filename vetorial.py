from collections import defaultdict
import copy
import math
import xml.etree.ElementTree as ET


def read_tf_idf_xml(path: str) -> dict:
    words = dict()
    tree = ET.parse(path)
    root = tree.getroot()

    palavras = root.findall("palavra")

    for palavra in palavras:
        documentos = palavra.findall("documento")
        file = dict()
        for documento in documentos:
            quantia = documento.find("tf-idf")
            if quantia is not None:
                file[documento.attrib["value"]] = quantia.attrib["value"]

        words[palavra.attrib["value"]] = file
    return words


def save_tf_idf_xml(index: dict, path: str):
    root = ET.Element("TF-IDF")
    for palavra in index:
        word = ET.SubElement(root, "palavra", value=palavra)
        for doc in index[palavra]:
            documento = ET.SubElement(word, "documento", value=doc)
            ET.SubElement(documento, "tf-idf", value=str(index[palavra][doc]))

    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def normalizacao_tf_idf_docs(dicionario: dict) -> dict:
    norm = defaultdict(float)
    for palavra in dicionario:
        for doc in dicionario[palavra]:
            norm[doc] += math.pow(dicionario[palavra][doc], 2)

    for doc in norm:
        norm[doc] = math.sqrt(norm[doc])

    return norm


def normalizacao_tf_idf_query(dicionario: dict) -> float:
    norm = 0
    for palavra in dicionario:
        norm += math.pow(dicionario[palavra], 2)

    return math.sqrt(norm)


def calc_idf(tot_docs: int, freq_palavra_doc: int):
    return math.log((tot_docs / freq_palavra_doc), 2)


def calc_tf_idf(tot_docs: int, freq_palavra_doc: int, freq_palavra: int) -> float:
    if freq_palavra > 0:
        result = (1 + math.log(freq_palavra, 2)) * (
            calc_idf(tot_docs, freq_palavra_doc)
        )
    else:
        result = 0
    return result


def tf_idf_docs(words: dict, aparece: dict):
    """
    Retorna um dict com o TF-IDF calculado de todos os documentos de acordo com cada palavra
            um dict com o IDF calculado por palavra
    """
    tf_idf = copy.deepcopy(words)
    idf = dict()
    # pega a lista de documentos da 1° palavra e verifica o tamanho total para definir a quantia de documentos
    tot_docs = len(list(words[next(iter(words))]))

    for word in words:
        for arquivo in words[word]:
            tf_idf[word][arquivo] = calc_tf_idf(
                tot_docs, aparece[word], int(words[word][arquivo])
            )
            if word not in idf.keys():
                idf[word] = calc_idf(tot_docs, aparece[word])

    return tf_idf, idf


def tf_idf_query(words: dict, aparece: dict, query: str) -> dict:
    """
    Retorna um dict com o TF-IDF calculado de todas as palavras da query, levando em conta palavras que ocorrem mais de uma vez
    """
    tf_idf = dict()
    quantia_palavras = defaultdict(int)
    # pega a lista de documentos da 1° palavra e verifica o tamanho total para definir a quantia de documentos
    tot_docs = len(list(words[next(iter(words))]))

    # logica booleana não se aplica ao modelo vetorial
    for palavra in query.split():
        quantia_palavras[palavra] += 1
    for palavra in query.split():
        tf_idf[palavra] = calc_tf_idf(
            tot_docs, aparece[palavra], quantia_palavras[palavra]
        )

    return tf_idf


def similaridade_query(
    tf_idf_query: dict, tf_idf_docs: dict, query_list: list, idf: dict
) -> dict:
    normalizacao_docs = normalizacao_tf_idf_docs(tf_idf_docs)
    normalizacao_query = normalizacao_tf_idf_query(tf_idf_query)
    sim_docs = defaultdict(float)

    for doc in normalizacao_docs:
        div = normalizacao_docs[doc] * normalizacao_query
        if div > 0:
            for palavra in query_list:
                sim_docs[doc] += tf_idf_query[palavra] * idf[palavra]

            sim_docs[doc] = sim_docs[doc] / div
        else:
            sim_docs[doc] = 0

    return sim_docs


def apply_query(words_index: dict, doc_words: dict, query: str) -> dict:
    tf_idf, idf = tf_idf_docs(words_index, doc_words)
    tf_idf_q = tf_idf_query(words_index, doc_words, query)
    query_list = query.split()

    return similaridade_query(tf_idf_q, tf_idf, query_list, idf)
