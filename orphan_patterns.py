#! /usr/bin/python3

import os
import sys
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter

ifile = 'all_orphans.conllu'

def main(ifile):
    text = open(ifile, 'r', encoding='utf-8').read()
    isent = text.split('\n\n')
    patterns = defaultdict(int)
    examples = {}

    for i, sent in enumerate(isent):
        sentence = sent.split('\n')
        sentence = [s.split('\t') for s in sentence if not s.startswith('#')]
        processed_tok = []
        for token in sentence:
            if len(token) == 10 and token[0] in processed_tok:
                continue
            if len(token) == 10 and token[7] == 'orphan':
                if token[8] == '_':
                    orph_rel = '_'
                else:
                    orph_rel = token[8].split(':')[1]
                processed_tok.append(token[0])
                for elem in sentence:
                    if elem[0] == token[6]:
                        head = elem[7]
                        if elem[8] == '_':
                            promoted = '_'
                        else:
                            promoted = elem[8].split(':')[1]
                        more_orph = []
                        for candidate in sentence:
                            if candidate[6] == elem[0] and candidate[7] == 'orphan' and candidate[0] not in processed_tok:
                                if candidate[8] == '_':
                                    more_orph.append('_')
                                else:
                                    more_orph.append(candidate[8].split(':')[1])
                                processed_tok.append(candidate[0])

                        if len(more_orph) > 0:
                            pattern = (head, promoted, orph_rel) + tuple(more_orph)
                        else:
                            pattern = (head, promoted, orph_rel)
                        patterns[pattern] += 1
                        if pattern not in examples:
                            examples[pattern] = ''.join([ (s[1] if '.' not in s[0] else '[' + s[1] + ']') + \
                                                          (' ' if 'SpaceAfter=No' not in s[9] else '' ) for s in sentence])

    data = OrderedDict(reversed(sorted(patterns.items(), key=itemgetter(1))))
    for entry in data:
        print('{:2}  {}  {}'.format(data[entry], entry, examples[entry]))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ifile = sys.argv[1]
    main(ifile)
