import logging

import networkx as nx

from store import store

log = logging.getLogger(__name__)

def run():
    all_outgoing_links_pairs = store.get_outgoing_links()
    effective_links = get_effective_links(all_outgoing_links_pairs)
    print('number of effective_links:' + str(len(effective_links)))
    G = nx.DiGraph()

    for pair in all_outgoing_links_pairs:
        key = pair['key']
        for outgoing_link in pair['links']:
            if outgoing_link in effective_links:
                G.add_edge(key,outgoing_link)
    # print(G.nodes())
    pageRanks = nx.pagerank(G)
    # print(pageRanks)
    if pageRanks is not None:
        for url, rank in pageRanks.iteritems():
            # key is the review url, value is the rank
            store.updatePageRank(url, rank)

def get_effective_links(all_outgoing_links_pairs):
    effective_links = []
    for pair in all_outgoing_links_pairs:
        effective_links.append(pair['key'])
    return effective_links
