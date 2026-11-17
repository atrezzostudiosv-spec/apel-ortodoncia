"""Build the APEL V2 private static preview from the verified handoff."""
import argparse
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import shutil
import tempfile

from bs4 import BeautifulSoup
from PIL import Image, ImageOps

from labels import LANGUAGES, TITLES, UI, localize

CODE = Path(__file__).resolve().parent
PILOT = ("portal", "o-home", "d-home")
PHONE = "+503 2243-9979"
PHONE_LINK = "tel:+50322439979"
SECTION_CSS = {"o-home": ["secciones/ats3.css"], "d-home": ["secciones/ats2.css"]}
ATZ_FILES = {
    "ATZ-PGT-002": "page-transitions", "ATZ-NAV-001": "navegacion",
    "ATZ-SEC-004": "secciones", "ATZ-SEC-007": "secciones",
}

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def markup(value):
    return escape(str(value), quote=True)

def public_review_text(text):
    if "Brident" not in text:
        return text
    approved_cuts = (
        " Y una vez que el diente problemático haya sido extraído, Brident",
        " And once the problem tooth has been extracted, Brident",
        " Und sobald der Problemzahn extrahiert wurde, bietet Brident",
    )
    for cut in approved_cuts:
        if cut in text:
            return text.split(cut, 1)[0]
    raise ValueError("Unreviewed legacy reference to Brident")


class Site:
    def __init__(self, package, root, fonts, prefix, public_review=False):
        self.package = package
        self.root = root
        self.fonts = fonts
        self.prefix = prefix
        self.public_review = public_review
        self.editorial = package / "qa/v2-editorial"
        self.evidence = package / "qa/v2-preflight"
        self.pages = read_json(self.editorial / "master-es.json")
        self.plan = read_json(self.editorial / "visual-plan.json")
        self.translations = read_json(self.editorial / "translations-draft.json")["entries"]
        self.atz = {entry["id"]: entry for entry in read_json(self.evidence / "component-provenance.json")}

    def path(self, page_id, lang):
        return self.prefix + self.pages[page_id]["route"][lang]

    def asset(self, path):
        return self.prefix + "/assets/" + path

    def title(self, page_id, lang):
        return markup(localize(TITLES[page_id], lang))

    def text(self, label, lang):
        return markup(localize(UI[label], lang))

    def localized_block(self, es, lang):
        if lang == "es" or es in {"APEL", "APEL Dental", "APEL Ortodoncia", "Apel Ortodoncia"}:
            text = es
        else:
            if not self.translations.get(es, {}).get(lang):
                raise ValueError("Missing translation for a source block")
            text = self.translations[es][lang]
        return public_review_text(text) if self.public_review else text

    def review_notice(self, lang):
        key = "review_public" if self.public_review else "review"
        return self.text(key, lang)

    def photo_url(self, name):
        extension = Path(self.plan["assets"][name]["file"]).suffix.lower()
        return self.asset(f"media/{name}{'.png' if extension == '.png' else '.webp'}")

    def img(self, name, lang, eager=False):
        entry = self.plan["assets"][name]
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        focus = f"--desktop-focus:{entry['desktop_focus']};--mobile-focus:{entry['mobile_focus']}"
        return (f'<img src="{self.photo_url(name)}" alt="{markup(entry["alt"][lang])}" '
                f'width="{entry["width"]}" height="{entry["height"]}" style="{focus}" {load}>')

    def link(self, page_id, lang, label=None, attributes=""):
        label = self.title(page_id, lang) if label is None else label
        return f'<a href="{self.path(page_id, lang)}" {attributes}>{label}</a>'

    def link_list(self, targets, lang):
        links = "".join(f"<li>{self.link(target, lang, self.title(target, lang) + '<span aria-hidden=true>↗</span>')}</li>" for target in targets)
        return f'<ul class="link-list">{links}</ul>'

    def locales(self, page_id, lang):
        options = "".join(self.link(page_id, candidate, candidate.upper(),
                            f'hreflang="{candidate}" lang="{candidate}"' + (' aria-current="page"' if candidate == lang else ""))
                          for candidate in LANGUAGES)
        return f'<nav class="locale" aria-label="{self.text("language", lang)}">{options}</nav>'

    def original(self, component):
        family = ATZ_FILES[component]
        fragment = self.evidence / "exports" / component / "atrezzo" / "components" / family / f"{component}.html"
        return BeautifulSoup(fragment.read_text(encoding="utf-8"), "html.parser")

    def prepare_assets(self):
        assets = self.root / "assets"
        assets.mkdir()
        shutil.copy2(CODE / "app.js", assets / "app.js")
        shutil.copy2(CODE / "style.css", assets / "style.css")
        shutil.copytree(self.fonts, assets / "fonts")
        for component in ATZ_FILES:
            record = self.atz[component]
            for path, hashes in record["files"].items():
                src = self.evidence / "exports" / component / "atrezzo" / path
                if digest(src) != hashes["sha256"]:
                    raise ValueError(f"Invalid ATREZZO byte hash: {path}")
                target = assets / "library" / Path(path).relative_to("components")
                if src.suffix in {".css", ".js"}:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, target)
        media = assets / "media"
        media.mkdir()
        for name, item in self.plan["assets"].items():
            src = self.package / "source-private/APEL-material-redisenio" / item["file"]
            if digest(src) != item["sha256"]:
                raise ValueError(f"Invalid media hash: {name}")
            if src.suffix.lower() == ".png":
                shutil.copy2(src, media / f"{name}.png")
            else:
                with Image.open(src) as captured:
                    photo = ImageOps.exif_transpose(captured).convert("RGB")
                    photo.save(media / f"{name}.webp", quality=85, method=5)

    def portal(self, lang):
        items = []
        for unit, name in (("d", "Dental"), ("o", self.text("unit_o", lang))):
            label = (f'{self.img(unit + "-logo", lang, eager=True)}<span class="portal-title">{name}</span>'
                     f'<span class="portal-action">{self.text("open", lang)} <span aria-hidden="true">↗</span></span>')
            items.append(self.link(unit + "-home", lang, label, 'data-atz-link data-atz-effect="split"'))
        return (
            f'<header class="portal-top">{self.locales("portal", lang)}</header>'
            f'<main id="content" class="portal-grid" aria-label="{self.title("portal", lang)}">{"".join(items)}</main>'
        )

    def unit_destinations(self, unit):
        if unit == "d":
            return ("d-tratamientos", "d-especialistas", "d-clinica"), ("d-room", "d-veronica", "d-room")
        return ("o-tratamientos", "o-doctores", "o-instalaciones"), ("o-andre", "o-pair", "o-room")

    def shell_header(self, page_id, lang, unit):
        contact = "d-citas" if unit == "d" else "o-contacto"
        other = "o-home" if unit == "d" else "d-home"
        destinations, photos = self.unit_destinations(unit)
        fragment = self.original("ATZ-NAV-001")
        host = fragment.select_one("[data-atz-id]")
        host["class"].append("unit-header")
        # These are the three demo destination scenes, replaced by site documents.
        for section in host.select(".atz-nav-intro,.atz-nav-anchor"):
            section.decompose()
        logo = host.select_one(".atz-nav-logo")
        logo["href"] = self.path(unit + "-home", lang)
        logo.clear()
        logo.append(BeautifulSoup(self.img(unit + "-logo", lang, eager=True), "html.parser"))
        fallback = host.select_one(".atz-nav-fallback")
        fallback["aria-label"] = localize(UI["nav"], lang)
        for anchor, destination in zip(fallback.select("a"), destinations, strict=True):
            anchor["href"] = self.path(destination, lang)
            anchor.string = localize(TITLES[destination], lang)
        trigger = host.select_one("[data-azn1-menu-trigger]")
        trigger["aria-label"] = localize(UI["menu"], lang)
        trigger.find_all("span", recursive=False)[-1].string = localize(UI["menu"], lang)
        dialog = host.select_one("[data-azn1-menu]")
        dialog["class"].append("apel-menu")
        dialog["aria-label"] = localize(UI["nav"], lang)
        dialog.select_one(".atz-nav-dialog-head strong").string = localize(TITLES[unit + "-home"], lang)
        close = dialog.select_one("[data-azn1-menu-close]")
        close["aria-label"] = localize(UI["close"], lang)
        close.contents[0].replace_with(localize(UI["close"], lang) + " ")
        dialog.select_one(".atz-nav-dialog-links-wrap > span").clear()
        dialog.select_one(".atz-nav-dialog-foot").clear()
        dialog.select_one(".atz-nav-photo-caption").clear()
        for anchor, destination in zip(dialog.select("[data-azn1-menu-link]"), destinations, strict=True):
            anchor["href"] = self.path(destination, lang)
            anchor.strong.string = localize(TITLES[destination], lang)
        for item, name in zip(dialog.select("[data-azn1-menu-photo]"), photos, strict=True):
            item.append(BeautifulSoup(self.img(name, lang), "html.parser"))
        return (
            f'<header><div class="site-utility">{self.link("portal", lang, self.text("portal", lang), "class=portal-back")}'
            f'{self.link(other, lang)}{self.locales(page_id, lang)}'
            f'{self.link(contact, lang, self.text("contact", lang))}</div>{host}</header>'
        )

    def footer(self, lang, unit):
        destinations, _ = self.unit_destinations(unit)
        legal = unit + "-privacidad"
        other = "d-home" if unit == "o" else "o-home"
        extra = ["o-pacientes", "o-galeria"] if unit == "o" else ["d-citas", "d-galeria"]
        links = "".join(self.link(target, lang) for target in destinations + tuple(extra))
        return (
            f'<footer class="foot"><div class="wrap foot-grid"><div>'
            f'{self.link(unit + "-home", lang, self.img(unit + "-logo", lang))}'
            f'<a href="{PHONE_LINK}">{PHONE}</a></div><div>{links}</div>'
            f'<div>{self.link(legal, lang)}{self.link(other, lang)}'
            f'{self.link("portal", lang, self.text("portal", lang))}</div></div></footer>'
        )

    def narrative(self, lang, unit):
        if unit == "o":
            root = self.original("ATZ-SEC-007").select_one("[data-atz-id]")
            root["aria-label"] = localize(TITLES["o-home"], lang)
            for chapter, photo, destination in zip(root.select(".ss03__chapter"),
                    ("o-andre", "o-office", "o-room"), ("o-tratamientos", "o-andre", "o-instalaciones"), strict=True):
                tag = chapter.img
                asset = self.plan["assets"][photo]
                tag["src"], tag["alt"] = self.photo_url(photo), asset["alt"][lang]
                tag["width"], tag["height"] = asset["width"], asset["height"]
                chapter["style"] = chapter["style"].split("--focus:")[0] + "--focus:" + asset["desktop_focus"]
                heading = chapter.h2
                words = localize(TITLES[destination], lang).split()
                if len(words) >= 3:
                    first, middle, last = words[0], " ".join(words[1:-1]), words[-1]
                else:
                    first, middle, last = words[0], words[-1] if len(words) > 1 else "", ""
                source_text = BeautifulSoup(f"{markup(first)}<br><em>{markup(middle)}</em><br>{markup(last)}", "html.parser")
                heading.clear()
                heading.append(source_text)
                chapter.select_one(".ss03__text").string = asset["alt"][lang]
                chapter.select_one(".ss03__kicker").string = localize(UI["unit_o"], lang)
                chapter.select_one(".ss03__indicator").string = localize(UI["scroll"], lang)
                chapter.a["href"] = self.path(destination, lang)
                chapter.a.string = localize(UI["open"], lang)
            return str(root)
        root = self.original("ATZ-SEC-004").select_one("[data-atz-id]")
        root.section["aria-label"] = localize(TITLES["d-home"], lang)
        for pane, photo, destination in zip(root.select(".ats2-handoff-pane"),
                ("d-veronica-model", "d-room"), ("d-especialistas", "d-clinica"), strict=True):
            asset = self.plan["assets"][photo]
            pane.img["src"], pane.img["alt"] = self.photo_url(photo), asset["alt"][lang]
            pane.img["width"], pane.img["height"] = asset["width"], asset["height"]
            pane.img["style"] = "object-position:" + asset["desktop_focus"]
            words = localize(TITLES[destination], lang).split(maxsplit=1)
            pane.h2.clear()
            pane.h2.append(BeautifulSoup("<br>".join(map(markup, words)), "html.parser"))
            pane.select_one(".ats2-scene-kicker").string = localize(TITLES["d-home"], lang)
            pane.p.string = asset["alt"][lang]
        return str(root) + f'<div class="wrap inline-content">{self.link_list(("d-especialistas", "d-clinica"), lang)}</div>'

    def blocks(self, page_id, lang):
        content = []
        for section in self.pages[page_id]["sections"]:
            blocks = []
            for part in section["blocks"]:
                tag = part["tag"]
                label = markup(self.localized_block(part["es"], lang))
                if part["target_id"] and part["target_id"] != page_id:
                    label = self.link(part["target_id"], lang, label)
                trace = markup(" ".join(part["block_ids"]))
                if tag.startswith("h"):
                    tag = "h3"
                elif tag not in {"p", "address"}:
                    tag = "p"
                blocks.append(f'<{tag} class="source-block" data-apel-block="{trace}">{label}</{tag}>')
            identity = f'id="{section["id"]}" data-apel-section="{section["id"]}"'
            if page_id == "o-faq" and len(blocks) > 1 and section["blocks"][0]["tag"].startswith("h"):
                question = section["blocks"][0]
                label = markup(self.localized_block(question["es"], lang))
                trace = markup(" ".join(question["block_ids"]))
                content.append(f'<details class="faq" {identity}><summary data-apel-block="{trace}">{label}</summary>{"".join(blocks[1:])}</details>')
            else:
                content.append(f'<div {identity}>{"".join(blocks)}</div>')
        return "".join(content)

    def home(self, page_id, lang, unit):
        dental = unit == "d"
        contact = "d-citas" if dental else "o-contacto"
        portrait = self.img("d-veronica" if dental else "o-pair", lang, eager=True)
        if dental:
            portrait = f"<figure>{portrait}</figure>"
        copy = (f'<div class="copy"><h1>{self.title(page_id, lang)}</h1><p class="motto">{self.text("motto", lang)}</p>'
                f'<div class="action-row">{self.link(contact, lang, attributes="class=button")}</div></div>')
        hero = f'<section class="home-{unit}-hero">{copy}{portrait}</section>'
        treatment = unit + "-tratamientos"
        treatments = tuple(key for key, data in self.pages.items() if data["family"] == "treatment" and key[0] == unit)
        service = (f'<section class="wrap section editorial-index"><h2>{self.title(treatment, lang)}</h2>'
                   f'{self.link_list((treatment, *treatments), lang)}</section>')
        patients = ("d-especialistas", "d-galeria", "d-contacto") if dental else (
                    "o-pacientes", "o-inicio-tratamiento", "o-faq", "o-sos", "o-ligas")
        body = (
            f'<section class="soft section"><div class="wrap editorial-index"><div class="reader">'
            f'<p class="notice">{self.review_notice(lang)}</p>{self.blocks(page_id, lang)}</div>'
            f'<div>{self.link_list(patients, lang)}{self.guide(lang, unit)}</div></div></section>'
        )
        final = (f'<section class="wrap section"><h2>{self.title(contact, lang)}</h2><p class="inline-content">'
                 f'<a class="button" href="{PHONE_LINK}">{self.text("call", lang)} · {PHONE}</a></p>'
                 f'<p>{self.text("phone_review", lang)}</p></section>')
        middle = self.narrative(lang, unit) + service if dental else service + self.narrative(lang, unit)
        return hero + middle + body + final

    def guide(self, lang, unit):
        guide_routes = (
            ("o-tratamientos", "o-doctores", "o-inicio-tratamiento", "o-faq", "o-sos", "o-ligas", "o-contacto", "d-home")
            if unit == "o" else
            ("d-tratamientos", "d-especialistas", "d-citas", "d-clinica", "d-contacto", "o-home")
        )
        return (f'<details class="guide"><summary>{self.text("guide", lang)}</summary>'
                f'{self.link_list(guide_routes, lang)}</details>')

    def gallery(self, photos, lang):
        shots = "".join(
            f'<figure><a data-gallery-photo href="{self.photo_url(photo)}">{self.img(photo, lang)}</a>'
            f'<figcaption>{markup(self.plan["assets"][photo]["alt"][lang])}</figcaption></figure>'
            for photo in photos
        )
        return (f'<div data-gallery class="picture-list">{shots}<dialog class="gallery-dialog">'
                f'<form method="dialog"><button>{self.text("close", lang)}</button></form>'
                '<img alt=""></dialog></div>')

    def studio(self, lang):
        colors = (("neutral", "#696969"), ("purple", "#8f4d9f"), ("green", "#5b834d"), ("blue", "#416b9a"))
        palette = "".join(f'<option value="{value}">{self.text(color, lang)}</option>' for color, value in colors)
        positions = []
        regions = []
        for index in range(12):
            x, y = 25 + (index % 6) * 42, 25 + (index // 6) * 78
            regions.append(f'<rect x="{x}" y="{y}" width="32" height="52" rx="12" fill="#f7f7f7" stroke="#696969"/>'
                           f'<circle data-piece cx="{x + 16}" cy="{y + 27}" r="7" fill="{colors[0][1]}"/>')
            positions.append(f'<option value="{index}">{index + 1}</option>')
        return (f'<fieldset class="studio-fieldset" data-studio><legend>{self.text("braces_demo", lang)}</legend>'
                f'<svg class="studio-diagram" viewBox="0 0 300 175" xmlns="http://www.w3.org/2000/svg"'
                f' role="img" aria-label="{self.text("braces_demo", lang)}">{"".join(regions)}</svg>'
                f'<div class="studio-controls"><label>{self.text("region", lang)}<select data-piece-select>{"".join(positions)}</select></label>'
                f'<label>{self.text("colour", lang)}<select data-colour-select>{palette}</select></label></div>'
                f'<div class="studio-controls"><button type="button" data-apply-all>{self.text("apply_all", lang)}</button>'
                f'<button type="button" data-reset>{self.text("reset", lang)}</button>'
                f'<button type="button" data-export>{self.text("export", lang)}</button></div></fieldset>')

    def interior(self, page_id, lang, unit):
        data = self.pages[page_id]
        family = data["family"]
        photos = self.plan["pages"][page_id]["scenes"][0]["photos"]
        hero = self.img(photos[0], lang, eager=True) if photos and family != "gallery" else ""
        heading = f'<section class="wrap page-head"><div><h1>{self.title(page_id, lang)}</h1></div>{hero}</section>'
        if family == "legal":
            return heading + f'<div class="wrap section"><p class="notice">{self.text("legal", lang)}</p></div>'
        body = self.blocks(page_id, lang)
        if family == "gallery":
            body = self.gallery(photos, lang) + body
        if page_id == "o-pacientes":
            body += self.guide(lang, unit)
        if family == "studio":
            body = self.studio(lang) + body
        if family == "people":
            people = ("o-andre", "d-veronica", "o-staff") if unit == "o" else (
                "d-veronica", "o-andre", "d-minerva", "d-david", "d-jaime", "d-mirna")
            body = self.link_list(tuple(target for target in people if target != page_id), lang) + body
        if family == "catalog":
            body = self.link_list(tuple(key for key, info in self.pages.items()
                                       if info["family"] == "treatment" and key[0] == unit), lang) + body
        if family == "clinic":
            locations = ("o-filosofia", "o-caracteristicas", "o-instalaciones", "o-galeria") if unit == "o" else ("d-clinica", "d-galeria")
            body += self.link_list(tuple(target for target in locations if target != page_id), lang)
        if family == "contact":
            body = (f'<p><a class="button" href="{PHONE_LINK}">{self.text("call", lang)} · {PHONE}</a></p>'
                    f'<p>{self.text("phone_review", lang)}</p>' + body)
        topic_links = []
        for section in data["sections"]:
            first = section["blocks"][0]
            if not first["tag"].startswith("h"):
                continue
            label = markup(self.localized_block(first["es"], lang))
            topic_links.append(f'<li><a href="#{section["id"]}">{label}</a></li>')
        toc = (f'<nav class="toc" aria-label="{self.text("topics", lang)}"><h3>{self.text("topics", lang)}</h3>'
               f'<ul>{"".join(topic_links)}</ul></nav>') if len(topic_links) > 1 else ""
        return (heading + f'<section class="wrap section {"article-layout" if toc else ""}">{toc}'
                f'<div class="{"reader" if family != "gallery" else ""}"><p class="notice">{self.review_notice(lang)}</p>{body}</div></section>')

    def render(self, page_id, lang):
        portal = page_id == "portal"
        unit = page_id[0]
        styles = ["page-transitions/atrezzo-transitions.css"]
        if not portal:
            styles.append("navegacion/ATZ-NAV-001.css")
        styles.extend(SECTION_CSS.get(page_id, []))
        css = "".join(f'<link rel="stylesheet" href="{self.asset("library/" + name)}">' for name in styles)
        hreflang = "".join(f'<link rel="alternate" hreflang="{other}" href="{self.path(page_id, other)}">'
                           for other in LANGUAGES)
        body = self.portal(lang)
        if not portal:
            main = self.home(page_id, lang, unit) if page_id.endswith("-home") else self.interior(page_id, lang, unit)
            body = (f'<a class="skip" href="#content">{self.text("skip", lang)}</a>'
                    f'{self.shell_header(page_id, lang, unit)}<main id="content" tabindex="-1">{main}</main>{self.footer(lang, unit)}')
        return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{self.title(page_id, lang)}</title>
<meta name="description" content="{self.title(page_id, lang)}">
<link rel="canonical" href="{self.path(page_id, lang)}">
{hreflang}
{css}
<link rel="stylesheet" href="{self.asset("style.css")}">
<script src="{self.asset("library/page-transitions/preflight.js")}"></script>
</head>
<body>
{body}
<script src="{self.asset("library/page-transitions/runtime.js")}"></script>
<script type="module" src="{self.asset("app.js")}"></script>
</body></html>
'''

    def build(self, pilot):
        self.prepare_assets()
        for page_id in PILOT if pilot else self.pages:
            for lang in LANGUAGES:
                relative_url = self.pages[page_id]["route"][lang].strip("/")
                output = self.root / relative_url / "index.html"
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(self.render(page_id, lang), encoding="utf-8")
        for lang in LANGUAGES:
            parent = self.root if lang == "es" else self.root / lang
            parent.mkdir(exist_ok=True)
            title = self.text("not_found", lang)
            (parent / "404.html").write_text(
                f'<!doctype html><html lang="{lang}"><meta charset="utf-8"><meta name="robots" content="noindex">'
                f'<title>{title}</title><h1>{title}</h1>{self.link("portal", lang, self.text("portal", lang))}</html>',
                encoding="utf-8",
            )

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--fonts", required=True, type=Path)
    parser.add_argument("--prefix", default="")
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--public-review", action="store_true", help="Use the authorized public-review notices and corrections.")
    args = parser.parse_args()
    package = args.package.resolve()
    output = args.output.resolve()
    forbidden = (package / "source-private", package / "content-master", CODE.parent)
    if any(place == output or place in output.parents or output in place.parents for place in forbidden):
        parser.error("Place output outside source trees and Git.")
    if args.prefix and (not args.prefix.startswith("/") or args.prefix.endswith("/") or ".." in args.prefix.split("/")):
        parser.error("Prefix must start with / and cannot end with /.")
    if output.exists():
        parser.error("Choose a new output directory.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix="apel-v2-build-") as staging:
        site = Site(package, Path(staging), args.fonts, args.prefix, args.public_review)
        site.build(args.pilot)
        Path(staging).rename(output)
    print(f"{9 if args.pilot else 141} routes built at {output}")

if __name__ == "__main__":
    main()
