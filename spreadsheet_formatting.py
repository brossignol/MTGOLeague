import json
import os

import pandas as pd

from ArchetypeParser import Parser
from formatdeck import reformat_deck

approx_drop = {0: (0, 0),
               1: (0, 1),
               2: (0, 2),
               3: (0, 3),
               4: (1, 3)}

approx_cedh = {0: (0, 0),
               1: (0, 1),
               2: (0, 2),
               3: (1, 2)}


def get_archetype_mapping(file):
    """
    Expect a csv file with first columns subarchetype, second columns archetype
    :param file:
    :return:
    """
    df = pd.read_csv(file)
    return {k.casefold(): v for _, k, v in df.itertuples()}


def create_sheets_inputs(league_ids, in_path, out_path, parser, arch_mapping, approx, anonymized=True, force=False):
    """
    List all json files and create output csv
    :param league_ids:
    :param in_path: input folder
    :param out_path: output path for .csv files
    :param anonymized: remove player names
    :param force: overwrite existing .csv
    :param approx:
    :param parser:
    :param arch_mapping:
    :return:
    """

    print('creating sheets:')
    for i, league_id in enumerate(sorted(league_ids, reverse=True)):
        file = f'{league_id}.json'
        out_file = os.path.join(out_path, os.path.splitext(file)[0] + '.csv')

        if not force and os.path.exists(out_file) and i > 0:  # always update the most recent
            continue

        print(file)
        df = {}
        with open(os.path.join(in_path, file)) as f:
            decks = json.load(f)

        decks_ = [reformat_deck(deck) for deck in decks]

        for deck in decks_:
            subarch = parser(deck)

            if subarch.casefold() not in arch_mapping:
                arch = 'other'
                print('missing archetype mapping for', subarch)
            else:
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


def combine_json(league_ids, data_path):
    dfs = []
    for i, league_id in enumerate(sorted(league_ids, reverse=True)):
        file = f'{league_id}.json'
        out_file = os.path.join(data_path, os.path.splitext(file)[0] + '.csv')

        dfs.append(pd.read_csv(out_file))

    df = pd.concat(dfs)
    df.to_csv(os.path.join(data_path, 'combined.csv'))

