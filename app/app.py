import re
import math


# start function for part 1
def start_existing_model(vocabulary, size, smoothing, training_file, testing_file):
    probability = generate_ngrams(size, vocabulary, training_file, smoothing, False)
    generate_ngram_output(vocabulary, size, smoothing, probability, testing_file, False)


# start function for part 2
def start_custom_model(training_file, testing_file):
    probability = generate_ngrams(3, 2, training_file, 0.5, True)
    generate_ngram_output(2, 3, 0.5, probability, testing_file, True)


# function to count number of ngrams and store them in dictionary
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


# calculate probability for each ngram and store in dictionary
def get_probability(count, total_count, smoothing, bins_size):
    probability = dict()

    for key in count:
        probability[key] = (count[key] + smoothing) / (total_count + smoothing * bins_size)

    probability["<NOT-APPEAR>"] = (0 + smoothing) / (total_count + smoothing * bins_size)

    return probability


# function to create ngrams
def generate_ngrams(size, vocabulary, file_name, smoothing, model_used):
    # regex used to filter for custom model
    re1 = '[@#$%^&*()=+\[\]{}/:|<>~]'
    re2 = 'xD|XD'

    re_filter = re.compile("(%s|%s)" % (re1, re2))

    f = open(file_name, "r", encoding='utf-8')
    count_eu = dict()
    count_ca = dict()
    count_gl = dict()
    count_es = dict()
    count_en = dict()
    count_pt = dict()

    total_count_eu = 0
    total_count_ca = 0
    total_count_gl = 0
    total_count_es = 0
    total_count_en = 0
    total_count_pt = 0

    # read info line by line
    for x in f:
        info = x.split()
        id = info[0]
        name = info[1]
        language = info[2]
        message = " ".join(info[3:])
        new_message_list = []
        new_message = ""

        # filter function for custom model
        if model_used:
            message = ""
            for word in info[3:]:
                if re_filter.search(word) == None:
                    message = word if message == "" else message + " " + word

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

    # calculate bin size
    if model_used:
        count_combine = {}
        count_combine.update(count_eu)
        count_combine.update(count_ca)
        count_combine.update(count_gl)
        count_combine.update(count_es)
        count_combine.update(count_en)
        count_combine.update(count_pt)
        bins_size = len(count_combine)
        print(bins_size)
    else:
        if vocabulary == 0:
            bins_size = 26 ** size
        elif vocabulary == 1:
            bins_size = 52 ** size
        elif vocabulary == 2:
            bins_size = 116766 ** size

    probability_eu = get_probability(count_eu, total_count_eu, smoothing, bins_size)
    probability_ca = get_probability(count_ca, total_count_ca, smoothing, bins_size)
    probability_gl = get_probability(count_gl, total_count_gl, smoothing, bins_size)
    probability_es = get_probability(count_es, total_count_es, smoothing, bins_size)
    probability_en = get_probability(count_en, total_count_en, smoothing, bins_size)
    probability_pt = get_probability(count_pt, total_count_pt, smoothing, bins_size)

    f.close()

    return {"eu": probability_eu, "ca": probability_ca, "gl": probability_gl, "es": probability_es,
            "en": probability_en, "pt": probability_pt}


# function to generate output
def generate_ngram_output(vocabulary, size, smoothing, probability, testing_file, model_used):
    # regex function
    re1 = '[@#$%^&*()=+\[\]{}/:|<>~]'
    re2 = 'xD|XD'

    re_filter = re.compile("(%s|%s)" % (re1, re2))

    input_file = open(testing_file, "r", encoding='utf-8')

    # output file names
    if model_used:
        trace_file_name = "trace_myModel.txt"
        eval_file_name = "eval_myModel.txt"
    else:
        trace_file_name = "trace_" + str(vocabulary) + "_" + str(size) + "_" + str(smoothing) + ".txt"
        eval_file_name = "eval_" + str(vocabulary) + "_" + str(size) + "_" + str(smoothing) + ".txt"

    output_file = open(trace_file_name, "w", encoding='utf-8')
    output_file2 = open(eval_file_name, "w", encoding='utf-8')

    count = dict()
    results = []

    # read input from test file line by line
    for x in input_file:
        info = x.split()
        id = info[0]
        name = info[1]
        language = info[2]
        message = " ".join(info[3:])

        if model_used:
            message = ""
            for word in info[3:]:
                if re_filter.search(word) == None:
                    message = word if message == "" else message + " " + word

        if size == 2:
            message = [message[i:i + 2] for i in range(len(message) - 1)]
        elif size == 3:
            message = [message[i:i + 3] for i in range(len(message) - 2)]

        score_eu = get_score(vocabulary, size, "eu", message, probability["eu"])

        score_ca = get_score(vocabulary, size, "ca", message, probability["ca"])

        score_gl = get_score(vocabulary, size, "gl", message, probability["gl"])

        score_es = get_score(vocabulary, size, "es", message, probability["es"])

        score_en = get_score(vocabulary, size, "en", message, probability["en"])

        score_pt = get_score(vocabulary, size, "pt", message, probability["pt"])

        scores = [score_eu, score_ca, score_gl, score_es, score_en, score_pt]

        max_score = max(scores, key=lambda y: y[0])

        label = "correct" if max_score[1] == language else "wrong"

        results.append((max_score[1], language, label))

        output_file.write(id + "  " + max_score[1] + "  " + str(max_score[0]) + "  " + language + "  " + label + "\n")

    metrics = generate_evaluation(results, count)
    output_file2.write(str(metrics[0]) + "\n" +
                       str(metrics[1]) + "  " + str(metrics[2]) + "  " + str(metrics[3]) + "  " + str(
        metrics[4]) + "  " + str(metrics[5]) + "  " + str(metrics[6]) + "\n" +
                       str(metrics[7]) + "  " + str(metrics[8]) + "  " + str(metrics[9]) + "  " + str(
        metrics[10]) + "  " + str(metrics[11]) + "  " + str(metrics[12]) + "\n" +
                       str(metrics[13]) + "  " + str(metrics[14]) + "  " + str(metrics[15]) + "  " + str(
        metrics[16]) + "  " + str(metrics[17]) + "  " + str(metrics[18]) + "\n" +
                       str(metrics[19]) + "  " + str(metrics[20]))

    input_file.close()
    output_file.close()
    output_file2.close()


# get score for message
def get_score(vocabulary, size, language, message, probability_table):
    score = 0

    if size == 1:
        if vocabulary == 0:
            for letter in message:
                lower_letter = letter.lower()
                if re.match("[a-z]", lower_letter):
                    score = score + math.log(probability_table.get(lower_letter, probability_table["<NOT-APPEAR>"]), 10)
        elif vocabulary == 1:
            for letter in message:
                if re.match("[a-zA-Z]", letter):
                    score = score + math.log(probability_table.get(letter, probability_table["<NOT-APPEAR>"]), 10)
        elif vocabulary == 2:
            for letter in message:
                if letter.isalpha():
                    score = score + math.log(probability_table.get(letter, probability_table["<NOT-APPEAR>"]), 10)
    elif size == 2:
        if vocabulary == 0:
            for bigram in message:
                lower_bigram = bigram.lower()
                if re.match("([a-z][a-z])", lower_bigram):
                    score = score + math.log(probability_table.get(lower_bigram, probability_table["<NOT-APPEAR>"]), 10)
        elif vocabulary == 1:
            for bigram in message:
                if re.match("([a-zA-Z][a-zA-Z])", bigram):
                    score = score + math.log(probability_table.get(bigram, probability_table["<NOT-APPEAR>"]), 10)
        elif vocabulary == 2:
            for bigram in message:
                if bigram.isalpha():
                    score = score + math.log(probability_table.get(bigram, probability_table["<NOT-APPEAR>"]), 10)
    elif size == 3:
        if vocabulary == 0:
            for trigram in message:
                lower_trigram = trigram.lower()
                if re.match("([a-z][a-z][a-z])", lower_trigram):
                    score = score + math.log(probability_table.get(lower_trigram, probability_table["<NOT-APPEAR>"]),
                                             10)
        elif vocabulary == 1:
            for trigram in message:
                if re.match("([a-zA-Z][a-zA-Z][a-zA-Z])", trigram):
                    score = score + math.log(probability_table.get(trigram, probability_table["<NOT-APPEAR>"]), 10)
        elif vocabulary == 2:
            for trigram in message:
                if trigram.isalpha():
                    score = score + math.log(probability_table.get(trigram, probability_table["<NOT-APPEAR>"]), 10)

    return score, language


# calculate accuracy of model
def generate_accuracy(correct_label, wrong_label):
    accuracy = correct_label / (correct_label + wrong_label)
    return accuracy


# get evaluation results for a model
def generate_evaluation(results, count):
    correct_label = 0
    wrong_label = 0
    total_correct_eu = 0
    total_correct_ca = 0
    total_correct_gl = 0
    total_correct_es = 0
    total_correct_en = 0
    total_correct_pt = 0

    for result in results:
        predicted_language = result[0]
        correct_language = result[1]
        label = result[2]

        if label == "correct":
            correct_label = correct_label + 1
        elif label == "wrong":
            wrong_label = wrong_label + 1

        # loops over to count correct, wrong outputs
        count[predicted_language + "-" + correct_language] = count.get(
            predicted_language + "-" + correct_language, 0) + 1

    accuracy = generate_accuracy(correct_label, wrong_label)

    if count.get("eu-eu", 0) > 0:
        # number of correct AND predicted eu / sum of predicted eu
        eu_per_class_precision = count.get("eu-eu", 0) / (
                count.get("eu-ca", 0) + count.get("eu-gl", 0) + count.get("eu-es", 0) + count.get("eu-en", 0)
                + count.get("eu-pt", 0) + count.get("eu-eu", 0))

        # number of correct eu
        total_correct_eu = (
                count.get("ca-eu", 0) + count.get("gl-eu", 0) + count.get("es-eu", 0) + count.get("en-eu", 0)
                + count.get("pt-eu", 0) + count.get("eu-eu", 0))
        # number of correct AND predicted eu / sum of correct eu
        eu_per_class_recall = count.get("eu-eu", 0) / total_correct_eu

        # f1 = (2*precision*recall/(precision+recall))
        eu_f1 = (2 * eu_per_class_precision * eu_per_class_recall) / (eu_per_class_precision + eu_per_class_recall)
    else:
        eu_per_class_precision = 0
        eu_per_class_recall = 0
        eu_f1 = 0

    # calculation for ca
    if count.get("ca-ca", 0) > 0:
        ca_per_class_precision = count.get("ca-ca", 0) / (
                count.get("ca-eu", 0) + count.get("ca-gl", 0) + count.get("ca-es", 0) + count.get("ca-en", 0)
                + count.get("ca-pt", 0) + count.get("ca-ca", 0))

        total_correct_ca = (
                count.get("eu-ca", 0) + count.get("gl-ca", 0) + count.get("es-ca", 0) + count.get("en-ca", 0)
                + count.get("pt-ca", 0) + count.get("ca-ca", 0))

        ca_per_class_recall = count.get("ca-ca", 0) / total_correct_ca

        ca_f1 = (2 * ca_per_class_precision * ca_per_class_recall) / (ca_per_class_precision + ca_per_class_recall)
    else:
        ca_per_class_precision = 0
        ca_per_class_recall = 0
        ca_f1 = 0

    # calculation for gl
    if count.get("gl-gl", 0) > 0:
        gl_per_class_precision = count.get("gl-gl", 0) / (
                count.get("gl-eu", 0) + count.get("gl-ca", 0) + count.get("gl-es", 0) + count.get("gl-en", 0)
                + count.get("gl-pt", 0) + count.get("gl-gl", 0))

        total_correct_gl = (
                count.get("eu-gl", 0) + count.get("ca-gl", 0) + count.get("es-gl", 0) + count.get("en-gl", 0)
                + count.get("pt-gl", 0) + count.get("gl-gl", 0))
        gl_per_class_recall = count.get("gl-gl", 0) / total_correct_gl

        gl_f1 = (2 * gl_per_class_precision * gl_per_class_recall) / (gl_per_class_precision + gl_per_class_recall)
    else:
        gl_per_class_precision = 0
        gl_per_class_recall = 0
        gl_f1 = 0

    # calculation for es
    if count.get("es-es", 0) > 0:
        es_per_class_precision = count.get("es-es", 0) / (
                count.get("es-eu", 0) + count.get("es-ca", 0) + count.get("es-gl", 0) + count.get("es-en", 0)
                + count.get("es-pt", 0) + count.get("es-es", 0))

        total_correct_es = (
                count.get("eu-es", 0) + count.get("ca-es", 0) + count.get("gl-es", 0) + count.get("en-es", 0)
                + count.get("pt-es", 0) + count.get("es-es", 0))
        es_per_class_recall = count.get("es-es", 0) / total_correct_es

        es_f1 = (2 * es_per_class_precision * es_per_class_recall) / (es_per_class_precision + es_per_class_recall)
    else:
        es_per_class_precision = 0
        es_per_class_recall = 0
        es_f1 = 0

    if count.get("en-en", 0) > 0:
        en_per_class_precision = count.get("en-en", 0) / (
                count.get("en-eu", 0) + count.get("en-ca", 0) + count.get("en-gl", 0) + count.get("en-es", 0)
                + count.get("en-pt", 0) + count.get("en-en", 0))

        total_correct_en = (
                count.get("eu-en", 0) + count.get("ca-en", 0) + count.get("gl-en", 0) + count.get("es-en", 0)
                + count.get("pt-en", 0) + count.get("en-en", 0))
        en_per_class_recall = count.get("en-en", 0) / total_correct_en

        en_f1 = (2 * en_per_class_precision * en_per_class_recall) / (en_per_class_precision + en_per_class_recall)
    else:
        en_per_class_precision = 0
        en_per_class_recall = 0
        en_f1 = 0

    # calculation for pt
    if count.get("pt-pt", 0) > 0:
        pt_per_class_precision = count.get("pt-pt", 0) / (
                count.get("pt-eu", 0) + count.get("pt-ca", 0) + count.get("pt-gl", 0) + count.get("pt-es", 0)
                + count.get("pt-en", 0) + count.get("pt-pt", 0))

        total_correct_pt = (
                count.get("eu-pt", 0) + count.get("ca-pt", 0) + count.get("gl-pt", 0) + count.get("es-pt", 0)
                + count.get("en-pt", 0) + count.get("pt-pt", 0))
        pt_per_class_recall = count.get("pt-pt", 0) / total_correct_pt

        pt_f1 = (2 * pt_per_class_precision * pt_per_class_recall) / (pt_per_class_precision + pt_per_class_recall)
    else:
        pt_per_class_precision = 0
        pt_per_class_recall = 0
        pt_f1 = 0

    # macro f1 sum of f1s/#of language
    macro_f1 = (eu_f1 + ca_f1 + gl_f1 + es_f1 + en_f1 + pt_f1) / 6

    # weighted average f1 (correct_eu*eu_f1 + correct_ca*ca_f1+ correct_gl*gl_f1+ correct_es*es_f1 + ...)/len(results)
    weighted_avg_f1 = (total_correct_eu * eu_f1 + total_correct_ca * ca_f1 + total_correct_gl * gl_f1
                       + total_correct_es * es_f1 + total_correct_en * en_f1 + total_correct_pt * pt_f1) / len(results)

    return accuracy, eu_per_class_precision, ca_per_class_precision, gl_per_class_precision, es_per_class_precision, \
           en_per_class_precision, pt_per_class_precision, eu_per_class_recall, ca_per_class_recall, \
           gl_per_class_recall, es_per_class_recall, en_per_class_recall, pt_per_class_recall, eu_f1, ca_f1, gl_f1, \
           es_f1, en_f1, pt_f1, macro_f1, weighted_avg_f1


# ------------------ Start code here ------------------

# start part 1
start_existing_model(0, 1, 0, "training-tweets.txt", "test-tweets-given.txt")
start_existing_model(1, 2, 0.5, "training-tweets.txt", "test-tweets-given.txt")
start_existing_model(1, 3, 1, "training-tweets.txt", "test-tweets-given.txt")
start_existing_model(2, 2, 0.3, "training-tweets.txt", "test-tweets-given.txt")

# start part 2
start_custom_model("training-tweets.txt", "test-tweets-given.txt")
