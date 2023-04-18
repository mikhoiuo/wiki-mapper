import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

# Initialize variables
start_url = 'https://en.wikipedia.org/wiki/Sumeria'
visited_urls = set()
level = 0
max_level = 2  # change this to limit the number of layers
G = nx.Graph()

def crawl(url, level):
    # Stop if we have reached the maximum level or the page has been visited before
    if level > max_level or url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch the HTML content of the page and parse it with BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all hyperlinks on the page
    links = soup.find_all('a')

    # Filter out links that don't lead to Wikipedia articles or are on the exclusion list
    for link in links:
        href = link.get('href')
        if href and href.startswith('/wiki/') and not href.startswith(('/wiki/Help:', '/wiki/Wikipedia:', '/wiki/Talk:')):
            target_url = 'https://en.wikipedia.org' + href
            G.add_edge(url, target_url)

            # Add node attributes for display purposes
            if not G.nodes.get(url):
                G.nodes[url]['size'] = 10
                G.nodes[url]['label'] = BeautifulSoup(requests.get(url).content, 'html.parser').title.string
            if not G.nodes.get(target_url):
                G.nodes[target_url]['size'] = 10
                G.nodes[target_url]['label'] = BeautifulSoup(requests.get(target_url).content, 'html.parser').title.string

            # Increase node size every 25 links
            if len(G.adj[url]) % 25 == 0:
                G.nodes[url]['size'] += 1
            if len(G.adj[target_url]) % 25 == 0:
                G.nodes[target_url]['size'] += 1

            # Recursively crawl the target page
            crawl(target_url, level + 1)

# Start crawling from the initial URL
crawl(start_url, level)

# Position nodes using the spring layout algorithm
pos = nx.spring_layout(G, k=0.3)

# Draw the graph and save it as an image
nx.draw_networkx_nodes(G, pos, node_size=[G.nodes[n]['size'] for n in G.nodes()])
nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]['label'] for n in G.nodes()}, font_size=8)
nx.draw_networkx_edges(G, pos, alpha=0.2)
plt.axis('off')
plt.savefig('wiki_map.png', dpi=300)