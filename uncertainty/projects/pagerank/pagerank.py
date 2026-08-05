import os
import random
import re
import sys

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
    p_dist = dict()
    for i in corpus:
        p_dist[i] = (1 - damping_factor)/len(corpus)
    
    links = corpus[page]
    if links == set():
        for i in corpus:
            p_dist[i] = 1/len(corpus)
    else:

        for i in links:
            p_dist[i] = damping_factor/len(links) + (1 - damping_factor)/len(corpus)
            
    return p_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    
    """
    proba = dict()
    resultados_das_amostras = []
    opcoes_sites = list(corpus.keys())

    site = random.choice(opcoes_sites)
    resultados_das_amostras.append(site)

    p_dist = transition_model(corpus, site, damping_factor)
    probabilidades = []

    for i in opcoes_sites:
        probabilidades.append(p_dist[i])

    resultado = random.choices(opcoes_sites, weights=probabilidades, k=1)[0]
    
    while len(resultados_das_amostras) < n:
        p_dist = transition_model(corpus, resultado, damping_factor)
        probabilidades = []

        for i in opcoes_sites:
            probabilidades.append(p_dist[i])

        resultado = random.choices(opcoes_sites, weights=probabilidades)[0]
        resultados_das_amostras.append(resultado)
        
    for i in opcoes_sites:
        proba[i] = 0

    for i in resultados_das_amostras:
        proba[i] += 1

    proba_temporaria = proba.copy()

    for i in proba_temporaria:
        proba[i] = proba_temporaria[i]/n

    return proba


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    p_dist = dict()
    links = []
    p_dist_temp_novo = dict()
    cont = 0

    for i in corpus:
        p_dist[i] = 1/len(corpus)

    p_dist_temp_antigo = p_dist.copy()

    converged = False
    while not converged:
        p_dist_temp_novo = {}
        
        for i in corpus:
            for j in corpus:
                if i in corpus[j]:
                    links.append(j)
                if corpus[j] == set():
                    links.append(j)
                    
            pr_novo = (1 - damping_factor)/len(corpus)

            for link in links:
                qntd_link = len(corpus[link])
                if qntd_link == 0:
                    cont += (p_dist[link]/len(corpus)) * damping_factor
                else: 
                    cont += (p_dist[link]/len(corpus[link])) * damping_factor
            p_dist_temp_novo[i] = pr_novo + cont
            cont = 0
            links = []

        converged = True
        for i in p_dist:
            if abs(p_dist_temp_antigo[i] - p_dist_temp_novo[i]) >= 0.001: 
                converged = False

        p_dist_temp_antigo = p_dist_temp_novo.copy()
        for i in p_dist:
            p_dist[i] = p_dist_temp_novo[i]

    return p_dist


if __name__ == "__main__":
    main()
    
