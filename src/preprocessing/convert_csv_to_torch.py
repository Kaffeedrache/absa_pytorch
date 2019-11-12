#!/usr/bin/env python3

# Convert data from csv to pytorch-readable csv which has been
# split into training, developement and test set with only the
# desired labels.
# If a 'TEST_FILENAME' is given, this is used as the test set,
# otherwise a random sample of 'TEST_RATIO' size from the training
# data is used.

# @author Wiltrud Kessler, 2019-11-06

import pandas as pd
import numpy as np
from nltk.tokenize import WordPunctTokenizer


VAL_RATIO = 0.2
TEST_RATIO = 0.3

KEEPLABELS = ['1', '-1', '0', 'conflict']
#KEEPLABELS = ['1', '-1', '0']
#KEEPLABELS = ['1', '-1']

TEXT_COLNAME = 'text'
POLARTITY_COLNAME = 'polarity'

#ASPECT_COLNAME = 'category'
ASPECT_COLNAME = 'term'

PREFIX = "semeval2014_restaurants"
DATA_FILENAME = "data/" + PREFIX + "_train_" + ASPECT_COLNAME + ".csv"
TEST_FILENAME = "data/" + PREFIX + "_test_" + ASPECT_COLNAME + ".csv"
OUTPREFIX = PREFIX + "_" + ASPECT_COLNAME + "_" + ".".join(KEEPLABELS)


def custom_tokenize(text):
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(text)
    words = [word for word in tokens if word.isalnum()]
    return words

def preprocess_data(df):
    df[TEXT_COLNAME] = df[TEXT_COLNAME].apply(lambda x: x.replace('[comma]',',').lower())
    df[TEXT_COLNAME] = df[TEXT_COLNAME].apply(custom_tokenize)
    df[TEXT_COLNAME] = df[TEXT_COLNAME].apply(lambda x:" ".join(x))
    df[ASPECT_COLNAME] = df[ASPECT_COLNAME].apply(lambda x: x.lower())
    df[ASPECT_COLNAME] = df[ASPECT_COLNAME].apply(custom_tokenize)
    df[ASPECT_COLNAME] = df[ASPECT_COLNAME].apply(lambda x:" ".join(x))
    return df

def write_csv(df, test_df, prefix = "dataset", seed=999):
    print("Write to " + prefix)
    idx = np.arange(df.shape[0])
    np.random.seed(seed)
    np.random.shuffle(idx)

    val_size = int(len(idx) * VAL_RATIO)
    df.iloc[idx[:val_size], :].to_csv(prefix + "_val.csv", index=False)

    if test_df is None:
        test_size = int(len(idx) * TEST_RATIO)
        df.iloc[idx[val_size:-test_size], :].to_csv(prefix + "_train.csv", index=False)
        df.iloc[idx[-test_size:], :].to_csv(prefix + "_test.csv", index=False)
    else:
        print("use test df")
        df.iloc[idx[val_size:], :].to_csv(prefix + "_train.csv", index=False)
        test_df.to_csv(prefix + "_test.csv", index=False)



# Read and preprocess training data
traindata = pd.read_csv(DATA_FILENAME)
traindata = preprocess_data(traindata)

# Remove unwanted labels
traindata = traindata[traindata[POLARTITY_COLNAME].isin(KEEPLABELS)]

testdata = None
if TEST_FILENAME is not None:
    # Read and preprocess test data
    testdata = pd.read_csv(TEST_FILENAME)
    testdata = preprocess_data(testdata)
    testdata = testdata.astype({POLARTITY_COLNAME: 'object'})

    # Remove unwanted labels
    testdata = testdata[testdata[POLARTITY_COLNAME].isin(KEEPLABELS)]

# Write out to csv
write_csv(traindata, testdata, OUTPREFIX)
