import os
from APIcall import call_and_save
from leagueID import get_leagues_id
from spreadsheet_formatting import create_sheets_inputs


def main(login):
    login = f's:{login}/'
    path = 'C:/Projects/mtgo/MTGODecklistCache/Tournaments/mtgo.com'
    league_ids = get_leagues_id(path, format_='vintage', start='2022-11-18', end='2100-01-01')

    data_path = './leagues_data/vintage'

    call_and_save(league_ids, login, out_path=data_path)

    create_sheets_inputs(in_path=data_path,
                         out_file=os.path.join(data_path, 'combined.csv'),
                         parser_format='Vintage',
                         parser_path=r'C:/Projects/mtgo/MTGOFormatData/Formats')


if __name__ == '__main__':
    main('mtgoapilogin')
