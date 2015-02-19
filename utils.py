from string import ascii_lowercase, digits, punctuation

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])

def tag_numbers(line):
    words = line.split()
    result = []
    for word in words:
        if word.isdigit():
            result.append("NUMBER")
        else:
            result.append(word)
    return ' '.join(word for word in result)

def separate_punt_marks(st):
    exclude = set(punctuation)
    st = ''.join(ch for ch in st if ch not in exclude)
    return st