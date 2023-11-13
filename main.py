from graphviz import Digraph
import requests
from argparse import ArgumentParser
import re

queue = list()

parser = ArgumentParser()
parser.add_argument("package", nargs=1, default="pandas")

argv = parser.parse_args()
queue.append(argv.package[0])

di = Digraph("Diagram", "shows package structure")
di.node(argv.package[0])

used_packages = [queue[0]]

while queue:
    name = queue.pop()
    json = requests.get(f"https://pypi.org/pypi/{name}/json").json()
    found = json["info"]["requires_dist"]

    if not found:
        continue

    found = list(filter(lambda x: "extra" not in x, found))

    found = list(set(map(lambda x: re.findall("^[-|\\w]+", x)[0], found)))
    print(name, found)

    for package in found:
        if package in used_packages:
            di.edge(name, package)
            continue

        used_packages.append(package)
        di.node(package)
        di.edge(name, package)

        queue.append(package)

di.render('test-output/test-table.gv', view=True)