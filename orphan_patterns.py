#! /usr/bin/python3

import os
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter

ifile = 'all_orphans.conllu'

def main(ifile):
    text = open(ifile, 'r', encoding='utf-8').read()
    isent = text.split('\n\n')
    patterns = defaultdict(int)

    for i, sent in enumerate(isent):
        sentence = sent.split('\n')
        processed_tok = []
        for token in sentence:
            token = token.split('\t')
            if len(token) == 10 and token[0] in processed_tok:
                continue
            if len(token) == 10 and token[7] == 'orphan':
                if token[8] == '_':
                    orph_rel = '_'
                else:
                    orph_rel = token[8].split(':')[1]
                processed_tok.append(token[0])
                for elem in sentence:
                    elem = elem.split('\t')
                    if elem[0] == token[6]:
                        head = elem[7]
                        if elem[8] == '_':
                            promoted = '_'
                        else:
                            promoted = elem[8].split(':')[1]
                        more_orph = []
                        for candidate in sentence:
                            candidate = candidate.split('\t')
                            if candidate[6] == elem[0] and candidate[7] == 'orphan' and candidate[0] not in processed_tok:
                                if candidate[8] == '_':
                                    more_orph.append('_')
                                else:
                                    more_orph.append(candidate[8].split(':')[1])
                                processed_tok.append(candidate[0])

                        if len(more_orph) > 0:
                            patterns[(head, promoted, orph_rel) + tuple(more_orph)] += 1
                        else:
                            patterns[(head, promoted, orph_rel)] += 1

    data = OrderedDict(reversed(sorted(patterns.items(), key=itemgetter(1))))
    for entry in data:
        print('{:2}  {}'.format(data[entry], entry))

if __name__ == "__main__":
    main(ifile)
