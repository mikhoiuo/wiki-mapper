import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import re
import time

import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import re

def get_links(url):
    """
    Given a Wikipedia URL, returns a list of links to other Wikipedia pages.
    Excludes links to pages with "/wiki/Help:", "/wiki/Wikipedia:", or "/wiki/Talk:" in the URL.
    """
    response = requests.get(url, timeout=3)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and not any(excluded in href for excluded in ['/wiki/Help:', '/wiki/Wikipedia:', '/wiki/Talk:', 'wiki/Special:', 'wiki/Category:', 'wiki/User:', 'wiki/File:', 'wiki/Portal:', 'wiki/ISBN_(identifier)', 'wiki/Template:']):
            links.append('https://en.wikipedia.org' + href)
    return links

def crawl_wikipedia(start_url, vis, max_depth=3):
    """
    Given a starting Wikipedia URL, crawls every page on Wikipedia that is directly linked to it
    (NOT sources) up to a maximum depth, and returns a networkx graph representing the relationships
    between pages.
    """
    G = nx.Graph()
    nodes_to_visit = [(start_url, 0)]
    while nodes_to_visit:
        node_url, depth = nodes_to_visit.pop(0)
        if depth >= max_depth:
            break
        if node_url in vis:
            continue
        vis.add(node_url)
        node_title = re.sub(r'^.*\/wiki\/(.*)$', r'\1', node_url).replace('_', ' ')
        G.add_node(node_title)
        links = get_links(node_url)
        for link_url in links:
            if link_url in vis:
                continue
            print(link_url)
            link_title = re.sub(r'^.*\/wiki\/(.*)$', r'\1', link_url).replace('_', ' ')
            G.add_node(link_title)
            G.add_edge(node_title, link_title)
            nodes_to_visit.append((link_url, depth+1))
    return G

def generate_map(start_url, max_depth=3, node_size_multiplier=25, min_node_distance=10):
    """
    Given a starting Wikipedia URL, crawls every page on Wikipedia that is directly linked to it
    (NOT sources) up to a maximum depth, and generates a networkx graph representing the relationships
    between pages. Returns a matplotlib figure representing the graph.
    Node sizes start at 10 and increase by node_size_multiplier for every 25 linked nodes.
    Nodes are spaced at least min_node_distance apart on all axes.
    """
    visited = set()
    G = crawl_wikipedia(start_url, visited, max_depth)
    pos = nx.spring_layout(G, k=0.02, scale=2, seed=42)
    fig, ax = plt.subplots(figsize=(20,20))
    for node in G.nodes():
        degree = G.degree[node]
        node_size = max(5, (degree // 25) * node_size_multiplier + 10)
        ax.text(pos[node][0], pos[node][1], node, fontsize=node_size, ha='center', va='center', bbox=dict(facecolor='w', edgecolor='k', boxstyle='circle'))
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3)
    ax.set_axis_off()
    return fig

import os

# Replace this with your desired output filename
output_filename = 'concorde_map.png'

# Remove the output file if it already exists
if os.path.exists(output_filename):
    os.remove(output_filename)

# Generate the map
fig = generate_map('https://en.wikipedia.org/wiki/Concorde', max_depth=1, node_size_multiplier=25, min_node_distance=10)

# Save the figure to a PNG file
fig.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')

def crawl_wikipedia(start_url, vis, max_depth=3):
    """
    Given a starting Wikipedia URL, crawls every page on Wikipedia that is directly linked to it
    (NOT sources) up to a maximum depth, and returns a networkx graph representing the relationships
    between pages.
    """
    G = nx.Graph()
    nodes_to_visit = [(start_url, 0)]
    while nodes_to_visit:
        node_url, depth = nodes_to_visit.pop(0)
        if depth >= max_depth:
            break
        if node_url in vis:
            continue
        vis.add(node_url)
        node_title = re.sub(r'^.*\/wiki\/(.*)$', r'\1', node_url).replace('_', ' ')
        G.add_node(node_title)
        links = get_links(node_url)
        for link_url in links:
            if link_url in vis:
                continue
            print(link_url)
            link_title = re.sub(r'^.*\/wiki\/(.*)$', r'\1', link_url).replace('_', ' ')
            G.add_node(link_title)
            G.add_edge(node_title, link_title)
            nodes_to_visit.append((link_url, depth+1))
    return G

def generate_map(start_url, max_depth=3, node_size_multiplier=2, min_node_distance=10):
    """
    Given a starting Wikipedia URL, crawls every page on Wikipedia that is directly linked to it
    (NOT sources) up to a maximum depth, and generates a networkx graph representing the relationships
    between pages. Returns a matplotlib figure representing the graph.
    Node sizes start at 10 and increase by node_size_multiplier for every 25 linked nodes.
    Nodes are spaced at least min_node_distance apart on all axes.
    """
    visited = set()
    G = crawl_wikipedia(start_url, visited, max_depth)
    pos = nx.spring_layout(G, k=5, scale=.5, seed=42)
    fig, ax = plt.subplots(figsize=(100,100))
    for node in G.nodes():
        degree = G.degree[node]
        node_size = max(5, (degree // 25) * node_size_multiplier + 10)
        ax.text(pos[node][0], pos[node][1], node, fontsize=node_size, ha='center', va='center', bbox=dict(facecolor='w', edgecolor='k', boxstyle='circle'))
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.3)
    ax.set_axis_off()
    return fig

import os
output_filename = 'concorde_map.png'

# Remove the output file if it already exists
if os.path.exists(output_filename):
    os.remove(output_filename)

fig = generate_map('https://en.wikipedia.org/wiki/Concorde', max_depth=.5, node_size_multiplier=2, min_node_distance=20)
fig.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')