"""
- Create a set of trigrams for the available strings.
    - Get the string. Pad it with 2 $$ at end and start since trigrams
    - Split the strings into 3 and 
  
"""
import time


class Trigram(set):
    def __init__(self):
        super(Trigram, self).__init__()
        self._trigrams = {}

    def _pad(self, item):
        """
        Adding $$ for padding. Since trigram adding 2 $$.
        Single string search
        :param item: 
        :return: 
        """
        return '$$' + item + '$$'

    def _split(self, string):
        for i in range(len(string) - 4):
            yield string[i:i + 3]

    def add(self, item):
        padded = self._pad(item)
        for gram in self._split(padded):
            self._trigrams.setdefault(gram, {}).setdefault(item, 0)
            self._trigrams[gram][item] += 1

    def search(self, query):
        shared = {}
        # Dictionary mapping n-gram to string to number of occurrences of that
        # trigram in the string that remain to be matched.
        remaining = {}
        padded = self._pad(query)
        for tg in self._split(padded):
            try:
                for match, count in list(self._trigrams[tg].items()):
                    remaining.setdefault(tg, {}).setdefault(match, count)
                    # match as many occurrences as exist in matched string
                    if remaining[tg][match] > 0:
                        remaining[tg][match] -= 1
                        shared.setdefault(match, 0)
                        shared[match] += 1
            except KeyError:
                pass
        results = []
        for match, samegrams in list(shared.items()):
            allgrams = (len(self._pad(query))
                        + (len(match) + 4) - 6 - samegrams + 2)
            similarity = float(samegrams) / allgrams
            if similarity >= 0.2:
                results.append((match, similarity))
        # Sort results by decreasing similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return results

# with open('word_search.tsv','r') as tsv:
#     AoA = [line.strip().split('\t')[0] for line in tsv]
#
#
# # trig = Trigram()
# # for word in AoA:
# #     trig.add(word)
# #
# # start = time.time()
# # a = trig.search('practical')
# # end = time.time()
# # print(end-start)
# # print(a)