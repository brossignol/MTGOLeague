from APIcall import call_and_save
from leagueID import get_leagues_id
from spreadsheet_formatting import create_sheets_inputs


def main():
    path = 'C:/Projects/mtgo/MTGODecklistCache/Tournaments/mtgo.com'
    data_path = r'C:\Projects\mtgo\Notebooks\leagues_data\vintage'

    league_ids = get_leagues_id(path, format_='vintage', start='2021-06-01', end='2100-01-01')

    with open('login.txt') as file:
        login = file.read()

    call_and_save(league_ids, login, out_path=data_path)

    create_sheets_inputs(in_path=data_path,
                         out_path=data_path,
                         parser_format='Vintage',
                         parser_path=r'C:/Projects/mtgo/MTGOFormatData/Formats',
                         mapping_file='mapping.csv')


if __name__ == '__main__':
    main()
