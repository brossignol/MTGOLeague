"""
MTGOArchetypeParser/Data/ArchetypeAnalyzer.cs
"""

import json
import os


def eval_condition(cond, main, side):
    type_ = cond.get('Type', cond.get('type'))
    cards = set(cond['Cards'])

    if type_ == 'InMainboard':
        return cards.issubset(main)
    if type_ == 'InSideboard':
        return cards.issubset(side)
    if type_ == 'InMainOrSideboard':
        return cards.issubset(main.union(side))
    if type_ == 'OneOrMoreInMainboard':
        return len(cards.intersection(main)) >= 1
    if type_ == 'OneOrMoreInSideboard':
        return len(cards.intersection(side)) >= 1
    if type_ == 'OneOrMoreInMainOrSideboard':
        return len(cards.intersection(main.union(side))) >= 1
    if type_ == 'TwoOrMoreInMainboard':
        return len(cards.intersection(main)) >= 2
    if type_ == 'TwoOrMoreInSideboard':
        return len(cards.intersection(side)) >= 2
    if type_ == 'TwoOrMoreInMainOrSideboard':
        return len(cards.intersection(main.union(side))) >= 2
    if type_ == 'DoesNotContain':
        return cards.isdisjoint(main) and cards.isdisjoint(side)
    if type_ == 'DoesNotContainMainboard':
        return cards.isdisjoint(main)
    if type_ == 'DoesNotContainSideboard':
        return cards.isdisjoint(side)


def eval_fallback(cards, main, side):
    weight = 0
    for card in cards:
        weight += main.get(card, 0) + side.get(card, 0)

    return weight


class Parser:
    def __init__(self, format_: str, path: str, encoding='utf-8'):
        """
        :param path: name of the format ex: 'Vintage'
        :param format_: path to MTGOFormatData\Formats
        :param encoding:
        """
        self.archs = []
        path_ = os.path.join(os.path.join(path, format_), 'Archetypes')
        for file in os.listdir(path_):
            with open(os.path.join(path_, file), encoding=encoding) as f:
                data = json.load(f)
                self.archs.append(data)

        self.fallbacks = []
        path_ = os.path.join(os.path.join(path, format_), 'Fallbacks')
        for file in os.listdir(path_):
            with open(os.path.join(path_, file)) as f:
                data = json.load(f)
                self.fallbacks.append(data)

    def __call__(self, deck):
        main = {c['CardName']: c['Count'] for c in deck['Mainboard']}
        side = {c['CardName']: c['Count'] for c in deck['Sideboard']}

        res = []
        for arch in self.archs:
            if all(eval_condition(cond, main, side) for cond in arch['Conditions']):
                res.append((arch['Name'], len(arch['Conditions'])))

        if len(res) > 0:
            # return [r[0] for r in sorted(res, key=lambda x: x[1])]
            return min(res, key=lambda x: x[1])[0]

        else:
            weights = []
            for fallback in self.fallbacks:
                weights.append((fallback['Name'], eval_fallback(fallback['CommonCards'], main, side)))

            max_ = max(weights, key=lambda x: x[1])

            if max_[1] > 0:
                return max_[0]
            else:
                return 'Other'
