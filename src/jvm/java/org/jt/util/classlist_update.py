#!/usr/bin/env python3

# Info: list all classes loaded by JVM:
# java -Xlog:class+load=info:classloaded.txt
# Info: list all classes loaded by process:
# jcmd 44506 VM.class_hierarchy

# Needs installed: requests, beautifulsoup4.
from pathlib import Path
import requests
from bs4 import BeautifulSoup

urls = {
     7: "https://docs.oracle.com/javase/7/docs/api/allclasses-frame.html",
     8: "https://docs.oracle.com/javase/8/docs/api/allclasses-frame.html",
     9: "https://docs.oracle.com/javase/9/docs/api/allclasses-frame.html",
    10: "https://docs.oracle.com/javase/10/docs/api/allclasses-frame.html",
    11: "https://docs.oracle.com/en/java/javase/11/docs/api/allclasses-index.html",
    12: "https://docs.oracle.com/en/java/javase/12/docs/api/allclasses-index.html",
    13: "https://docs.oracle.com/en/java/javase/13/docs/api/allclasses-index.html",
    14: "https://docs.oracle.com/en/java/javase/14/docs/api/allclasses-index.html",
    15: "https://docs.oracle.com/en/java/javase/15/docs/api/allclasses-index.html",
    16: "https://docs.oracle.com/en/java/javase/16/docs/api/allclasses-index.html",
    17: "https://docs.oracle.com/en/java/javase/17/docs/api/allclasses-index.html",
    18: "https://docs.oracle.com/en/java/javase/18/docs/api/allclasses-index.html",
    19: "https://docs.oracle.com/en/java/javase/19/docs/api/allclasses-index.html",
    20: "https://docs.oracle.com/en/java/javase/20/docs/api/allclasses-index.html",
    21: "https://docs.oracle.com/en/java/javase/21/docs/api/allclasses-index.html",
}

here = Path(__file__).resolve().parent

for major_version, url in urls.items():
    req = requests.get(url)
    req.raise_for_status()
    soup = BeautifulSoup(req.content, "lxml")
    with (here/f"classlist_{major_version}.txt").open("wb") as f:
        elem  = "td"       if major_version < 16 else "div"
        klass = "colFirst" if major_version < 15 else "col-first"
        anchors = (soup.find_all("a")
                   if major_version < 11 else
                   (tag.find("a") for tag in soup.find_all(elem, class_=klass)))
        for anchor in anchors:
            if not anchor: continue
            href = anchor["href"]
            name = href.replace(".html", "")
            module, _, name = name.partition("/")
            if "." not in module:
                name = module + "/" + name
                module = ""
            name = name.lstrip("/")
            if "#" in name: continue
            if "." in name: continue
            f.write(name.encode("utf-8"))
            f.write(b"\n")
