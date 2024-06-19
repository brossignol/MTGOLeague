import json
import os
import time

import requests

from formatdeck import format_deck

census = 'https://census.daybreakgames.com/'


def call_api(league_id, login, firstid=0):
    i = firstid
    step = 5000
    xs = []

    while True:
        # Decks ids by leagues ID
        a = f"get/mtgo/league_decklist?instance_id=^{league_id}&loginplayeventcourseid=>{i}&c:limit={step}"
        # wins/losses
        a += "&c:join=type:league_match_wins^on:loginplayeventcourseid^to:loginplayeventcourseid" \
             "^list:0^inject_at:score^hide:loginplayeventcourseid"
        # associated matches
        a += ",type:loginplayeventcoursematch^on:loginplayeventcourseid^to:loginplayeventcourseid" \
             "^list:1^inject_at:matches^hide:loginplayeventcourseid"
        # decklist with cards docid
        a += ",type:league_decklist_cards^on:loginplayeventcourseid^to:loginplayeventcourseid" \
             "^list:1^inject_at:deck^hide:loginplayeventcourseid'leaguedeckid"
        # map docid to card names
        a += "(type:card_attributes^on:docid^to:digitalobjectcatalogid^list:0^inject_at:name" \
             "^terms:attribute_description=RARITY_STATUS" \
             "^hide:digitalobjectcatalogid'attribute_description'attribute_value)"
        # remove unnecessary data
        a += '&c:hide=loginid'
        url = census + f's:{login}/' + a
        r = requests.get(url)

        x = json.JSONDecoder().decode(r.content.decode('utf8'))
        xs.append(x)

        print(i, x['returned'])

        if x['returned'] < step:
            break

        i = int(x['league_decklist_list'][-1]['loginplayeventcourseid'])

    return xs


def call_and_save(league_ids, login, out_path, force_update=False):
    """
    Recursively call API for all leagues ID and save decks into json file, one per ID.

    :param league_ids: list of league ID (4 digits number)
    :param login:
    :param out_path:
    :return:
    """
    os.makedirs(out_path, exist_ok=True)
    for i, league_id in enumerate(sorted(league_ids, reverse=True)):
        out_file = os.path.join(out_path, f'{league_id}.json')
        if os.path.exists(out_file):
            if not force_update and i != 0:  # if already exist and not last leagues
                continue
            with open(out_file) as file:
                decks = json.load(file)
                start_id = max([deck['loginplayeventcourseid'] for deck in decks])
        else:
            decks = []
            start_id = 0

        print('retrieving league', league_id, i + 1, '/', len(league_ids))
        s = time.time()
        xs = call_api(league_id, login, start_id)
        print('done in', time.time() - s, 's')

        if len(xs) > 0:
            try:
                decks.extend(format_deck(deck) for x in xs for deck in x['league_decklist_list'])

                print('writing')
                with open(out_file, 'w') as file:
                    json.dump(decks, file, indent=0)
            except Exception as e:
                print('failed writing raw')
                with open(out_file + '-failed.json', 'w') as file:
                    json.dump([deck for x in xs for deck in x['league_decklist_list']], file, indent=2)

                raise e
