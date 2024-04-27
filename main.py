import os
from APIcall import call_and_save
from leagueID import get_leagues_id
from spreadsheet_formatting import create_sheets_inputs


def main():
    path = 'C:/Projects/mtgo/MTGODecklistCache/Tournaments/mtgo.com'
    data_path = r'C:\Projects\mtgo\MTGO classifier\leagues_data\vintage'

    league_ids = get_leagues_id(path, format_='vintage', start='2022-11-18', end='2100-01-01')
    # league_ids = ['8115']

    with open('login.txt') as file:
        login = file.read()

    call_and_save(league_ids, login, out_path=data_path)

    create_sheets_inputs(in_path=data_path,
                         out_file=os.path.join(data_path, 'combined.csv'),
                         parser_format='Vintage',
                         parser_path=r'C:/Projects/mtgo/MTGOFormatData/Formats')


if __name__ == '__main__':
    main()
