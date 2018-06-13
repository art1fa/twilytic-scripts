# pylint: disable=invalid-name
# pylint: disable=missing-docstring

import networkx as nx
from itertools import combinations

import rethinkdb as r 

from db_conf import get_conf

rdb_config = get_conf()

r.connect(**rdb_config).repl()

G = nx.Graph()

for user in r.table('users').get_field('list_tags').run():
    list_tags = user
    # Add list tags
    for item in list_tags:
        if not item['text'] in G:
            attr = {'type': 'list_tag', 'weight': 1}
            G.add_node(item['text'], **attr)
        else:
            G.nodes[item['text']]['weight'] += 1
    for edge in combinations([item['text'] for item in list_tags], 2):
        ni, nj = edge
        if not nj in G[ni]:
            attr = {'type': 'tag_tag', 'weight': 1}
            G.add_edge(ni, nj, **attr)
        else:
            G.edges[ni, nj]['weight'] += 1
    # Add users
    # if user['listed_count'] > 0:
    #     G.add_node(user['screen_name'], type='user')
    #     for edge in [item['text'] for item in list_tags]:
    #         ni, nj = user['screen_name'], edge
    #         attr = {'type': 'user_tag', 'weight': 1}
    #         G.add_edge(ni, nj, **attr)

nx.write_graphml(G, 'user_tags.graphml')

#Open and customize exported graph with Gephi























# options = {
#     #'node_size': [x*100 for x in node_weights],
#     #'edge_color': [x/max(edge_weights) for x in edge_weights],
#     'edge_color': 'grey',
#     #'node_color': [x/max(node_weights) for x in node_weights],
#     #'labels': labels,
#     'cmap': plt.cm.YlOrRd,
#     'alpha': 0.9,
#     'edge_cmap': plt.cm.Greys,
#     'edge_vmax': 1.3,
#     'edge_vmin': 0,
#     'with_labels': True
#     }
