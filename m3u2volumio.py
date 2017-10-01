#!/usr/bin/python3

import sys, os
from collections import OrderedDict

changelog = {}

# ================ Configuration =================

version = 0.2
changelog[0.1] = "Init"
changelog[0.2] = "Added handling for non-ascii characters and changelog."

# ================================================

def check_m3u(data):
    ''.join(data)
    if data[0] == '#EXTM3U':
        if not (len(data) % 2) == 1:
            raise RuntimeError('Even number of entries! Forgotten declaration or uri?')
        return 'extended'
    else:
        return 'simple'

def gen_extended(data):
    data = data[1:]
    parsed_m3u  = OrderedDict()
    trigger_www = {}

    for n in range(int(len(data)/2)):
        title = data[2*n].split(',')[1]
        uri = data[2*n+1]

        try:
            title = title.encode('ascii').decode('utf-8')
            uri = uri.encode('ascii').decode('utf-8')

        except UnicodeEncodeError:
            nonascii = set([c for c in ''.join([title,uri]) if ord(c) >= 128])
            print('Warning: Non-ASCII character(s) {} found and omitted in:\n{}\n{}\nCheck your encoding!\n'.format(nonascii,title,uri), file=sys.stderr)
            title = title.encode('ascii', 'ignore').decode('utf-8')
            uri = uri.encode('ascii', 'ignore').decode('utf-8')

        parsed_m3u[title] = uri

        if 'http://' in uri or 'https://' in uri:
            trigger_www[title] = 1
        else:
            trigger_www[title] = 0

    return parsed_m3u, trigger_www

def gen_simple(data):
    parsed_m3u  = OrderedDict()
    trigger_www = {}

    for l in data:

        title = l.split('/')[-1]
        uri = l

        try:
            title = title.encode('ascii').decode('utf-8')
            uri = uri.encode('ascii').decode('utf-8')

        except UnicodeEncodeError:
            nonascii = set([c for c in ''.join([title,uri]) if ord(c) >= 128])
            print('Warning: Non-ASCII character(s) {} found and omitted in:\n{}\n{}\nCheck your encoding!\n'.format(nonascii,title,uri), file=sys.stderr)
            title = title.encode('ascii', 'ignore').decode('utf-8')
            uri = uri.encode('ascii', 'ignore').decode('utf-8')

        parsed_m3u[title] = uri
        if 'http://' in uri or 'https://' in uri:
            trigger_www[title] = 1
        else:
            trigger_www[title] = 0

    return parsed_m3u, trigger_www

if __name__ == "__main__":

    # =============== Argument parser=================

    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print('Usage:')
        print('\t{} <filename.m3u>'.format(sys.argv[0]))
        print('\t-c, --changelog')
        print('\t-h, --help')
        print('\t-v, --version')
        sys.exit(0)
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-v', '--version']:
        print("Version {}".format(version))
        sys.exit(0)
    
    elif len(sys.argv) > 1 and sys.argv[1] in ['-c', '--changelog']:
        for key in changelog:
            print(key,"\t",changelog[key])
        sys.exit(0)

    if not len(sys.argv) == 2:
        raise ValueError('Wront number of arguments!\nUsage: {} <filename.m3u>'.format(sys.argv[0]))

    elif not os.path.isfile(sys.argv[1]):
        raise ValueError('File {} not found!'.format(sys.argv[1]))
    
    elif not sys.argv[1].endswith('.m3u'):
        raise ValueError('Not a .m3u file!')

    # ================================================


    with open(sys.argv[1], 'r') as f:
        data = f.readlines()

    data = [l.strip() for l in data]    
    data = list(filter(None, data))

    m3u_type = check_m3u(data)

    if m3u_type == 'extended':
        data, trigger_www = gen_extended(data)
    elif m3u_type == 'simple':
        data, trigger_www = gen_simple(data)

    output = []

    for key in data:

        if trigger_www[key]:
            output.append('{' + '"service":"webradio","title":"' + key + '","name":"' + key + '","uri":"' + data[key] + '"}')

        else:
            if '-' in key and key.count('-') == 1:
                artist = key.split('-')[0].strip()
                title = key.split('-')[1].strip()

                # Assuming file extention: Removing it
                title_temp = '.'.join(title.split('.')[:-1])
                if not title_temp == '':
                    title = title_temp
                
                output.append('{' + '"service":"mpd","title":"' + title + '","artist":"' + artist + '","uri":"' + data[key] + '"}')

            else:
                # Assuming file extention: Removing it
                title_temp = '.'.join(key.split('.')[:-1])
                if not title_temp == '':
                    title = title_temp
                output.append('{' + '"service":"mpd","title":"' + title + '","uri":"' + data[key] + '"}')

    print('[' + ','.join(output) + ']')
