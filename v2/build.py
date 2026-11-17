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

from composition import DENTAL_CHAPTERS, ORTHO_CHAPTERS, PORTRAITS
from labels import LANGUAGES, TITLES, UI, localize
from navigation import BLOG, DENTAL_DIRECT, DENTAL_ESTHETICS, DENTAL_PEOPLE, ORTHO_CLINIC, ORTHO_TREATMENTS

CODE = Path(__file__).resolve().parent
PILOT = ("portal", "o-home", "d-home")
PHONE = "+503 2243-9979"
PHONE_LINK = "tel:+50322439979"
SECTION_CSS = {"o-home": ["secciones/ats3.css"], "d-home": ["secciones/ats2.css"]}
ATZ_FILES = {
    "ATZ-PGT-002": "page-transitions",
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
        for unit, photo, label in (("d", "d-veronica", "unit_d"), ("o", "o-pair", "unit_o")):
            identity = (
                f'<span class="portal-identity">{self.img(unit + "-logo", lang, eager=True)}'
                f'<span class="portal-title">{self.text(label, lang)}</span>'
                f'<span class="portal-action">{self.text("open", lang)} <span aria-hidden="true">↗</span></span></span>'
            )
            picture = f'<span class="portal-photo">{self.img(photo, lang, eager=True)}</span>'
            items.append(self.link(unit + "-home", lang, picture + identity,
                                   'data-atz-link data-atz-effect="split"'))
        return (
            f'<header class="portal-top">{self.locales("portal", lang)}</header>'
            f'<main id="content" class="portal-grid" aria-label="{self.title("portal", lang)}">{"".join(items)}</main>'
        )

    def primary_navigation(self, page_id, lang, unit):
        def item(target, label=None):
            attributes = 'aria-current="page"' if target == page_id else ""
            return self.link(target, lang, label, attributes)

        def labeled(target, key):
            return item(target, self.text(key, lang))

        def menu_list(targets):
            return "".join(f"<li>{item(target)}</li>" for target in targets)

        def group(key, targets, extra="", wide=False):
            name = self.text(key, lang)
            section = (' aria-label="' + name + '"')
            panel_class = "header-submenu header-submenu-wide" if wide else "header-submenu"
            return (f'<details name="primary-sections" class="header-disclosure"><summary>{name}</summary>'
                    f'<ul class="{panel_class}"{section}>{menu_list(targets)}{extra}</ul></details>')

        if unit == "d":
            esthetics = (
                f'<li class="header-subgroup"><span>{self.text("nav_esthetics", lang)}</span>'
                f'<ul>{menu_list(DENTAL_ESTHETICS)}</ul></li>'
            )
            direct = f'<li>{item("d-ortodoncia")}</li>{esthetics}{menu_list(DENTAL_DIRECT)}'
            navigation = (
                labeled("d-home", "nav_home"),
                labeled("d-clinica", "nav_dental_clinic"),
                group("nav_specialists", ("d-especialistas", *DENTAL_PEOPLE)),
                group("nav_dental_treatments", ("d-tratamientos",), direct, wide=True),
                item("o-home"),
                labeled("d-citas", "nav_appointments"),
            )
        else:
            navigation = (
                labeled("o-home", "nav_home"),
                group("nav_treatments", ORTHO_TREATMENTS),
                group("nav_staff", ("o-doctores", "o-staff")),
                group("nav_clinic", ORTHO_CLINIC),
                item("o-ligas"),
                labeled("o-sos", "nav_sos"),
                labeled("o-faq", "nav_faq"),
                f'<a href="{BLOG}">Blog</a>',
                item("d-home"),
                labeled("o-contacto", "contact"),
            )
        return (f'<nav class="primary-navigation" aria-label="{self.text("nav", lang)}"><ul>'
                + "".join(f"<li>{entry}</li>" for entry in navigation) + "</ul></nav>")

    def shell_header(self, page_id, lang, unit):
        return (
            f'<header class="unit-header unit-header-{unit}"><div class="site-utility">'
            f'{self.link("portal", lang, self.text("portal", lang), "class=portal-back")}'
            f'<a class="review-status" href="#review">{self.text("review_short", lang)}</a>'
            f'{self.locales(page_id, lang)}</div>'
            f'<div class="header-row">{self.link(unit + "-home", lang, self.img(unit + "-logo", lang, eager=True), "class=header-logo")}'
            f'{self.primary_navigation(page_id, lang, unit)}</div></header>'
        )

    def footer(self, lang, unit):
        destinations = (("d-tratamientos", "d-especialistas", "d-clinica") if unit == "d"
                        else ("o-tratamientos", "o-doctores", "o-instalaciones"))
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
        ortho = unit == "o"
        root = self.original("ATZ-SEC-007" if ortho else "ATZ-SEC-004").select_one("[data-atz-id]")
        root["aria-label"] = localize(TITLES[f"{unit}-home"], lang)
        selector = ".ss03__chapter" if ortho else ".ats2-handoff-pane"
        scenes = ORTHO_CHAPTERS if ortho else DENTAL_CHAPTERS
        for frame, (photo, destination, titles, description) in zip(root.select(selector), scenes, strict=True):
            asset = self.plan["assets"][photo]
            frame.img["src"], frame.img["alt"] = self.photo_url(photo), asset["alt"][lang]
            frame.img["width"], frame.img["height"] = asset["width"], asset["height"]
            title = [markup(line) for line in localize(titles, lang)]
            if ortho:
                title[1] = f"<em>{title[1]}</em>"
                frame["style"] = frame["style"].split("--focus:")[0] + "--focus:" + asset["desktop_focus"]
                frame.select_one(".ss03__text").string = localize(description, lang)
                frame.select_one(".ss03__kicker").string = localize(TITLES[destination], lang)
                frame.select_one(".ss03__indicator").string = localize(UI["scroll"], lang)
                frame.a["href"] = self.path(destination, lang)
                frame.a.string = localize(UI["open"], lang)
            else:
                frame.img["style"] = "object-position:" + asset["desktop_focus"]
                frame.select_one(".ats2-scene-kicker").string = localize(TITLES[destination], lang)
                frame.p.string = localize(description, lang)
            frame.h2.clear()
            frame.h2.append(BeautifulSoup("<br>".join(title), "html.parser"))
        return str(root)

    def blocks(self, page_id, lang, sections=None):
        content = []
        for section in self.pages[page_id]["sections"] if sections is None else sections:
            blocks = []
            for part in section["blocks"]:
                tag = part["tag"]
                label = markup(self.localized_block(part["es"], lang))
                if part["target_id"] and part["target_id"] != page_id:
                    label = self.link(part["target_id"], lang, label)
                trace = markup(" ".join(part["block_ids"]))
                date_label = tag.startswith("h") and all(character.isdigit() or character in " -–—" for character in part["es"])
                if date_label:
                    tag = "p"
                elif tag.startswith("h"):
                    tag = "h2" if tag in {"h1", "h2", "h3", "h4"} else "h3"
                elif tag not in {"p", "address"}:
                    tag = "p"
                kind = "source-block source-date" if date_label else "source-block"
                blocks.append(f'<{tag} class="{kind}" data-apel-block="{trace}">{label}</{tag}>')
            identity = f'id="{section["id"]}" data-apel-section="{section["id"]}"'
            if page_id == "o-faq" and len(blocks) > 1 and section["blocks"][0]["tag"].startswith("h"):
                question = section["blocks"][0]
                label = markup(self.localized_block(question["es"], lang))
                trace = markup(" ".join(question["block_ids"]))
                content.append(f'<details class="faq" {identity}><summary data-apel-block="{trace}">{label}</summary>{"".join(blocks[1:])}</details>')
            else:
                content.append(f'<div {identity}>{"".join(blocks)}</div>')
        return "".join(content)

    def care_links(self, lang, unit):
        choices = (
            (("o-concepto", "o-aparatos", "o-alineadores"), ("o-interdisciplinarios", "o-tratamientos"))
            if unit == "o" else (DENTAL_ESTHETICS, ("d-ortodoncia", *DENTAL_DIRECT))
        )
        heads = (
            (self.text("nav_treatments", lang), self.title("o-tratamientos", lang))
            if unit == "o" else (self.text("nav_esthetics", lang), self.text("integrated_care", lang))
        )
        return "".join(f"<div><h3>{heading}</h3>{self.link_list(links, lang)}</div>"
                       for heading, links in zip(heads, choices, strict=True))

    def source_notice(self, lang):
        return f'<p class="notice" id="review">{self.review_notice(lang)}</p>'

    def call(self, lang):
        return f'<a class="button" href="{PHONE_LINK}">{self.text("call", lang)} · {PHONE}</a>'

    def portrait_directory(self, page_id, lang, sections):
        cards = []
        for section in sections:
            target = next((item["target_id"] for item in section["blocks"] if item["target_id"] in PORTRAITS), None)
            source = self.blocks(page_id, lang, [section])
            if not target:
                cards.append(f'<div class="team-context reader">{source}</div>')
                continue
            photo = self.link(target, lang, self.img(PORTRAITS[target], lang))
            cards.append(f'<article class="team-member"><figure>{photo}</figure><div>{source}</div></article>')
        return "".join(cards)

    def ortho_home(self, lang):
        page = "o-home"
        sections = self.pages[page]["sections"]
        return (
            f'<section class="ortho-entry" data-scene="O1"><figure>{self.img("o-room", lang, eager=True)}</figure>'
            f'<div class="wrap ortho-title"><h1>{self.title(page, lang)}</h1><div>'
            f'<p class="motto">{self.text("motto", lang)}</p>'
            f'{self.link("o-contacto", lang, attributes="class=button")}</div></div></section>'
            f'<section class="wrap section ortho-method" data-scene="O2"><div class="reader">'
            f'{self.source_notice(lang)}{self.blocks(page, lang, sections[:4])}</div>'
            f'<div class="method-links">{self.care_links(lang, "o")}</div></section>'
            f'<div data-scene="O3">{self.narrative(lang, "o")}</div>'
            f'<section class="patient-band section" data-scene="O4"><div class="wrap patient-grid">'
            f'<div><h2>{self.title("o-pacientes", lang)}</h2>{self.guide(lang, "o")}</div>'
            f'{self.link_list(("o-inicio-tratamiento", "o-faq", "o-sos", "o-ligas", "o-pacientes"), lang)}'
            f'</div></section>'
            f'<section class="wrap section editorial-close" data-scene="O5"><div>'
            f'<h2>{self.title("o-contacto", lang)}</h2>{self.call(lang)}<p>{self.text("phone_review", lang)}</p></div>'
            f'<div class="reader">{self.blocks(page, lang, sections[4:])}</div></section>'
        )

    def dental_home(self, lang):
        page = "d-home"
        sections = self.pages[page]["sections"]
        context = [sections[0], {**sections[1], "blocks": sections[1]["blocks"][2:]}, sections[2]]
        care, appointment, team_intro = sections[3:6], sections[6:7], sections[7:8]
        hero_content = sections[1]["blocks"][:2]
        hero_heading, hero_intro = hero_content
        headline = markup(self.localized_block(hero_heading["es"], lang))
        introduction = markup(self.localized_block(hero_intro["es"], lang))
        title_trace = markup(" ".join(hero_heading["block_ids"]))
        intro_trace = markup(" ".join(hero_intro["block_ids"]))
        return (
            f'<section class="dental-entry" data-scene="D1"><div class="wrap dental-entry-inner">'
            f'<div><p class="elabel">{self.title(page, lang)}</p>'
            f'<h1 data-apel-block="{title_trace}">{headline}</h1>'
            f'<p class="dental-lead" data-apel-block="{intro_trace}">{introduction}</p>'
            f'<div class="action-row">{self.link("d-citas", lang, attributes="class=button")}'
            f'<a href="#dental-team">{self.title("d-especialistas", lang)}</a></div></div>'
            f'<figure>{self.img("d-veronica", lang, eager=True)}</figure></div></section>'
            f'<div data-scene="D2">{self.narrative(lang, "d")}</div>'
            f'<section class="wrap section dental-care" data-scene="D3"><div class="dental-care-intro">'
            f'<div><h2>{self.title("d-tratamientos", lang)}</h2>{self.link("d-tratamientos", lang)}</div>'
            f'<div class="reader">{self.source_notice(lang)}{self.blocks(page, lang, context)}</div></div>'
            f'<div class="care-columns">{self.care_links(lang, "d")}</div></section>'
            f'<section class="soft section" id="dental-team" data-scene="D4"><div class="wrap"><div class="team-intro reader">'
            f'{self.blocks(page, lang, team_intro)}</div><div class="team-list">'
            f'{self.portrait_directory(page, lang, sections[8:])}</div>'
            f'<div class="action-row team-links">{self.link("d-especialistas", lang)}'
            f'{self.link("d-clinica", lang)}{self.link("d-galeria", lang)}</div></div></section>'
            f'<section class="wrap section editorial-close" data-scene="D5"><div class="reader">'
            f'{self.blocks(page, lang, appointment)}{self.link("d-citas", lang, attributes="class=button")}'
            f'{self.guide(lang, "d")}</div><div class="reader">{self.blocks(page, lang, care)}</div></section>'
        )

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

    def contents(self, page_id, lang):
        items = []
        for section in self.pages[page_id]["sections"]:
            first = section["blocks"][0]
            if not first["tag"].startswith("h"):
                continue
            title = markup(self.localized_block(first["es"], lang))
            items.append(f'<li><a href="#{section["id"]}">{title}</a></li>')
        if len(items) < 2:
            return ""
        label = self.text("topics", lang)
        return f'<nav class="toc" aria-label="{label}"><h2>{label}</h2><ul>{"".join(items)}</ul></nav>'

    def interior(self, page_id, lang, unit):
        family = self.pages[page_id]["family"]
        photos = self.plan["pages"][page_id]["scenes"][0]["photos"]
        title = self.title(page_id, lang)
        contact = "d-citas" if unit == "d" else "o-contacto"
        call = self.call(lang)
        contact_link = self.link(contact, lang, attributes="class=button")
        heading = f'<div class="wrap interior-title"><h1>{title}</h1></div>'
        notice = self.source_notice(lang)
        blocks = self.blocks(page_id, lang)

        if family == "legal":
            return heading + f'<div class="wrap reading-section"><p class="notice" id="review">{self.text("legal", lang)}</p></div>'
        if family == "profile":
            portrait = PORTRAITS.get(page_id) or photos[0]
            header = (f'<div class="profile-cover soft"><div class="wrap profile-cover-inner">'
                      f'<figure>{self.img(portrait, lang, eager=True)}</figure><div><h1>{title}</h1>'
                      f'<div class="action-row">{contact_link}</div></div></div></div>')
            contents = self.contents(page_id, lang)
            return (header + f'<div class="wrap reading-section article-layout profile-history">{contents}'
                    f'<article class="reader">{notice}{blocks}</article></div>')
        if family == "people":
            sections = self.pages[page_id]["sections"]
            entries = self.portrait_directory(page_id, lang, sections)
            if unit == "o":
                entries += self.link_list(tuple(page for page in ("o-doctores", "o-staff", "o-andre", "d-veronica") if page != page_id), lang)
            return (f'<div class="soft">{heading}</div><section class="wrap section">'
                    f'<div class="reader">{notice}</div><div class="team-list">{entries}</div></section>')
        if family == "clinic":
            locations = ("o-filosofia", "o-caracteristicas", "o-instalaciones", "o-galeria") if unit == "o" else ("d-clinica", "d-galeria")
            picture = f'<figure class="clinic-cover">{self.img(photos[0], lang, eager=True)}</figure>' if photos else ""
            details = self.gallery(photos[1:], lang) if len(photos) > 1 else ""
            related = self.link_list(tuple(target for target in locations if target != page_id), lang)
            return (heading + picture + f'<div class="wrap section clinic-reading"><article class="reader">'
                    f'{notice}{blocks}</article><aside>{related}{contact_link}</aside></div>'
                    f'<div class="wrap clinic-extra">{details}</div>')
        if family == "gallery":
            return heading + f'<section class="wrap reading-section">{notice}{self.gallery(photos, lang)}<div class="reader">{blocks}</div></section>'
        if family == "catalog":
            return (f'<div class="soft">{heading}</div><section class="wrap section">'
                    f'<div class="care-columns">{self.care_links(lang, unit)}</div>'
                    f'<article class="reader catalog-source">{notice}{blocks}</article></section>')
        if family == "treatment":
            overview = self.contents(page_id, lang)
            related = (("o-tratamientos", "o-inicio-tratamiento") if unit == "o" else ("d-tratamientos", "d-citas"))
            return (
                f'<div class="treatment-cover"><div class="wrap treatment-cover-inner">'
                f'<div>{self.link(f"{unit}-tratamientos", lang)}<h1>{title}</h1></div>{contact_link}</div></div>'
                f'<div class="wrap reading-section article-layout treatment-reading">'
                f'<aside>{overview}{self.link_list(related, lang)}</aside><article class="reader">{notice}{blocks}</article></div>'
            )
        if family == "contact":
            return (
                f'<div class="soft">{heading}</div><section class="wrap reading-section contact-layout"><div>'
                f'{call}<p class="call-note">{self.text("phone_review", lang)}</p></div>'
                f'<article class="reader">{notice}{blocks}</article></section>'
            )

        tools = self.studio(lang) if family == "studio" else (
            self.guide(lang, unit) if page_id == "o-pacientes" else ""
        )
        immediate = call if page_id in {"o-sos", "o-inicio-tratamiento"} else self.link("o-sos", lang)
        return (
            f'<div class="patient-hero">{heading}</div><section class="wrap reading-section patient-detail">'
            f'<div class="action-row">{immediate}</div>{tools}<article class="reader">{notice}{blocks}</article></section>'
        )

    def render(self, page_id, lang):
        portal = page_id == "portal"
        unit = page_id[0]
        styles = ["page-transitions/atrezzo-transitions.css"]
        styles.extend(SECTION_CSS.get(page_id, []))
        css = "".join(f'<link rel="stylesheet" href="{self.asset("library/" + name)}">' for name in styles)
        hreflang = "".join(f'<link rel="alternate" hreflang="{other}" href="{self.path(page_id, other)}">'
                           for other in LANGUAGES)
        body = self.portal(lang)
        if not portal:
            main = self.ortho_home(lang) if page_id == "o-home" else (
                self.dental_home(lang) if page_id == "d-home" else self.interior(page_id, lang, unit)
            )
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
