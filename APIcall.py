import json
import os
from datetime import datetime

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
        # Associate matches
        a += ",type:loginplayeventcoursematch^on:loginplayeventcourseid^to:loginplayeventcourseid" \
             "^list:1^inject_at:matches^hide:loginplayeventcourseid"
        # deck list with docid
        a += ",type:league_decklist_cards^on:loginplayeventcourseid^to:loginplayeventcourseid" \
             "^list:1^inject_at:deck^hide:loginplayeventcourseid'leaguedeckid"
        # map docid to card name
        a += "(type:card_attributes^on:docid^to:digitalobjectcatalogid^list:0^inject_at:name" \
             "^terms:attribute_description=RARITY_STATUS" \
             "^hide:digitalobjectcatalogid'attribute_description'attribute_value)"
        # remove necessary data
        a += '&c:hide=loginid'
        url = census + f's:{login}/' + a
        r = requests.get(url)

        x = eval(r.content)
        xs.append(x)

        print(i, x['returned'])

        if x['returned'] < step:
            break

        i = int(x['league_decklist_list'][-1]['loginplayeventcourseid'])

    return xs


def call_and_save(league_ids, login, out_path):
    """
    Recursively call API for all leagues ID and save decks into json file, one per ID.

    :param league_ids: list of league ID (4 digits number)
    :param login:
    :param out_path:
    :return:
    """
    os.makedirs(out_path, exist_ok=True)
    for league_id in league_ids:
        print('retrieving league', league_id)

        xs = call_api(league_id, login)

        decks = [deck for x in xs for deck in x['league_decklist_list']]
        decks_ = [format_deck(deck) for deck in decks]

        print('writing')
        today = datetime.today().isoformat().replace(':', '-')
        with open(os.path.join(out_path, f'{league_id}_on_{today}.json'), 'w') as file:
            json.dump(decks_, file)
