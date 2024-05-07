from collections import defaultdict

from APIcall import call_and_save
from ArchetypeParser import Parser, ParserEDH
from leagueID import get_leagues_id
from spreadsheet_formatting import create_sheets_inputs, get_archetype_mapping, approx_drop, approx_cedh


def main():
    path = 'C:/Projects/mtgo/MTGODecklistCache/Tournaments/mtgo.com'
    data_path = r'.\leagues_data\cedh'

    league_ids = get_leagues_id(path, format_='modern', start='2020-04-01', end='2020-07-13')

    league_ids = [8059]

    with open('login.txt') as file:
        login = file.read()

    call_and_save(league_ids, login, out_path=data_path)

    # parser = Parser(format_='Vintage', path=r'C:/Projects/mtgo/MTGOFormatData/Formats')
    # arch_mapping = get_archetype_mapping('mapping.csv')
    # approx = approx_drop

    parser = ParserEDH()
    arch_mapping = defaultdict(lambda: 'edh')
    approx = approx_cedh

    create_sheets_inputs(in_path=data_path,
                         out_path=data_path,
                         parser=parser,
                         arch_mapping=arch_mapping,
                         approx=approx)


if __name__ == '__main__':
    main()
