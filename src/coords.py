table = []
sz = 60
all_x = all_y = [i * sz for i in range(8)]
for x in all_x:
    for y in all_y:
        table.append([x, y, x + 60, y + 60])

import pprint

pp = pprint.PrettyPrinter(indent=1)
pp.pprint(table)