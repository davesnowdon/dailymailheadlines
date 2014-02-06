import pprint
import collections
from random import choice

HEADLINES = """
The cat jumped off the bridge
The fox jumped over the hedge
The car drove round the corneread
""".strip().splitlines()

def generate_chain(headlines):
    model = collections.defaultdict(list)
    for headline in headlines:
        words = [word.lower() for word in headline.split()]
        for i in range(len(words)):
            if i == len(words) - 1:
                model[words[i]].append(None)
                continue
            model[words[i]].append(words[i + 1])
    return model

def headline(model, seed=None, length=20):
    # while seed is None or model[seed] == [None]:
    seed = choice(model.keys()) if seed is None else seed
    phrase = [seed]
    while len(phrase) < length:
        if not phrase[-1] in model.keys():
            break
        new = choice(model[phrase[-1]])
        if new is None:
            break
        phrase.append(new)
    return " ".join(phrase), len(phrase)


def gimme_headlines(headlines):
    model = generate_chain(headlines)
    while True:
        h, length = headline(model)
        if length > 1:
            yield h


if __name__ == '__main__':
    count = 0
    for line in gimme_headlines(HEADLINES):
        count += 1
        print line
        if count > 3:
            break
