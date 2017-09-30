#!/usr/bin/python3

import sys, os
from collections import OrderedDict

def check_m3u(data):
    if data[0] == '#EXTM3U':
        if not (len(data) % 2) == 1:
            raise RuntimeError('Even number of entries! Forgotten declaration or url?')
        return 'extended'
    else:
        return 'simple'

def gen_extended(data):
    data = data[1:]
    parsed_m3u  = OrderedDict()

    for n in range(int(len(data)/2)):
        title = data[2*n].split(',')[1]
        url = data[2*n+1]
        parsed_m3u[title] = url

    return parsed_m3u

def gen_simple(data):
    parsed_m3u  = OrderedDict()

    for l in data:
        title = l.split('/')[-1]
        url = l
        parsed_m3u[title] = url

    return parsed_m3u

if __name__ == "__main__":

    if not len(sys.argv) == 2:
        raise ValueError('Wront number of arguments!\nUsage: {} <filename.m3u>'.format(sys.argv[0]))

    elif not os.path.isfile(sys.argv[1]):
        raise ValueError('File {} not found!'.format(sys.argv[1]))
    
    elif not sys.argv[1].endswith('.m3u'):
        raise ValueError('Not a .m3u file!')

    with open(sys.argv[1], 'r') as f:
        data = f.readlines()

    data = [l.strip() for l in data]    

    m3u_type = check_m3u(data)

    if m3u_type == 'extended':
        data = gen_extended(data)
    elif m3u_type == 'simple':
        data = gen_simple(data)

    output = []
    for key in data:
        output.append('{' + '"service":"webradio","name":"' + key + '","uri":"' + data[key] + '"}')

    print('[' + ','.join(output) + ']')
