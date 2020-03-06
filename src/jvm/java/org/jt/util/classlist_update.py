#!/usr/bin/env python3

# Needs installed: beautifulsoup4.

import requests
from bs4 import BeautifulSoup

urls = {7: "https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html",
        8: "https://docs.oracle.com/javase/8/docs/api/allclasses-frame.html",
        9: "https://docs.oracle.com/javase/9/docs/api/allclasses-frame.html",
       10: "https://docs.oracle.com/javase/10/docs/api/allclasses-frame.html",
       11: "https://docs.oracle.com/en/java/javase/11/docs/api/allclasses.html",
       12: "https://docs.oracle.com/en/java/javase/11/docs/api/allclasses.html",
       13: "https://docs.oracle.com/en/java/javase/11/docs/api/allclasses.html"}
       #   "https://docs.oracle.com/en/java/javase/12/docs/api/allclasses-index.html"
       #   "https://docs.oracle.com/en/java/javase/13/docs/api/allclasses-index.html"

for major_version, url in urls.items():
    req = requests.get(url)
    req.raise_for_status()
    soup = BeautifulSoup(req.content, "lxml")
    with open("classlist_{}.txt".format(major_version), "wb") as f:
        for anchor in soup.find_all("a"):
            name = anchor["href"].replace(".html", "")
            module, _, name = name.partition("/")
            if "." not in module:
                name = module + "/" + name
                module = ""
            name = name.lstrip("/")
            if "#" in name: continue
            if "." in name: continue
            f.write(name.encode("utf-8"))
            f.write(b"\n")
