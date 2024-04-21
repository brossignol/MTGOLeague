import os


def get_leagues_id(path, format_, start='2000-01-01', end='2100-01-01'):
    """
    Get leagues ID and data from

    :param path: path to ~\MTGODecklistCache\Tournaments\mtgo.com
    :param start:
    :param format_: starting date, YYYY-MM-DD
    :param end: finishing date, YYYY-MM-DD
    :return:
    """

    leagues = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if format_ in filename and 'league' in filename:
                leagues.append(filename)

    dates = {}
    for league in leagues:
        dates.setdefault(league[-9:-5], []).append(league[-19:-9])

    dates_ = {k: (min(d), max(d)) for k, d in dates.items()}

    id_to_dates = {}
    for id_, date in dates_.items():
        if date[1] >= start and date[0] <= end:
            id_to_dates[id_] = date

    return id_to_dates
