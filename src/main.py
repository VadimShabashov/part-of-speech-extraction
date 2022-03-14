from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)


def load_document(path):
    with open(path, 'r') as file:
        data = file.read()

    return data


def extract_sequences(data, morph_sequence):
    # Проверка на пустой список или пустые данные
    if (not morph_sequence) or (not data):
        return []

    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)

    doc = Doc(data)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    words_tags = [(word.text, word.pos) for word in doc.tokens]
    sequences = []

    # Не совсем понятно по условию, что надо выводить, например, в случае NOUN NOUN и передачи "дом дерево кот".
    # Решил остановиться на [["дом", "дерево"], ["дерево", "кот"]], то есть возвращаться обратно по строке.
    ind_word_tag = 0
    ind_morph_seq = 0
    seq_start = 0
    while ind_word_tag < len(words_tags):
        word, tag = words_tags[ind_word_tag]
        if tag == morph_sequence[ind_morph_seq]:
            ind_morph_seq += 1
        else:
            if tag == morph_sequence[0]:
                ind_morph_seq = 1
            else:
                ind_morph_seq = 0

        # Начинаем новую последовательность
        if ind_morph_seq == 1:
            seq_start = ind_word_tag

        # Проверка на окончание последовательности
        if ind_morph_seq == len(morph_sequence):
            sequences.append([word for word, _ in words_tags[seq_start:ind_word_tag + 1]])
            ind_word_tag = seq_start + 1
            ind_morph_seq = 0
        else:
            ind_word_tag += 1

    return sequences


def show_sequence(morph_sequence):
    for line in morph_sequence:
        print(" ".join(line))


def main():
    path = "./texts/example.txt"
    morph_sequence = ["ADJ", "NOUN", "PUNCT"]

    try:
        data = load_document(path)
    except FileNotFoundError:
        print("File not found")
        return

    sequences = extract_sequences(data, morph_sequence)
    show_sequence(sequences)
    return


if __name__ == "__main__":
    main()
