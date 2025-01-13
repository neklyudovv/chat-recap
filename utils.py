def pr_word_stats(word_stats):
    s = '\n'
    for i, word in enumerate(word_stats):
        if i<10:
            s += f'{word} {word_stats[word]}\n'
    return s
