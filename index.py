import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt


# concorde = best plane
start_url = 'https://en.wikipedia.org/wiki/Concorde'


graph = nx.DiGraph()
graph.add_node(start_url)


def crawl_page(url, level=0):
    if level == 3:
        return
    try:
        # meow meow meow
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/wiki/') and ':' not in href:
                linked_url = 'https://en.wikipedia.org' + href
                graph.add_node(linked_url)
                graph.add_edge(url, linked_url)

                crawl_page(linked_url, level+1)
    except:
        pass


crawl_page(start_url)


# honestly im not even sure what this does
pos = nx.spring_layout(graph, k=0.1)
plt.figure(figsize=(20, 20))
nx.draw_networkx_nodes(graph, pos, node_size=10, node_color='b')
nx.draw_networkx_edges(graph, pos, alpha=0.2)
nx.draw_networkx_labels(graph, pos, font_size=10)
plt.axis('off')
plt.show()