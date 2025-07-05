def calcula_avaliacao(dict_doc_query, dict_doc_relevantes):
    qnt_relevantes = 0
    iterate = 0
    tot_relevantes = len(list(dict_doc_relevantes))

    for doc in dict_doc_query:
        iterate += 1
        if doc in dict_doc_relevantes:
            qnt_relevantes += 1

        if iterate == 5:
            print(f"P@5 = {(qnt_relevantes/tot_relevantes) * 100:.0f}%")

        if iterate == 10:
            print(f"P@10 = {(qnt_relevantes/tot_relevantes) * 100:.0f}%")
            break
