def format_deck(deck):
    """
    Format deck from APi into compressed format.
    :param deck:
    :return:
    """
    deck_ = {'instance_id': deck['instance_id'],
             'loginplayeventcourseid': deck['loginplayeventcourseid'],
             'Player': deck['player'],
             'Result': deck.get('score', {}),
             'Matches': deck.get('matches', []),
             'Mainboard': {},
             'Sideboard': {}}

    for card in deck['deck']:
        side = 'Mainboard' if card['sideboard'] == 'false' else 'Sideboard'
        name = card['name']['card_name']
        deck_[side][name] = deck_[side].get(name, 0) + int(card['qty'])

    return deck_


def format_deck_classic(deck):
    """
    Format deck from APi into parser compatible format.
    :param deck:
    :return:
    """
    deck_ = {'instance_id': deck['instance_id'],
             'Player': deck['player'],
             'Result': deck.get('score', {}),
             'Matches': len(deck.get('matches', [])),
             'Mainboard': [],
             'Sideboard': []}

    for card in deck['deck']:
        side = 'Mainboard' if card['sideboard'] == 'false' else 'Sideboard'
        assert 'fix multiple card name'
        deck_[side].append({'Count': int(card['qty']), 'CardName': card['name']['card_name']})

    return deck_


def reformat_deck(deck):
    """
    Format deck from compressed format to parser compatible format.
    :param deck:
    :return:
    """
    deck_ = {}
    for k, v in deck.items():
        if k in ('Mainboard', 'Sideboard'):
            deck_[k] = [{'CardName': k_, 'Count': v_} for k_, v_ in deck[k].items()]
        elif k == 'Matches':
            deck_[k] = len(deck.get('Matches', []))
        else:
            deck_[k] = v
    return deck_

