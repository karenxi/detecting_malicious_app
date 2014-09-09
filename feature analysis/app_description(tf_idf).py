import re
import json
import math
import sys
import os
import simplejson
from operator import itemgetter

def read_json(filename):
    f = open(filename, 'r')
    data = json.load(f)
    decoded_file = data[0]
    return decoded_file

def read_ids(idsfile):
    f = open(idsfile, 'r')
    result = json.load(f)
    return result

def tokenize(text):
    tokens = []
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9]',' ',text)
    tokens = text.split()
    return tokens

def generate_tf_idf_vectors(decoded_file):
    tf_idf_vectors = {}
    tf_vectors = {}
    idf_vector = {}
    for app_id in decoded_file:
        tf_vector = {}
        words = tokenize(decoded_file[app_id])
        document_id = app_id
        for word in words:
            if word not in tf_vector:
                tf_vector[word] = 0
            tf_vector[word] += 1
        # generate idf_vector for the words that exist in tf_vector
        for word in tf_vector:
            if word not in idf_vector:
                idf_vector[word] = 0
            idf_vector[word] += 1
        # tf_vector dictionary is the value of tf_vectors, whoes keys are the tweest_id
        tf_vectors[document_id] = tf_vector
        #document_id = app_id
    N = len(decoded_file)  # the number of documents in collection
    for word in idf_vector:
        idf_vector[word] = 1.0 * N / idf_vector[word]
    # call generate_document_tf_idf_vector function to calculte the weight
    # tf_idf_vector dictionary is the value of tf_idf_vectors
    for document_id in tf_vectors:
        tf_idf_vectors[document_id] = generate_document_tf_idf_vector(
            tf_vectors[document_id], idf_vector)
    return tf_idf_vectors, idf_vector, tf_vector

def log2(n):
    return math.log(n) / math.log(2)

def generate_document_tf_idf_vector(tf_vector, idf_vector):
    tf_idf_vector = {}
    total_sum = 0.0
    for word in tf_vector:
    # if any token in the query does no occur in the tweet corpus, 
    # then the idf will be unfined. Program should return no results.
        if word not in idf_vector:
            return None
        tf_idf_vector[word] = ((1 + log2(tf_vector[word])) * log2(idf_vector[word]))
        total_sum += tf_idf_vector[word] ** 2
    # NOMALIZATION
    for word in tf_idf_vector:
        tf_idf_vector[word] /= total_sum ** 0.5
    return tf_idf_vector

def calculate_cosine_similarity(tf_idf_vector_i, tf_idf_vector_j):
    cosine_similarity = 0.0
    for word in tf_idf_vector_j:
        if word in tf_idf_vector_i:
            cosine_similarity += tf_idf_vector_j[word] * tf_idf_vector_i[word]
    return cosine_similarity

def main():
    os.chdir("/Users/karen/Desktop/project")
    filename = "app_description.json"
    decoded_file = read_json(filename)
    #print decoded_file

    idsfile = "final_ids.json"
    final_ids = read_ids(idsfile)
    #print final_ids

    ids = []
    for app_id in decoded_file:
        ids.append(app_id)
    tf_idf_vectors, idf_vector,tf_vector = generate_tf_idf_vectors(decoded_file)
    result = {}
    """
    # original: just calculate similarity between apps that have description
    for i in range(len(ids)):
        tf_idf_vector_i = tf_idf_vectors[ids[i]]
        for j in range(i+1, len(ids)):
            tf_idf_vector_j = tf_idf_vectors[ids[j]]
            score = calculate_cosine_similarity(tf_idf_vector_i, tf_idf_vector_j)
            pair_id = ids[i] + "-" + ids[j]
            result[pair_id] = score
    """
    # updated with apps that have empty description
    for i in range(len(final_ids)):
        if final_ids[i] in ids:
            tf_idf_vector_i = tf_idf_vectors[final_ids[i]]
            for j in range(i + 1, len(final_ids)):
                if final_ids[j] in ids:
                    tf_idf_vector_j = tf_idf_vectors[final_ids[j]]
                    score = calculate_cosine_similarity(tf_idf_vector_i, tf_idf_vector_j)

                else:
                    score = 0
                pair_id = final_ids[i] + "-" + final_ids[j]
                result[pair_id] = score
        else:
            for j in range(i + 1, len(final_ids)):
                if final_ids[j] in ids:
                    score = 0
                else:
                    score = 0.876
                pair_id = final_ids[i] + "-" + final_ids[j]
                result[pair_id] = score
    print len(result)

    list_result = []
    list_result.append(result)
    # to json file
    f = open("app_description_similarity.json", "w")
    encoded = simplejson.dumps(list_result, indent = 4, skipkeys = True)
    f. write(encoded)

if __name__ == "__main__":
    main()
