from flask import Flask, render_template, jsonify, request
from tries import TrieNode, search
import time
from trigram import Trigram
app = Flask(__name__, static_url_path='/static')

# read dictionary file into a trie
word_list = []
with open('word_search.tsv','r') as tsv:
    AoA = [line.strip().split('\t')[0] for line in tsv]

# print('Creating a tree')
# trie = TrieNode()
# for word in AoA:
#     trie.insert(word)

trig = Trigram()
for word in AoA:
    trig.add(word)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/search')
def search1():
    query = request.args.get('query')
    print("getting search results")
    start = time.time()
    result = trig.search(query)
    lst2 = [item[0] for item in result][:25]
    # results = []
    # for i in range(3):
    #     for word1 in result_hash[i]:
    #         results.append(word1)
    end = time.time()
    print("Search took %g s" % (end - start))
    return jsonify({'query': query, 'suggestions': lst2})

if __name__ == '__main__':
    app.run()