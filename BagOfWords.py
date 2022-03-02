import string, os, math

class BagOfWords:

    def __init__(self, fname=None):
        self.bag = {}
        if fname is not None:
            with open(fname) as f:
                words = [word.strip(string.punctuation).lower() for word in f.read().split()]

                for word in words:
                    if word in self.bag:
                        self.bag[word] += 1
                    else:
                        self.bag[word] = 1

# This implements the [] fetch operator, allowing us to access the BagOfWords as if it was a dictionary.
#. For example: b['cat']
    def __getitem__(self, item):
        return self.bag[item]

# This implements the [] store operator, allowing us to access the BagOfWords as if it was a dictionary.
#. For example: b['cat'] = 3

    def __setitem__(self, key, value):
        self.bag[key] = value


# This implements the 'in' operator. It allows us to easily test for membership.
# For example:
#   b = BagOfWords()
#   if 'cat' in b :
#       print('meow')

    def __contains__(self, item):
            return item in self.bag.keys()

# String representation of the bag
    def __repr__(self) :
        return "%s" % (self.bag)

# add additional documents from a corpus to our bag. If noDuplicates is true, we will only
# count each word once. (this is useful for document frequency)

    def append(self, fname, noDuplicates=False):
        with open(fname) as f:
            words = [word.strip(string.punctuation).lower() for word in f.read().split()]
            if noDuplicates:
                words = set(words)
            for word in words:
                if word in self.bag:
                    self.bag[word] += 1
                else:
                    self.bag[word] = 1

# Convert the counts to TFIDF-weighted. TF * log(corpus_size/DF)
# If a word is not present in the DF, we treat DF as 1

    def TFIDFWeights(self, document_frequencies, corpus_size):
        for word in self.bag:
            if word in document_frequencies:
                self.bag[word] = self.bag[word] * math.log(corpus_size / document_frequencies[word])
            else:
                self.bag[word] = self.bag[word] * math.log(corpus_size)

# compare one bag of words to another. returns a value between 0
# (completely orthogonal, or sharing no words in common) and 1 (identical)

    def cosineSimilarity(self, other):
        numerator = sum([self.bag[word] * other.bag[word] for word in self.bag if word in other.bag])
        denominator = math.sqrt(sum([self.bag[word] * self.bag[word] for word in self.bag])) * \
                      math.sqrt(sum([other.bag[word] * other.bag[word] for word in other.bag]))
        return numerator / denominator

# read through a set of files (a corpus) to construct DF.
# If we fail to parse a file, we just move on. This could be more robust.

def constructDF(directoryName):
    DocFreq = BagOfWords()
    for root, dirs, files in os.walk(directoryName):
        for file in files:
            print(file)
            try:
                DocFreq.append(root + "/" + file, noDuplicates=True)
            except:
                print("Error parsing " + file)
                continue
    return DocFreq
