# coding=utf-8
import io
import operator
import pickle

import numpy as np


def make_token_label_encoding(data_files, labels_file, token_label_encoding_file):
    print "make_token_label_encoding"
    token_label_counts = {}
    for path in data_files:
        token_label_counts = update_token_label_counts(
            path, token_label_counts)
    
    label_str_to_id = load_labels(labels_file)

    token_label_encoding = {}
    for token, labels in sorted(token_label_counts.items(), key=operator.itemgetter(0)):
        label_encoding = np.zeros(29)
        for label in labels.keys():
            label_id = int(label_str_to_id[label])
            label_encoding[label_id] = token_label_counts[token][label]
        token_label_encoding[token] = label_encoding / np.sum(label_encoding)

    with open(token_label_encoding_file, 'wb') as f:
        pickle.dump(token_label_encoding, f)


def update_token_label_counts(path, token_label_counts):
    print "update_token_label_counts"
    with io.open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            _, token, label = line.split()
            if label == "O":
                return token_label_counts

            if token not in token_label_counts:
                token_label_counts[token][label] = 1
            elif label not in token_label_counts[token]:
                token_label_counts[token][label] = 1
            else:
                token_label_counts[token][label] += 1
    return token_label_counts


def load_labels(path):
    print "load_labels"
    label_str_to_id = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            label, id = line.split()
            label_str_to_id[label] = id
    return label_str_to_id


if __name__ == "__main__":
    train_filename = ""
    dev_filename = ""
    labels_file = ""
    token_label_encoding_file = ""

    data_files = [train_filename, dev_filename]
    make_token_label_encoding(data_files, labels_file, token_label_encoding_file)
    print "Done."
