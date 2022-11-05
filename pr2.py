import requests
from bs4 import *

def parse_from_page(package):

    PIP_URL = "https://pypi.org/project/"
    page = requests.get(PIP_URL + package)
    if page.status_code != 200: return None
    text = page.text
    links_html = BeautifulSoup(text, "html.parser").find_all('a')
    for link in links_html:
        if link.get('href') is not None \
                and "https://github.com/" in link.get("href") \
                and package.lower() in link.get("href") \
                and (link.get("href")[-len(package) - 1:] == package + "/"
                     or link.get("href")[-len(package):] == package):
            return link.get("href")
    return None


def parse_from_file(link):
    page = requests.get(link)
    if page.status_code != 200: return None
    text = page.text
    links_html = BeautifulSoup(text, "html.parser").find_all('a')
    a = []
    for link in links_html:
        if link.get('href') is not None and ("setup.py" in link.get("href") or "setup.cfg" in link.get("href")):
            a.append(link.get("href"))
    return a


def dependencies(package):
    links = []
    link_1 = parse_from_page(package)
    if link_1 is None: return None
    repeats = link_1.replace("https://github.com/", "")
    link_2 = parse_from_file(link_1)
    if link_2 is None: return None
    for link in link_2:
        links.append(link_1 + link.replace(repeats, "")[1:])
    return links


def packages(page_url):
    page = requests.get(page_url)
    if page.status_code != 200: return None
    text = page.text
    packages_name = set()
    flag = False
    body_fail = BeautifulSoup(text, "html.parser").find_all('tr')
    for line in body_fail:
        if "]" in line.text or line.text is None: flag = False
        if flag:
            counter = 0
            for elem in line.text:
                if elem == " " or elem == "\n": counter += 1
                else: break
            first_index = counter
            if line.text[first_index:].find(" ") != -1:
                last_index = line.text[first_index:].find(" ") + first_index
            elif line.text[first_index:].find(";") != -1:
                last_index = line.text[first_index:].find(";") + first_index
            elif line.text[first_index:].find(">") != -1:
                last_index = line.text[first_index:].find(">") + first_index
            else: last_index = 0
            name = line.text[first_index:last_index].replace(";", "").replace(" ", "").replace('"', "")
            if "\n" in name or name == "": continue
            packages_name.add(name)
        if "install_requires" in line.text or "requires = [" in line.text: flag = True
    return packages_name


def dependencies_print(package, tab):
    urls = dependencies(package)
    if urls is not None:
        for url in urls:
            if url is not None:
                if packages(url) is not None:
                    for name in packages(url):
                        if name is None: continue
                        print(tab * "\t" + package + " -> " + name)
                        dependencies_print(name, tab + 1)

package = input()
print("Digraph " + package + "{")
dependencies_print(package, 1)
print("}")