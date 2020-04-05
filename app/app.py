import re


def start(vocabulary, size, smoothing, training_file, testing_file):
    probability = generate_ngrams(size, vocabulary, training_file, smoothing)


def get_count(size, vocabulary, message, count, total_count):
    if size == 1:
        if vocabulary == 0:
            for letter in message:
                lower_letter = letter.lower()
                if re.match("[a-z]", lower_letter):
                    count[lower_letter] = count.get(lower_letter, 0) + 1
                    total_count = total_count + 1
        elif vocabulary == 1:
            for letter in message:
                if re.match("[a-zA-Z]", letter):
                    count[letter] = count.get(letter, 0) + 1
                    total_count = total_count + 1
        elif vocabulary == 2:
            for letter in message:
                if letter.isalpha():
                    count[letter] = count.get(letter, 0) + 1
                    total_count = total_count + 1
    elif size == 2:
        if vocabulary == 0:
            for bigram in message:
                lower_bigram = bigram.lower()
                if re.match("([a-z][a-z])", lower_bigram):
                    count[lower_bigram] = count.get(lower_bigram, 0) + 1
                    total_count = total_count + 1
        elif vocabulary == 1:
            for bigram in message:
                if re.match("([a-zA-Z][a-zA-Z])", bigram):
                    count[bigram] = count.get(bigram, 0) + 1
                    total_count = total_count + 1
        elif vocabulary == 2:
            for bigram in message:
                if bigram.isalpha():
                    count[bigram] = count.get(bigram, 0) + 1
                    total_count = total_count + 1
    elif size == 3:
        if vocabulary == 0:
            for trigram in message:
                lower_trigram = trigram.lower()
                if re.match("([a-z][a-z][a-z])", lower_trigram):
                    count[lower_trigram] = count.get(lower_trigram, 0) + 1
                    total_count = total_count + 1
        elif vocabulary == 1:
            for trigram in message:
                if re.match("([a-zA-Z][a-zA-Z][a-zA-Z])", trigram):
                    count[trigram] = count.get(trigram, 0) + 1
                    total_count = total_count + 1
        elif vocabulary == 2:
            for trigram in message:
                if trigram.isalpha():
                    count[trigram] = count.get(trigram, 0) + 1
                    total_count = total_count + 1

    return total_count


def generate_ngrams(size, vocabulary, file_name, smoothing):
    f = open(file_name, "r", encoding='utf-8')
    count_eu = dict()
    count_ca = dict()
    count_gl = dict()
    count_es = dict()
    count_en = dict()
    count_pt = dict()

    if vocabulary == 0:
        bins_size = 26 ** size
    elif vocabulary == 1:
        bins_size = 52 ** size
    elif vocabulary == 2:
        bins_size = 116766 ** size

    total_count_eu = 0
    total_count_ca = 0
    total_count_gl = 0
    total_count_es = 0
    total_count_en = 0
    total_count_pt = 0

    for x in f:
        info = x.split()
        id = info[0]
        name = info[1]
        language = info[2]
        message = " ".join(info[3:])

        if size == 2:
            message = [message[i:i + 2] for i in range(len(message) - 1)]
        elif size == 3:
            message = [message[i:i + 3] for i in range(len(message) - 2)]

        if language == "eu":
            total_count_eu = get_count(size, vocabulary, message, count_eu, total_count_eu)
        elif language == "ca":
            total_count_ca = get_count(size, vocabulary, message, count_ca, total_count_ca)
        elif language == "gl":
            total_count_gl = get_count(size, vocabulary, message, count_gl, total_count_gl)
        elif language == "es":
            total_count_es = get_count(size, vocabulary, message, count_es, total_count_es)
        elif language == "en":
            total_count_en = get_count(size, vocabulary, message, count_en, total_count_en)
        elif language == "pt":
            total_count_pt = get_count(size, vocabulary, message, count_pt, total_count_pt)

    probability_eu = get_probability(count_eu, total_count_eu, smoothing, bins_size)
    probability_ca = get_probability(count_ca, total_count_ca, smoothing, bins_size)
    probability_gl = get_probability(count_gl, total_count_gl, smoothing, bins_size)
    probability_es = get_probability(count_es, total_count_es, smoothing, bins_size)
    probability_en = get_probability(count_en, total_count_en, smoothing, bins_size)
    probability_pt = get_probability(count_pt, total_count_pt, smoothing, bins_size)

    f.close()

    return {"eu": probability_eu, "ca": probability_ca, "gl": probability_gl, "es": probability_es,
            "en": probability_en, "pt": probability_pt}


def get_probability(count, total_count, smoothing, bins_size):
    probability = dict()
    for key in count:
        probability[key] = (count[key] + smoothing) / (total_count + smoothing * bins_size)

    probability["<NOT-APPEAR>"] = (0 + smoothing) / (total_count + smoothing * bins_size)

    return probability

# ------------------ Start code here ------------------

start(0, 3, 0.3, "training-tweets.txt", "test-tweets-given.txt")
