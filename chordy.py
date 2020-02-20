#! /usr/bin/env python3

# Fin Warman, Initial release: 19-02-2020
# Chords data credit: github.com/tombatossals/chords-db/blob/master/lib/guitar.json

# TODO:
# - Use argparse for cli arg, and additional flags (e.g. -v for voicings, etc.)
# - Add views for multiple voicings (not just first)
# - Add handling for capos
# - Truncate start of fretboard for higher-up fingerings
# - Add handling for alt tunings (?)

import argparse
import json
import sys
import re
from typing import List
import os


def loadChordsData():
    chords = None

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'guitar.json')

    with open(filename) as chords_file:
        chords = json.load(chords_file)
    return chords


def getSuffixIndex(data, key, suffix):
    index = -1
    for ch in data['chords'][key]:
        index += 1
        if suffix == ch['suffix']:
            return index
    print('Could not find suffix {} for key {}'.format(
        suffix, key.replace('sharp', '#')))
    quit()


def getChordInfo(data, key, suffix='major'):
    key = key.replace('#', 'sharp')
    suffix_index = getSuffixIndex(data, key, suffix)
    chord_info = data['chords'][key][suffix_index]
    return chord_info

# make text bold


def b(s):
    return "\033[1m{}\033[0m".format(s)

# make text faint


def f(s):
    return "\033[2m{}\033[0m".format(s)

# underline text


def u(s):
    return "\033[4m{}\033[0m".format(s)


def printChord(chord, name, suffix):
    max_fret = max(max(chord['frets']), 4)
    frets = chord['frets']
    fingers = chord['fingers']

    capo = chord.get('capo', False)
    basefret = chord.get('baseFret', 1) - 1
    barres = chord.get('barres', [])
    # print(capo)
    # print(basefret)
    # print(barres)
    # TODO - Use real barre/basefret info for drawing barre

    header = '{0}E{0}A{0}D{0}G{0}B{0}E{0}'.format(' ')

    width = 21

    print()
    print('{}'.format(header).center(width))

    if capo:
        print(f('    ╷ ╷ ╷ ╷ ╷ ╷ ╷'))

    p = '╷'
    if capo:
        print(f('bar.|'), end='')
        p = '|'
    else:
        print(f('    ╷'), end='')

    for i in range(6):
        s = f('‗')
        if frets[i] == -1:
            s = f('x')
        elif frets[i] == 0:
            s = '‗'
        print(s + f(p), end='')
    print()

    for fret in range(1, max_fret + 2):
        sep = f('_') if fret in [3, 5, 7, 9, 12, 15, 17, 19] else ' '
        div = f('|')

        row = div

        row_fingers = []  # track fingers used for this fret
        barre_start = 6
        barre_end = 0

        for string in range(len(frets)):
            if(frets[string] == fret):
                finger = str(fingers[string])
                row += b(finger)
                row_fingers.append(finger)
            else:
                row += sep
            row += div

        # add barre markings if all fingers are the same
        if set(row_fingers) == {'1'}:
            barre_start = row.index('1\033')
            barre_end = (len(row) - 1 - row[::-1].index('\0331'))
            row = row[:barre_start] + \
                row[barre_start:barre_end].replace(
                    sep, b('-')) + row[barre_end:]

        print('{0: 3} {1}'.format(fret + basefret, row))

    print(f('    ╵ ╵ ╵ ╵ ╵ ╵ ╵'))
    print(('{0}{1}'.format(name, suffix)).center(width))
    print()


def printColumns(lst: List[str], cols=5):
    widest_length = len(max(lst, key=len))

    row_count = 0
    for i in lst:
        print(i.ljust(widest_length + 1), end='')
        row_count += 1
        if row_count % cols == 0:
            print()
    print('')


def showValidInputs(keys, suffixes):
    if(keys):
        print('Available keys:\n')
        printColumns(keys, 12)

    if(suffixes):
        print('Available suffixes:\n')
        printColumns(suffixes, 6)


data = loadChordsData()

keys = data['keys']
suffixes = data['suffixes']

parser = argparse.ArgumentParser(
    description='Chordy: Find voicings for guitar chords.')

parser.add_argument('target_chord', nargs='?', action='store')
parser.add_argument('-a', '--all-voicings',
                    dest='all', action='store_true')

args = parser.parse_args()
if args.target_chord is None:
    print("\nNo chord specified\n")
    showValidInputs(keys, suffixes)
    print("\nUse -h flag for more help.\n")
    quit()

target_chord = args.target_chord

p = re.compile('^([A-G][b#]?)')
s = p.search(target_chord)
if not s:
    print("\n'{}' is not a valid chord\n".format(target_chord))
    showValidInputs(keys, suffixes)
    print()
    quit()

key = s.group(1)
suffix = target_chord.replace(key, '', 1)

if(len(suffix) == 0):
    suffix = 'major'
elif(suffix == 'maj'):
    suffix = 'major'
elif(suffix == 'min' or suffix == 'm'):
    suffix = 'minor'

if suffix not in suffixes:
    print("\n'{}' is not a valid suffix\n".format(suffix))
    showValidInputs(None, suffixes)
    print()
    quit()

chord = getChordInfo(data, key, suffix)

print()
if(args.all):
    for i in range(len(chord['positions'])):
        position = chord['positions'][i]
        print("Position {}:".format(i+1))
        printChord(position, chord['key'], chord['suffix'])
else:
    position = chord['positions'][0]
    print("Showing position {0} of {1}:".format(1, len(chord['positions'])))
    printChord(position, chord['key'], chord['suffix'])
    print('Use flag -a to show more positions.\n')
