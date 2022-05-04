import os
import random
import re
import sys
from matplotlib.pyplot import flag
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    corpus_size,page_size = len(corpus), len(corpus[page])
    tmp_distribution = {}
    if page_size == 0:
        for p in corpus.keys():
            tmp_distribution[p] = 1/corpus_size
        return tmp_distribution
    else:
        for p in corpus.keys():
            tmp_distribution[p] = (1 - damping_factor) / corpus_size
        for p in corpus[page]:
            tmp_distribution[p] += damping_factor / page_size
        return tmp_distribution
        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict.fromkeys(corpus, 0)
    keys = list(corpus.keys())
    tmp_page = random.choice(list(corpus.keys()))
    pagerank[tmp_page] += 1
    for i in range(n -1):
        tmp_model = transition_model(corpus, tmp_page, damping_factor)
        next_page = np.random.choice(a = list(tmp_model.keys()), size= 1, p = list(tmp_model.values()))[0]
        pagerank[next_page] += 1
        tmp_page = next_page
    for page in keys:
        pagerank[page] /= n
    print(f"sample check : {sum(pagerank.values())}")
    return pagerank
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = dict.fromkeys(corpus, 1/N)
    num_links = {p: len(corpus[p]) for p in corpus.keys()}
    flag = True
    c = (1 - damping_factor) / N
    while flag:
        flag = False
        next_rank = dict.fromkeys(corpus, c)
        for p in corpus.keys():
            for i in corpus.keys():
                if p in corpus[i]:
                    next_rank[p] += damping_factor * pagerank[i] / num_links[i] 
            if abs(next_rank[p] - pagerank[p]) > 1e-3:
                flag = True
        for p in pagerank.keys():
            pagerank[p] = next_rank[p]
    print(f"iterate check : {sum(pagerank.values())}")
    return pagerank


if __name__ == "__main__":
    main()
