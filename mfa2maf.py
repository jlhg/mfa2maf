#!/usr/bin/env python

import re
import sys


def output_data(align_set, seq, ref_length):
    data = []
    for seqid in align_set:
        data.append('\t'.join(['s ',
                               seqid.group(1).replace(' ', '').replace('.', '_').replace('(CAF1)', '') + '.' + seqid.group(2),
                               seqid.group(3),
                               str(len(seq[seqid].replace('-', ''))),
                               seqid.group(4),
                               ref_length,
                               seq[seqid]]))
        ref_length = '0'

    return '\n'.join(data) + '\n\n'


def main(argvs):
    if len(argvs) != 3:
        sys.exit('Usage: mfa2maf.py <input.mfa> <output.maf> <ref_genome_length>')

    header = re.compile('>(.+)\s(.+):(.+)-.+\s\((\S)\)')
    header_gap = re.compile('>(.+)\s(.+): gap between (.+) and.+\s\((\S)\)')

    with open(argvs[0], 'r') as fi, open(argvs[1], 'w') as fo:
        fo.write('##maf\n')
        fo.flush()

        align_set = []
        seq = {}

        for line in fi:
            if line[0] == '=':
                fo.write('a\n')
                fo.write(output_data(align_set, seq, argvs[2]))
                fo.flush()
                align_set = []
                seq.clear()
            elif line[0] == '>':
                seqid = header.match(line)
                if seqid is None:
                    seqid = header_gap.match(line)
                seq[seqid] = ''
                align_set.append(seqid)
            elif line[0] in ('A', 'T', 'C', 'G', 'N', '-'):
                seq[seqid] = seq[seqid] + line.rstrip()


if __name__ == '__main__':
    main(sys.argv[1:])
