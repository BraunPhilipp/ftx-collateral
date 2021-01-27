#!/usr/bin/env python3
import json
import numpy as np
from itertools import permutations
from plot import MultipleAxisPlot


# current positions
data = json.load(open("example.json"))

collateral = 100000 # usd collateral
n_tick = 5

if __name__ == "__main__":

    # filter key-value pairs
    names = [x for x in data.keys()]
    factors = [x["factor"] for x in data.values()]
    amounts = [x["amount"] for x in data.values()]
    prices = [x["price"] for x in data.values()]

    # create plot
    plot = MultipleAxisPlot(8, 8)
    plot.drawAxis(maxvals=prices, names=names)

    # create permutations of prices
    subtotals = np.array([np.linspace(0, prices[idx], n_tick) * factors[idx] * amounts[idx] for idx in range(len(prices))])
    prices = np.array([np.linspace(0, prices[idx], n_tick) for idx in range(len(prices))])
    perms = list(permutations(list(range(0, n_tick)), len(prices)))
    indices = tuple(range(len(prices)))

    # calculate collateral value and plot
    for perm in perms:
        idx = (indices, perm)
        total = np.sum(subtotals[idx])

        if (total <= collateral) and (0 not in perm):
            print(perm)
            alpha = total / collateral
            plot.drawPolygon(prices[idx], alpha = 0.5 * (alpha ** 2))

    # plot.drawPolygon([1000.0,  6.0,  3.0, 1.0], 0.8)
    plot.savePlot("plot.png", {'dpi':300})
