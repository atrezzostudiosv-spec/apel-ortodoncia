"""Validate private build routes, original component assets and editorial traces."""
import argparse
from collections import deque
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

from build import ATZ_FILES, LANGUAGES, digest, read_json, public_review_text

def compare(output, package, prefix, public_review=False):
    master = read_json(package / "qa/v2-editorial/master-es.json")
    plan = read_json(package / "qa/v2-editorial/visual-plan.json")
    translations = read_json(package / "qa/v2-editorial/translations-draft.json")["entries"]
    pinned = read_json(package / "qa/v2-preflight/component-provenance.json")
    routes = {prefix + row["route"][lang]: (page, lang) for page, row in master.items() for lang in LANGUAGES}
    expected_routes = 3 * len(master)
    assert len(routes) == expected_routes
    errors = []
    graph = {}

    def record(condition, message):
        if not condition:
            errors.append(message)

    for route, (page, lang) in routes.items():
        path = output / route.removeprefix(prefix).strip("/") / "index.html"
        if not path.is_file():
            errors.append(f"{route}: missing page")
            continue
        doc = BeautifulSoup(path.read_bytes(), "html.parser")
        record(doc.html.get("lang") == lang, f"{route}: wrong html lang")
        record(doc.select_one("link[rel=canonical]")["href"] == route, f"{route}: wrong canonical")
        hreflang = {tag["hreflang"]: tag["href"] for tag in doc.select("link[hreflang]")}
        record(hreflang == {language: prefix + url for language, url in master[page]["route"].items()},
               f"{route}: wrong alternates")
        record("noindex" in doc.select_one("meta[name=robots]")["content"], f"{route}: indexing")
        observed = {block_id: node for node in doc.select("[data-apel-block]")
                    for block_id in node["data-apel-block"].split()}
        expected = {block_id for sec in master[page]["sections"] for block in sec["blocks"]
                    for block_id in block["block_ids"]}
        if page != "portal":
            record(expected == set(observed), f"{route}: missing or extra editorial block IDs")
            for section in master[page]["sections"]:
                for block in section["blocks"]:
                    es = block["es"]
                    text = es if lang == "es" or es in {"APEL", "APEL Dental", "APEL Ortodoncia", "Apel Ortodoncia"} else translations[es][lang]
                    if public_review:
                        text = public_review_text(text)
                    for block_id in block["block_ids"]:
                        node = observed.get(block_id)
                        record(node is not None and node.get_text(" ", strip=True) == text,
                               f"{route}: source text mismatch in {block_id}")
        links = set()
        for tag in doc.select("a[href],link[href],script[src],img[src]"):
            ref = tag.get("href", tag.get("src"))
            url = urlsplit(ref)
            if url.scheme or not url.path:
                continue
            resolved = unquote(url.path)
            if resolved in routes:
                if tag.name == "a":
                    links.add(resolved)
                continue
            in_prefix = resolved.startswith(prefix + "/")
            relative = resolved.removeprefix(prefix).lstrip("/")
            asset = (output / relative).resolve()
            record(in_prefix and output in asset.parents and asset.is_file(), f"{route}: broken reference {ref}")
        graph[route] = links

    for lang in LANGUAGES:
        start = prefix + master["portal"]["route"][lang]
        reached = set()
        queue = deque([start])
        while queue:
            route = queue.popleft()
            if route in reached or routes[route][1] != lang:
                continue
            reached.add(route)
            queue.extend(graph.get(route, ()))
        record(len(reached) == len(master), f"{lang}: orphan routes {sorted(set(route for route, info in routes.items() if info[1] == lang) - reached)}")

    for entry in pinned:
        if entry["id"] not in ATZ_FILES:
            continue
        for source, signature in entry["files"].items():
            path = Path(source)
            if path.suffix in {".js", ".css"}:
                compiled = output / "assets/library" / path.relative_to("components")
                record(compiled.is_file() and digest(compiled) == signature["sha256"],
                       f"Copied ATREZZO file changed: {source}")

    for name, item in plan["assets"].items():
        if Path(item["file"]).suffix.lower() == ".png":
            logo = output / "assets/media" / (name + ".png")
            record(logo.is_file() and digest(logo) == item["sha256"], f"Original logo changed: {name}")
    return {"checked_routes": len(graph), "errors": errors, "status": "fail" if errors else "pass"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prefix", default="")
    parser.add_argument("--public-review", action="store_true")
    args = parser.parse_args()
    result = compare(args.output.resolve(), args.package.resolve(), args.prefix, args.public_review)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result["errors"]))

if __name__ == "__main__":
    main()
