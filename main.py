import os
from collections import defaultdict

import pandas as pd

from APIcall import call_and_save
from ArchetypeParser import Parser, ParserEDH
from leagueID import get_leagues_id
from spreadsheet_formatting import create_sheets_inputs, get_archetype_mapping, approx_drop, approx_cedh, combine_json


def main():
    path = 'C:/Projects/mtgo/MTGODecklistCache/Tournaments/mtgo.com'
    format_ = 'vintage'
    data_path = fr'.\leagues_data\{format_}'

    league_ids = get_leagues_id(path, format_=format_, start='2020-04-16', end='2100-01-01')
    # league_ids = [8059]  # cedh
    print(league_ids)

    with open('login.txt') as file:
        login = file.read()

    call_and_save(league_ids, login, out_path=data_path)

    parser = Parser(format_=format_.capitalize(), path=r'C:\Projects\mtgo\MTGOFormatData\Formats')
    arch_mapping = get_archetype_mapping('mapping.csv')
    approx = approx_drop

    # parser = ParserEDH()
    # arch_mapping = defaultdict(lambda: 'edh')
    # approx = approx_cedh

    create_sheets_inputs(league_ids, in_path=data_path, out_path=data_path, parser=parser, arch_mapping=arch_mapping,
                         approx=approx, force=False)

    # combine_json(league_ids, data_path)


if __name__ == '__main__':
    main()
