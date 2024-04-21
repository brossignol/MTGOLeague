import json
import os
from collections import defaultdict

import pandas as pd

from ArchetypeParser import Parser, arch_mapping
from formatdeck import reformat_deck

approx = {0: (0, 0),
          1: (0, 1),
          2: (0, 2),
          3: (0, 3),
          4: (1, 3)}


def create_sheets_inputs(in_path='./leagues_data/vintage',
                         out_file=f'./leagues_data/vintage/vintage_combined.csv',
                         parser_format='Vintage',
                         parser_path=r'C:\Projects\mtgo\MTGOFormatData\Formats',
                         anonymized=True):
    """
    List all json files in folder
    :param in_path: input folder
    :param out_file: input folder
    :param parser_path:
    :param parser_format:
    :param anonymized:
    :return:
    """

    files = []
    for file in os.listdir(in_path):
        if '.json' in file:
            files.append(os.path.join(file))

    parser = Parser('utf-8', format_=parser_format, path=parser_path)

    df = {}

    for file in files:
        print(file)
        with open(os.path.join(in_path, file)) as f:
            decks = json.load(f)

        decks_ = [reformat_deck(deck) for deck in decks]

        for deck in decks_:
            subarch = parser(deck)
            arch = arch_mapping[subarch.casefold()]

            m = min(5, deck['Matches'])

            w = deck['Result'].get('wins', 0)
            l = deck['Result'].get('losses', 0)
            if w + l == 0:
                w, l = approx.get(m, (0, m))

            if w + l == 0:
                continue

            if anonymized:
                player = 'player'
            else:
                player = deck.get('Player')

            df.setdefault('Rank', []).append(deck['loginplayeventcourseid'])
            df.setdefault('Player', []).append(player)
            df.setdefault('Wins', []).append(w)
            df.setdefault('Losses', []).append(l)
            df.setdefault('Matches', []).append(m)
            df.setdefault('Archetype', []).append(arch)
            df.setdefault('Subarchetype', []).append(subarch)
            df.setdefault('Date', []).append(deck['instance_id'][-10:].replace('-', '/'))
            df.setdefault('League ID', []).append(f'{deck["instance_id"][:4]}')

    df = pd.DataFrame(df)

    df.to_csv(out_file, index=False)