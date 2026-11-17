from pathlib import Path
import json,csv,html,re,shutil
R=Path(__file__).resolve().parents[1]; D=R/'dist'; P=json.loads((R/'data/pages.json').read_text()); by={p['id']:p for p in P}; C={r[0]:r[1:] for r in csv.reader((R/'data/copy.tsv').open(),delimiter='\t')}; langs=['es','en','de']; E=html.escape; CONTACT=json.loads((R/'data/contact.json').read_text())
T={
'skip':['Saltar al contenido','Skip to content','Zum Inhalt springen'],'book':['Citas','Appointments','Termine'],'menu':['Menú','Menu','Menü'],'close':['Cerrar','Close','Schließen'],'explore':['Explorar','Explore','Entdecken'],'read':['Ver detalles','View details','Details ansehen'],'team':['Conoce al equipo','Meet the team','Unser Team'],'units':['Dos unidades, una visión','Two practices, one vision','Zwei Praxisbereiche, eine Vision'],'unitdesc':['Encuentra el área de atención que necesitas.','Find the area of care you need.','Finden Sie den passenden Behandlungsbereich.'],'doctors':['Los Doctores Apel','The Apel doctors','Die Dres. Apel'],'journey':['Una trayectoria compartida','A shared professional journey','Ein gemeinsamer beruflicher Weg'],'care':['Atención al paciente','Patient care','Patientenbetreuung'],'services':['Tratamientos','Treatments','Behandlungen'],'related':['También te puede interesar','Related information','Weitere Informationen'],'information':['Información del tratamiento','Treatment information','Behandlungsinformationen'],'source':['Detalles del archivo original (revisión clínica pendiente)','Details from original Spanish source (clinical review pending)','Details aus der spanischen Originalquelle (fachliche Prüfung ausstehend)'],'cv':['Trayectoria y formación — archivo original','Career and education — original Spanish source','Werdegang und Ausbildung — spanische Originalquelle'],'draft':['Traducción resumida para maqueta; el detalle original en español se conserva debajo.','Draft summary translation; original Spanish detail is preserved below.','Zusammenfassender Übersetzungsentwurf; spanische Originaldetails stehen unten.'],'phone':['Llamar a la clínica','Call the clinic','Praxis anrufen'],'whatsapp':['WhatsApp — pendiente de confirmación','WhatsApp — awaiting confirmation','WhatsApp — Bestätigung ausstehend'],'help':['Guía de navegación','Navigation guide','Navigationshilfe'],'guideq':['¿Qué estás buscando?','What are you looking for?','Wonach suchen Sie?'],'back':['Volver','Back','Zurück'],'select':['Selecciona una liga','Select an elastic','Gummiring auswählen'],'apply':['Aplicar a todas','Apply to all','Auf alle anwenden'],'reset':['Restablecer','Reset','Zurücksetzen'],'download':['Descargar ilustración','Download illustration','Zeichnung herunterladen'],'color':['Color','Colour','Farbe'],'region':['Liga','Elastic','Gummiring'],'demo':['Paleta de demostración · 16 regiones esquemáticas','Demo palette · 16 schematic regions','Demo-Farbpalette · 16 schematische Bereiche'],'nojs':['Activa JavaScript para utilizar la herramienta.','Enable JavaScript to use the tool.','Aktivieren Sie JavaScript für dieses Werkzeug.'],'clinical':['Información histórica pendiente de revisión clínica. No sustituye una consulta.','Historical information awaiting clinical review. Not a substitute for consultation.','Historische Informationen, fachliche Prüfung ausstehend. Kein Ersatz für eine Beratung.'],'address':['Dirección y horarios pendientes de confirmación.','Address and opening hours awaiting confirmation.','Adresse und Öffnungszeiten müssen bestätigt werden.'],'original':['Fotografía original de APEL','Original APEL photograph','Originalfoto von APEL'],'preview':['Vista previa de diseño · No es el sitio oficial','Design preview · Not the official website','Designvorschau · Keine offizielle Website'],'legal':['Información legal pendiente de validación.','Legal information awaiting approval.','Rechtliche Informationen müssen geprüft werden.'],'location':['San Salvador, El Salvador','San Salvador, El Salvador','San Salvador, El Salvador'],'next':['Siguiente imagen','Next image','Nächstes Bild'],'prev':['Imagen anterior','Previous image','Vorheriges Bild'],'navigate':['Navegar por APEL','Explore APEL','APEL entdecken'],'homeLabel':['Inicio','Home','Startseite'],'toc':['En esta página','On this page','Auf dieser Seite'],'contactInfo':['Teléfono publicado en el sitio original; verificar vigencia antes del lanzamiento.','Telephone published on the original site; confirm before launch.','Telefonnummer der ursprünglichen Website; vor Veröffentlichung bestätigen.'],'faq1':['¿Cuánto dura el tratamiento?','How long does treatment take?','Wie lange dauert die Behandlung?'],'faq2':['¿Cuánto cuesta?','How much does it cost?','Was kostet die Behandlung?'],'faq3':['¿A qué edad se puede iniciar?','At what age can treatment start?','In welchem Alter kann die Behandlung beginnen?'],'faq4':['¿Por qué es importante la posición dental?','Why does tooth position matter?','Warum ist die Zahnstellung wichtig?'],'faqA1':['Depende de la situación de los dientes y huesos y del plan individual. La clínica explica la duración estimada tras el diagnóstico.','It depends on the position of teeth and bones and the individual plan. The clinic explains the estimated duration after diagnosis.','Sie hängt von der Zahn- und Kieferstellung sowie vom individuellen Plan ab. Die Praxis erläutert die voraussichtliche Dauer nach der Diagnostik.'],'faqA2':['El costo depende de la complejidad y del tipo de aparato. Consulta al equipo para conocer tu presupuesto.','Cost depends on complexity and appliance type. Ask the team for your estimate.','Die Kosten hängen von Komplexität und Apparatur ab. Fragen Sie das Team nach Ihrem Kostenvoranschlag.'],'faqA3':['La valoración individual permite determinar cuándo conviene iniciar el tratamiento.','An individual assessment helps determine when treatment should begin.','Eine individuelle Untersuchung hilft, den geeigneten Behandlungsbeginn zu bestimmen.'],'faqA4':['La posición de los dientes y la mordida forman parte de la valoración funcional y estética.','Tooth position and bite are part of functional and aesthetic assessment.','Zahnstellung und Biss gehören zur funktionellen und ästhetischen Beurteilung.'],'sos1':['Brackets sueltos','Loose brackets','Lose Brackets'],'sos2':['Alambre suelto o que molesta','Loose or irritating wire','Loser oder störender Draht'],'sos3':['Módulo o cadena elástica','Elastic module or chain','Gummiring oder elastische Kette'],'sos4':['Retenedor fijo','Fixed retainer','Festsitzender Retainer'],'sos5':['Dolor después de control','Discomfort after adjustment','Beschwerden nach Kontrolle'],'sos6':['Aparato removible','Removable appliance','Herausnehmbare Apparatur'],'sosA':['Llama a la clínica para recibir indicaciones. El equipo determinará los próximos pasos.','Call the clinic for guidance. The team will determine the next steps.','Rufen Sie die Praxis an. Das Team bespricht die nächsten Schritte.'],'prevention':['Prevención y atención familiar','Prevention and family care','Prävention und Familienzahnmedizin'],'restoration':['Restauración y estética','Restoration and aesthetics','Restauration und Ästhetik'],'rehab':['Rehabilitación y prótesis','Rehabilitation and prosthetics','Rehabilitation und Zahnersatz'],'special':['Tratamientos especializados','Specialist treatments','Spezialisierte Behandlungen'],'diagnosis':['Consulta y diagnóstico','Consultation and diagnosis','Beratung und Diagnostik'],'planning':['Plan de tratamiento','Treatment plan','Behandlungsplan'],'followup':['Seguimiento','Follow-up','Nachsorge'],'visit1':['Escuchamos tus expectativas y evaluamos tus dientes y mordida.','We discuss your expectations and assess your teeth and bite.','Wir besprechen Ihre Erwartungen und untersuchen Zähne und Biss.'],'visit2':['Los registros diagnósticos permiten preparar un plan individualizado y hablar de duración y costos.','Diagnostic records help prepare an individual plan and discuss duration and costs.','Diagnostische Unterlagen unterstützen die individuelle Planung und das Gespräch über Dauer und Kosten.'],'visit3':['El equipo evalúa el progreso y las necesidades de retención según el plan.','The team evaluates progress and retention needs according to the plan.','Das Team beurteilt Fortschritt und Retentionsbedarf gemäß dem Plan.']}
profiles=['andre','veronica','minerva','david','jaime','mirna']; patients=['first','faq','sos','braces']; gallery=[0,2,19,22,25,27,31,34,41,42,43,47]
def tr(k,l):return T[k][langs.index(l)]
def text(id,l,col=0):return C[id][col*3+langs.index(l)]
def title(id,l):return text(id,l)
def url(id,l):return by[id][l]
def a(id,l,label=None,cls=''):return f'<a class="{cls}" href="{url(id,l)}">{E(label or title(id,l))}</a>'
def btn(id,l,label=None,alt=False):return f'<a class="btn{" alt" if alt else ""}" href="{url(id,l)}">{E(label or title(id,l))}<span aria-hidden="true">↗</span></a>'
def whatsapp(l):
 w=CONTACT['whatsapp']
 if not (w['active'] and w['verified_current']):return f'<button class="btn" disabled data-channel="whatsapp">{tr("whatsapp",l)}</button>'
 from urllib.parse import quote
 return f'<a class="btn" href="https://wa.me/{w["e164"].lstrip("+")}?text={quote(w["messages"][l])}">WhatsApp ↗</a>'
def call(l):return f'<a class="btn" href="tel:+50322439979">{E(tr("phone",l))}<span aria-hidden="true">↗</span></a>'
def img(id,l,cls=''):
 f=by[id].get('image');return f'<img class="{cls}" src="/assets/{E(f)}" alt="{E(title(id,l))}" loading="lazy" decoding="async">' if f else ''
def logo(unit):return f'/assets/logo-{ "dental" if unit=="dental" else "ortodoncia"}-original.png'
def header(p,l):
 unit='dental' if p['identity']=='APEL Dental' or p['id']=='dental' or p['parent']=='dental' else 'ortho'
 def units(cls):return f'<nav class="units {cls}" aria-label="APEL"><a href="{url("ortho",l)}" {"aria-current=\"true\"" if unit=="ortho" and p["id"]!="home" and p["parent"]=="ortho" or p["id"]=="ortho" else ""}>{E(title("ortho",l))}</a><a href="{url("dental",l)}" {"aria-current=\"true\"" if unit=="dental" else ""}>{E(title("dental",l))}</a></nav>'
 return f'<a class="skip" href="#main">{tr("skip",l)}</a><header class="header atz-nav atz-nav-menuhost" data-atz-id="ATZ-NAV-001"><div class="wrap headtop"><a class="logo" href="{url("home",l)}" aria-label="{title("home",l)} · APEL"><img src="{logo(unit)}" alt="APEL {"Dental" if unit=="dental" else "Ortodoncia"}"></a>{units("desktop-units")}<div class="head-actions"><nav class="languages" aria-label="Languages">'+''.join(f'<a lang="{x}" hreflang="{x}" href="{p[x]}" {"aria-current=\"page\"" if x==l else ""}>{x.upper()}</a>' for x in langs)+f'</nav>{btn("contact",l,tr("book",l))}<button class="atz-nav-trigger apel-menu-trigger" type="button" data-azn1-menu-trigger aria-controls="atz-nav-dialog-001" aria-expanded="false" aria-label="{tr("menu",l)}"><span class="atz-nav-glyph" aria-hidden="true"><i></i><i></i></span><span>{tr("menu",l)}</span></button><a class="atz-nav-fallback" href="#site-map">{tr("menu",l)}</a></div></div><div class="wrap">{units("mobile-units")}</div>{nav_dialog(l)}</header>'
def nav_dialog(l):
 labels={'es':['Doctores','Clínica','Pacientes'],'en':['Doctors','Clinic','Patients'],'de':['Ärzte','Praxis','Patienten']}[l]
 links=''.join(f'<li><a data-azn1-menu-link href="{url(id,l)}"><strong>{E(label)}</strong><small>0{i}</small></a></li>' for i,(id,label) in enumerate(zip(['couple','clinic','patients'],labels),1))
 photos=''.join(f'<div data-azn1-menu-photo class="atz-nav-photo{" is-active" if i==0 else ""}" style="background-image:url(/assets/{f})"></div>' for i,f in enumerate(['home.webp','clinic.webp','gallery-42.webp']))
 return f'<div class="atz-nav-dialog apel-nav-dialog" id="atz-nav-dialog-001" role="dialog" aria-modal="true" aria-label="{tr("menu",l)}" tabindex="-1" data-azn1-menu hidden><div class="atz-nav-dialog-left"><div class="atz-nav-dialog-head"><strong>APEL</strong><button type="button" data-azn1-menu-close aria-label="{tr("close",l)}">{tr("close",l)} <span aria-hidden="true">×</span></button></div><div class="atz-nav-dialog-links-wrap"><span>{tr("navigate",l)} / 01</span><ul class="atz-nav-dialog-links">{links}</ul></div><div class="atz-nav-dialog-foot"><a href="{url("contact",l)}">{tr("book",l)} · +503 2243-9979 ↗</a></div></div><div class="atz-nav-dialog-visual" aria-hidden="true">{photos}<span class="atz-nav-photo-caption">{tr("original",l)}</span></div></div>'

def crumb(p,l):
 if p['id']=='home':return ''
 par=p['parent']; return '<nav class="wrap crumb" aria-label="Breadcrumb">'+a('home',l)+'<span>/</span>'+((a(par,l)+'<span>/</span>') if par and par!='home' and par in by else '')+f'<span aria-current="page">{E(title(p["id"],l))}</span></nav>'
def index(ids,l):return '<div class="index-list">'+''.join(f'<a href="{url(id,l)}"><span>{i:02}</span><span>{E(title(id,l))}</span><span aria-hidden="true">↗</span></a>' for i,id in enumerate(dict.fromkeys(ids),1))+'</div>'
def section(body,cls=''):return f'<section class="section {cls}"><div class="wrap">{body}</div></section>'
def team(ids,l):return '<div class="team-grid">'+''.join(f'<a class="team-item" href="{url(id,l)}">{img(id,l)}<h3>{E(title(id,l))} ↗</h3><p>{E(text(id,l,1))}</p></a>' for id in ids)+'</div>'
def editorial(id,l,kicker='',reverse=False):return f'<div class="editorial{" reverse" if reverse else ""}">{img(id,l,"portrait" if id=="couple" else "wide")}<div class="body"><span class="kicker">{E(kicker or title(id,l))}</span><h2>{E(text(id,l,1))}</h2><p>{E(text(id,l,2))}</p><div class="links">{btn(id,l,tr("read",l))}</div></div></div>'
def home(l):
 phrase=text('home',l,1).rstrip('.'); split={'es':('La calidad es','nuestra pasión.'),'en':('Quality is','our passion.'),'de':('Qualität ist','unsere Leidenschaft.')}[l]
 hero=f'<section class="hero"><div class="wrap hero-inner"><h1 class="hero-title">{E(split[0])}<span class="serif">{E(split[1])}</span></h1><img class="hero-photo" src="/assets/home.webp" alt="{tr("doctors",l)}" fetchpriority="high"><div class="hero-copy"><p>{E(text("home",l,2))}</p><div class="hero-actions">{btn("ortho",l)}{btn("dental",l)}</div></div><div class="hero-caption">{tr("doctors",l)} · {tr("location",l)}</div></div></section>'
 chapters='<div class="chapter-head"><h2>'+tr('units',l)+'</h2><p>'+tr('unitdesc',l)+'</p></div><div class="chapter-pair">'+''.join(f'<article class="chapter"><span class="number">0{i} / APEL</span><img class="chapter-logo" src="{logo(id)}" alt="{title(id,l)}"><h3>{E(text(id,l,1))}</h3><p>{E(text(id,l,2))}</p>{a(id,l,tr("explore",l)+" ↗","textlink")}</article>' for i,id in enumerate(['ortho','dental'],1))+'</div>'
 authority=f'<div class="split-title"><h2>{tr("doctors",l)}</h2>{a("couple",l,tr("journey",l)+" ↗","textlink")}</div>'+team(['andre','veronica'],l)+f'<div class="links" style="margin-top:30px">{btn("team",l,tr("team",l),True)}</div>'
 exp=editorial('clinic',l)+f'<div class="split-title" style="margin-top:64px"><h2>{title("patients",l)}</h2>{a("patients",l,tr("explore",l)+" ↗","textlink")}</div>'+index(patients,l)
 return hero+section(chapters,'surface')+section(authority)+section(exp,'surface')
def heading(id,l):return f'<section class="pagehead"><div class="wrap"><span class="kicker">APEL / {E(title(by[id]["parent"],l) if by[id]["parent"] in by and by[id]["parent"]!="home" else tr("navigate",l))}</span><h1>{E(title(id,l))}</h1><p class="lead">{E(text(id,l,1))}</p><p class="intro">{E(text(id,l,2))}</p></div></section>'
def unit(id,l):
 p=by[id]; intro=f'<section class="pagehead"><div class="wrap unithead"><div><span class="kicker">APEL / 0{"1" if id=="ortho" else "2"}</span><h1>{E(title(id,l))}</h1><p class="lead">{E(text(id,l,1))}</p><p class="intro">{E(text(id,l,2))}</p><div class="links">{btn("contact",l,tr("book",l))}{btn("team",l,tr("team",l),True)}</div></div>{img(id,l)}</div></section>'
 groups=[('services',['appliances','aligners','interdisciplinary','other'])] if id=='ortho' else [('prevention',['cleaning','kids']),('restoration',['resin','veneers','crowns','whitening']),('rehab',['dentures','valplast','implants']),('special',['surgery','endo','sedation'])]
 body='<h2>'+tr('services',l)+'</h2>'+''.join(f'<h3 class="group-title">{tr(k,l)}</h3>'+index(ids,l) for k,ids in groups)
 return intro+section(body)+source(id,l)+section(f'<div class="split-title"><h2>{tr("team",l)}</h2>{a("team",l,tr("read",l)+" ↗","textlink")}</div>'+team(['andre'] if id=='ortho' else ['veronica','minerva','david','jaime','mirna'],l),'surface')+section(f'<h2>{title("patients",l)}</h2>'+index(patients+(['dental'] if id=='ortho' else ['ortho']),l))
def formattext(t):
 t=t.replace('**','').replace('\xa0',' ');parts=re.split(r'\n\s*\n',t);out=[]
 for part in parts:
  lines=part.strip().splitlines(); ls=[]; para=[]
  def flush():
   if para:out.append('<p>'+E(' '.join(para).strip())+'</p>');para.clear()
  for line in lines:
   if not line.strip():continue
   if line.strip().startswith(('* ','- ')):
    flush();ls.append(E(line.strip()[2:]));continue
   if ls:out.append('<ul>'+''.join('<li>'+x+'</li>' for x in ls)+'</ul>');ls=[]
   para.append(line.strip())
  flush()
  if ls:out.append('<ul>'+''.join('<li>'+x+'</li>' for x in ls)+'</ul>')
 return ''.join(out)
def source(id,l,cv=False):
 ss=by[id]['source_sections'];
 if not ss:return ''
 # Historical content only: place all potentially outdated clinical claims within an explicitly marked review disclosure.
 nav=''.join(f'<a href="#detail-{i}">{E(s["heading"] or str(i+1))}</a>' for i,s in enumerate(ss))
 body=''.join(f'<section id="detail-{i}"><h3>{E(s["heading"])}</h3>{formattext(s["text"])}</section>' for i,s in enumerate(ss))
 label=tr('cv' if cv else 'source',l)
 content=f'<div class="reading" lang="es"><aside><span class="kicker">{tr("toc",l)}</span>{nav}</aside><article>{body}</article></div>'
 if l=='es' and (cv or id not in ['sos','faq']):return section(f'<h2 style="margin-bottom:40px">{E(label)}</h2>'+('' if cv else f'<p class="warning">{tr("clinical",l)}</p>')+content)
 return section(f'<div class="details"><details><summary>{E(label)}</summary><div><p class="warning">{tr("clinical",l) if l=="es" else tr("draft",l)}</p>{content}</div></details></div>','surface')
def related(id,l):
 p=by[id];ids=[]
 for b in p['blocks']:
  ids.extend(b['links'])
 ids=[x for x in dict.fromkeys(ids) if x in by and x not in [id,'home','contact']]
 if p['plantilla']=='tratamiento' and 'team' not in ids:ids.append('team')
 return section(f'<h2>{tr("related",l)}</h2>'+index(ids,l)) if ids else ''
def profile(id,l):return f'<section class="pagehead"><div class="wrap profile">{img(id,l)}<div><span class="kicker">{title("team",l)} / APEL</span><h1>{E(title(id,l))}</h1><p class="lead">{E(text(id,l,1))}</p><p>{E(text(id,l,2))}</p>{btn("contact",l,tr("book",l))}</div></div></section>'+source(id,l,True)+related(id,l)
def gallerybody(l):return '<div class="gallery-grid">'+''.join(f'<a href="/assets/gallery-{i}.webp" data-lightbox><img src="/assets/gallery-{i}.webp" alt="{tr("original",l)} · {n:02}" loading="lazy"></a>' for n,i in enumerate(gallery,1))+'</div>'
def detailrows(rows):return '<div class="details">'+''.join(f'<details><summary>{E(q)}</summary><div>{E(a)}</div></details>' for q,a in rows)+'</div>'
def studio(l):
 colors=[('#C1D540',['Verde','Green','Grün']),('#D94A66',['Rosa','Pink','Rosa']),('#2672B8',['Azul','Blue','Blau']),('#6B43A6',['Morado','Purple','Violett']),('#E8842C',['Naranja','Orange','Orange']),('#222222',['Negro','Black','Schwarz']),('#D4D4D4',['Gris','Grey','Grau']),('#FFFFFF',['Blanco','White','Weiß']),('#D53936',['Rojo','Red','Rot'])]; parts=[]
 for i in range(16):
  row=i//8; col=i%8;x=36+col*56;y=55+row*115
  parts.append(f'<g data-region="{i}" transform="translate({x} {y})"><rect width="49" height="76" rx="16" fill="#FFFFFF" stroke="#696969" stroke-width="1.5"/><rect data-elastic="{i}" x="14" y="25" width="21" height="25" rx="7" fill="none" stroke="#C1D540" stroke-width="7"/><rect x="19" y="30" width="11" height="15" rx="2" fill="#DCDEE4" stroke="#696969"/></g>')
 svg='<svg id="brace-svg" viewBox="0 0 520 285" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="'+E(title('braces',l))+'"><rect width="520" height="285" fill="#F7F7F7"/><path d="M22 42 Q260 -5 498 42 L498 243 Q260 290 22 243Z" fill="#DCDEE4"/>'+''.join(parts)+'<path d="M30 92H490M30 207H490" stroke="#696969" stroke-width="3" pointer-events="none"/></svg>'
 controls=f'<div class="studio-controls"><h3>{tr("select",l)}</h3><div class="region-grid">'+''.join(f'<button type="button" data-choose="{i}" aria-label="{tr("region",l)} {i+1}" aria-pressed="{"true" if i==0 else "false"}">{i+1}</button>' for i in range(16))+f'</div><h3>{tr("color",l)}</h3><div class="color-palette">'+''.join(f'<button type="button" data-color="{c}" aria-pressed="false"><span class="swatch" style="background:{c}"></span>{E(n[langs.index(l)])}</button>' for c,n in colors)+f'</div><div class="links"><button class="btn" data-apply>{tr("apply",l)}</button><button class="btn alt" data-reset>{tr("reset",l)}</button><button class="btn alt" data-download>{tr("download",l)}</button></div><p class="small" aria-live="polite" id="studio-status"></p></div>'
 return section(f'<p class="warning">{tr("demo",l)}</p><noscript><p>{tr("nojs",l)}</p></noscript><div class="studio"><div class="studio-drawing">{svg}</div>{controls}</div>')
def mainbody(p,l):
 id=p['id']; typ=p['plantilla']
 if id=='home':return home(l)
 if typ=='unidad':return unit(id,l)
 if typ=='perfil':return profile(id,l)
 body=heading(id,l)
 if id=='couple':return body+section(editorial('couple',l)+f'<div style="margin-top:50px">{team(["andre","veronica"],l)}</div>')+related(id,l)
 if id=='team':return body+section(team(profiles,l))+related(id,l)
 if id=='clinic':return body+section(editorial('clinic',l)+f'<div class="links" style="margin-top:32px">{btn("gallery",l)}</div>')+source(id,l)+section(gallerybody(l),'surface')+related(id,l)
 if id=='gallery':return body+section(gallerybody(l))+related(id,l)
 if id=='patients':return body+section(index(patients,l))+related(id,l)
 if id=='first':return body+section(''.join(f'<div class="editorial rule" style="padding:28px 0"><h3>{i:02} / {tr(k,l)}</h3><p>{tr(v,l)}</p></div>' for i,(k,v) in enumerate([('diagnosis','visit1'),('planning','visit2'),('followup','visit3')],1)))+source(id,l)+related(id,l)
 if id=='faq':return body+section(detailrows([(tr('faq'+str(i),l),tr('faqA'+str(i),l)) for i in range(1,5)]))+source(id,l)+related(id,l)
 if id=='sos':return body+section(call(l)+f'<p class="warning">{tr("clinical",l)}</p>'+detailrows([(tr('sos'+str(i),l),tr('sosA',l)) for i in range(1,7)]))+source(id,l)+related(id,l)
 if id=='braces':return body+studio(l)+related(id,l)
 if id=='contact':return body+section(f'<span class="kicker">{tr("location",l)}</span><a class="callblock" href="tel:+50322439979">+503 2243-9979 ↗</a><p>{tr("contactInfo",l)}</p><div class="links" style="margin:30px 0">{whatsapp(l)}</div><p class="warning">{tr("address",l)}</p>{a("privacy",l,None,"textlink")}')
 if id=='privacy':return body+section(f'<p class="warning">{tr("legal",l)}</p>'+a('contact',l,None,'textlink'))
 return body+(section(f'<figure style="margin:0;max-width:640px">{img(id,l)}<figcaption class="asset-credit">{tr("original",l)}</figcaption></figure>') if p.get("image") else "")+source(id,l)+related(id,l)
def footer(l):
 return f'<section class="section green contact-end"><div class="wrap"><div><span class="kicker">APEL / {tr("book",l)}</span><h2>{E(text("contact",l,1))}</h2><p>+503 2243-9979</p></div>{btn("contact",l,tr("book",l),True)}</div></section><footer id="site-map" class="footer"><div class="wrap"><div class="footer-top"><div><a href="{url("ortho",l)}"><img class="footer-logo" src="{logo("ortho")}" alt="APEL Ortodoncia"></a>'+''.join(a(x,l) for x in ['ortho','appliances','aligners','interdisciplinary','other'])+f'</div><div><a href="{url("dental",l)}"><img class="footer-logo" src="{logo("dental")}" alt="APEL Dental"></a>'+''.join(a(x,l) for x in ['dental']+by['dental']['children'])+f'</div><div><h3>{tr("navigate",l)}</h3>'+''.join(a(x,l) for x in ['couple','team','clinic','gallery','patients']+patients+['contact','privacy'])+f'</div></div><div class="footer-bottom"><span class="small">{tr("preview",l)} · ATREZZO STUDIOS</span><span class="small">{tr("location",l)}</span></div></div></footer>'
def dialogs(l):
 gids=['ortho','dental','team','first','faq','sos','braces','contact','clinic']; groups=[['ortho','dental','couple','team'],['clinic','patients','sos','braces','contact']]; data={'q':tr('guideq',l),'back':tr('back',l),'nodes':{id:{'name':title(id,l),'url':url(id,l),'children':by[id]['children']} for id in by},'root':gids}
 return f'<button class="guide-launch" data-open="guide" aria-haspopup="dialog">{tr("help",l)} <span aria-hidden="true">↗</span></button><dialog class="guide" id="guide"><div class="dialog-head"><h2>{tr("help",l)}</h2><button class="close" data-close aria-label="{tr("close",l)}">×</button></div><div class="guide-body" id="guide-body"></div></dialog><dialog class="gallery-dialog" id="lightbox"><div class="dialog-head"><button class="close" data-prev aria-label="{tr("prev",l)}">‹</button><button class="close" data-next aria-label="{tr("next",l)}">›</button><button class="close" data-close aria-label="{tr("close",l)}">×</button></div><img alt="{tr("original",l)}"></dialog><script type="application/json" id="guide-data">{json.dumps(data,ensure_ascii=False).replace("<","\\u003c")}</script>'
def document(p,l):
 id=p['id']; t=title(id,l); desc=text(id,l,2); alternates=''.join(f'<link rel="alternate" hreflang="{x}" href="{p[x]}">' for x in langs); return f'<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{E(t)} | APEL</title><meta name="description" content="{E(desc,quote=True)}"><link rel="canonical" href="{p[l]}">{alternates}<link rel="stylesheet" href="/assets/atz-nav/ATZ-NAV-001.css"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script><script type="module" src="/assets/nav-mount.js"></script></head><body>{header(p,l)}<main id="main" tabindex="-1">{crumb(p,l)}{mainbody(p,l)}</main>{footer(l)}{dialogs(l)}</body></html>'
def build():
 if D.exists():shutil.rmtree(D)
 D.mkdir();(D/'assets').mkdir();shutil.copy2(R/'src/site.css',D/'assets/site.css');shutil.copy2(R/'src/site.js',D/'assets/site.js');shutil.copytree(R/'src/vendor/atz-nav',D/'assets/atz-nav');shutil.copy2(R/'src/nav-mount.js',D/'assets/nav-mount.js')
 for p in P:
  for l in langs:
   out=D/p[l].strip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(document(p,l))
 for l in langs:
  x={'es':'Página no encontrada','en':'Page not found','de':'Seite nicht gefunden'}[l]; out=D/('' if l=='es' else l)/'404.html';out.write_text(f'<!doctype html><html lang="{l}"><meta charset="utf-8"><meta name="robots" content="noindex"><title>{x}</title><link rel="stylesheet" href="/assets/site.css"><main class="wrap section"><h1>{x}</h1>{btn("home",l)}</main></html>')
 (D/'robots.txt').write_text('User-agent: *\nDisallow: /\n');print(f'Generated {len(P)*len(langs)} routes in {D}')
if __name__=='__main__':
 build()
 # GitHub Pages staging project prefix; reference existing public media, never upload photos.
 images=json.loads((R/'data/public-image-urls.json').read_text())
 for file in D.rglob('*.html'):
  value=file.read_text()
  for name,remote in images.items():value=value.replace('/assets/'+name,remote)
  value=re.sub(r'((?:href|src)=")/(?!/)',r'\1/apel-ortodoncia/',value)
  value=value.replace('"url": "/','"url": "/apel-ortodoncia/')
  file.write_text(value)
 (D/'.nojekyll').write_text('')

