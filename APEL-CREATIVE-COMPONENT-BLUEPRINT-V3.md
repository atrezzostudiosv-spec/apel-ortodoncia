# APEL — CREATIVE COMPONENT BLUEPRINT V3

**Dirección creativa independiente · 18/11/2026 · Fase 08 abierta**
**Estado:** propuesta de implementación para Codex; no constituye aceptación visual ni autorización para publicar.
**Base auditada:** APEL main `63e6cb63cd248d9c91f5a13ea7df0a6d40482744`. Catálogo ATREZZO fijado en `9ee01f9e4de7208e0f1ec16882239b9124e68f78`. Verificar ambos HEAD y las decisiones vigentes antes de ejecutar. Este documento no contiene fuentes privadas, material clínico ni nuevos datos del cliente.

## 1. Mandato y diagnóstico

APEL debe ser una experiencia editorial inmersiva, no un catálogo ni un documento con animaciones. El portal mantiene Dental a la izquierda y Ortodoncia a la derecha; cada unidad tiene su propio website, cabecera visible, identidad original y navegación cruzada. Se mantienen ES/EN/DE, rutas vigentes, Poppins/Lora, colores y logotipos originales. No reabrir etapas 01–07. V1 sigue rechazada; V2 sigue en revisión. No cambiar dominio, DNS ni biblioteca.

**Causa demostrable:** `v2/build.py` selecciona `interior()` por familia y vuelca `blocks()` dentro de un lector genérico. La rama treatment consulta fotos de la primera escena pero no las renderiza. `blocks()` convierte numerosas jerarquías originales a h2 y otros elementos a párrafos. `SECTION_CSS` y `narrative()` fijan motion exclusivamente en las dos Home (además de la transición de portal). `composition.py` define capítulos de Home, no una composición completa por página. El problema no es Python ni la generación estática; es que la composición no se gobierna por una partitura completa. La vista de limpieza dental confirma una portada textual y un artículo sin imágenes; el perfil André, una fotografía y un índice curricular. La clínica Dental usa una foto y texto.

**Regla de arquitectura:** conservar infraestructura y trazabilidad verificables, no la estética de la plantilla. Una página puede compartir primitivas semánticas, tipografía y componentes con otras; no debe compartir por defecto una secuencia visual que ignore su contenido.

## 2. Lenguaje visual y reglas de composición

- Grid editorial desktop de 12 columnas, márgenes amplios, ritmo intencionado; tablet y móvil se recomponen, no se limitan a apilar columnas. Usar tokens actuales, no crear otra identidad. Poppins para lectura/navegación; Lora para titulares editoriales. Una jerarquía principal visible por escena.
- Escala y contraste: alternar portada amplia, escena de lectura, escena fotográfica, transición y cierre. No encerrar todo en tarjetas, bordes, píldoras o paneles repetidos. No aplicar sombra, degradados, fondos oscuros, neón o filtros por reflejo.
- Ortodoncia: carácter preciso, contemporáneo, clínico y humano. Dental: atención multidisciplinaria, cálida y profesional. Ambos deben parecer APEL, no dos plantillas de agencias distintas.
- Fotografías como contenido, no decoración: encuadrar con punto focal, preservar rostros, no estirar ni duplicar imágenes para rellenar escenas. Fotografías de personas y espacios solo con autorización; una fotografía de clínica nunca se presenta como demostración de un procedimiento.
- Cada portada responde de inmediato qué unidad/página es, por qué importa y cómo continuar. CTA pertinente visible sin completar una animación. Evitar repetir el mismo titular en H1 y primer H2 o convertir etiquetas heredadas (por ejemplo BLOG) en párrafos aislados.
- Contenido: mantener IDs de origen y textos íntegros en el master, separar títulos, introducciones, listas reales, datos y preguntas. La organización editorial puede cambiar; reescrituras clínicas, traducciones, claims y eliminación de duplicados requieren cotejo/registro. No inventar beneficios, tiempos, precios, tecnologías, pasos, resultados ni indicaciones clínicas.
- No confundir visual premium con saturación de motion: una escena protagonista por tramo narrativo; evitar pins consecutivos que obliguen a scroll largo. Páginas de contacto, SOS, privacidad y ayuda inmediata: rapidez, legibilidad y controles nativos, no animaciones que retrasen la tarea.
- Las referencias Studio Brusco, LAVA, Smilebar y West LA son estándar creativo, no fuentes de código ni autorización para extraer efectos. No copiar branding.

## 3. Contrato de integración ATREZZO

Registro: [registry/components.json](https://github.com/atrezzostudiosv-spec/atrezzo-repositorio/blob/9ee01f9e4de7208e0f1ec16882239b9124e68f78/registry/components.json). Demos: https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/index.html

Códigos de la partitura:
- **R**: conservar componente ya presente, condicionado a verificación de fidelidad en destino.
- **I**: integración dirigida; ejecutar si el gate de medios, semántica, licencia y compatibilidad pasa.
- **C**: componente condicionado; si no hay medios o contenido suficiente, entregar composición editorial estática de calidad y documentar el bloqueo. No fabricar un efecto parecido.
- **E**: composición estática APEL; no implica un nuevo motor ni un ID inventado. Controles nativos funcionales permitidos.

| ID y demo | Rol | Requisito / límite |
|---|---|---|
| [ATZ-PGT-002](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-PGT-002) | Split entre documentos | R: portal → unidad. No retrasar contacto/SOS. |
| [ATZ-MOT-005](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-MOT-005) | Cinematic Hero Reveal | I: portada Ortodoncia, máscara original del 42% a full-screen. CTA y H1 disponibles de inmediato. |
| [ATZ-SEC-002](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-SEC-002) | Split | I: presentación Dental; recorte progresivo original y texto acompañante. |
| [ATZ-SEC-004](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-SEC-004) | Cinematic Handoff | R condicionado: dos ideas consecutivas, fotos aptas; no añadir otra escena pinned contigua. |
| [ATZ-SEC-007](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-SEC-007) | Full-Bleed Chapters | R condicionado: tres capítulos ortodoncia, fotos horizontales apropiadas, sin texto sobre rostro. |
| [ATZ-MOT-006](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-MOT-006) | Editorial Journey | C/I: proceso con capítulos e imágenes acreditadas, sticky desktop e imágenes por paso en móvil. |
| [ATZ-NAV-002](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-NAV-002) | Chapter Rail | I: trayectoria extensa o tratamiento extenso con capítulos reales; banda horizontal móvil; anclas nativas. No aplicar a páginas cortas. |
| [ATZ-SEC-005](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-SEC-005) | Horizontal Filmstrip | C: instalaciones/galería con secuencia de fotos diferentes, suficientes para DOM original. Scroll vertical mueve filmstrip; no simular con carrusel. |
| [ATZ-MIC-004](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-MIC-004) | Image Hover Reveal | I/C: índice de especialistas o tratamientos solo con fotos correspondientes. Hover/foco; miniaturas y enlaces en touch/sin JS. |
| [ATZ-MIC-003](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-MIC-003) | CTA Arrow & Fill | I: CTA editorial en ambas unidades, no globalizar indiscriminadamente. |
| [ATZ-SVC-001](https://atrezzostudiosv-spec.github.io/atrezzo-repositorio/catalog/preview.html?id=ATZ-SVC-001) | Service Bento 1+4 | C: solamente si el master acredita una línea principal, cuatro secundarias y cinco imágenes pertinentes. No imponer jerarquía comercial ni cinco servicios inventados. Si no pasa, índice estático editorial. No importar identidad Tri-Lane. |

Las fichas individuales son la autoridad para dependencias, archivos, hooks y restricciones; abrir demo real, copiar HTML/CSS/JS/runtime originales, verificar SHA-256, conservar estructura DOM, tiempos, geometría, capas, triggers, comportamiento de ida y vuelta y licencias. Solo sustituir medios/textos/tokens permitidos. Si una adaptación cambia el efecto o la geometría, requiere aprobación. Las demos abstractas no se publican como material clínico. `client_ready:false` hasta verificación específica en APEL.

**Importante:** no utilizar componentes más complejos de portfolio, preloaders o WebGL por espectáculo; APEL es una clínica y debe permitir atención inmediata. La cabecera visible recuperada es una decisión vigente; no volver a Immersive Menu.

## 4. Partitura de Home (orden exacto)

### Portal / — selección, no tercera marca
P1: dos mitades iguales a pantalla disponible en desktop; mantener izquierda Dental y derecha Ortodoncia. Fotografía distinta por unidad, logo intacto, denominación y acción inequívoca. Usar los originales autorizados correspondientes (en preview: d-veronica y o-pair), revisar recortes; evitar logos/títulos redundantes. Móvil: dos accesos consecutivos con igual peso y ambos reconocibles rápidamente. Idiomas visibles.
P2: R ATZ-PGT-002 al elegir unidad, navegación real y retorno correcto. No añadir hero, servicios, marketing ni scroll narrativo al portal.

### /ortodoncia/ — cinco actos
O1 — Bienvenida/identidad: I ATZ-MOT-005 con fotografía horizontal autorizada de clínica/equipo; candidato o-room (evaluar recorte) o medio original pertinente. H1 y lema, contacto, logo contextual visible. El texto y foto deben convivir en una escena; no imagen aislada sobre título independiente. Comparar demo inicio/mitad/final.
O2 — Método y confianza: E composición asimétrica 5/7, titular de bienvenida y texto original agrupado, vínculo a concepto y segunda opinión. Diferenciar método de listado de aparatos. No duplicar encabezados ni poner BLOG como contenido suelto.
O3 — Tres capítulos: R ATZ-SEC-007, un plan para cada caso → estudio y práctica → visita. Fotografías originales o-chair/o-standing/o-reception de la preview, solo si el encuadre es adecuado; no tapar rostros. Destinos concepto, André, instalaciones. No añadir otro pin contiguo. Revisar entrada, tres relevos, salida e inverso.
O4 — Explorar tratamiento / pacientes: E índice editorial con dos jerarquías (tratamiento y ayuda), enlaces reales a aparatos, alineadores, interdisciplinarios, FAQ, inicio, ligas, SOS; C ATZ-MIC-004 solo si imágenes pertinentes de cada destino autorizadas. SOS inmediatamente distinguible.
O5 — Cierre: E contacto, financiación/ubicación/seguridad solo como consten en fuente; I ATZ-MIC-003 para contacto principal. No promesas nuevas ni repetir menú entero.

### /dental/ — cinco actos
D1 — Dirección humana: E portada editorial con retrato original d-veronica, título de calidad, introducción, cita y equipo. Foto grande, jerarquía integrada, espacio negativo; evitar párrafo largo dominante. Mantener texto íntegro en recorrido.
D2 — Autoridad → clínica: I ATZ-SEC-002 como presentación editorial de la doctora, con retrato de formato adecuado (d-standing candidato). Si se conserva el R ATZ-SEC-004 actual, solo como sustitución de este bloque, no apilar ambos. Decisión tras comparar demos y captura de APEL: prioridad Split; Handoff si Split no supera gate de composición y Handoff sí. Mantener acceso a trayectoria y clínica fuera de la animación.
D3 — Tratamientos: E índice editorial por estética e integral, titulares y enlaces diferenciados; C ATZ-SVC-001 solo con jerarquía 1+4 y cinco imágenes verificadas; C ATZ-MIC-004 en índice solo con correspondencia real. No convertir 13 tratamientos en tarjetas repetidas ni usar fotos genéricas de la clínica como imágenes de cada intervención.
D4 — Equipo: E dirección profesional con protagonismo de los perfiles acreditados y los seis especialistas accesibles; I ATZ-MIC-004 en índice de especialistas si los seis retratos encajan en su DOM original; preservar nombre y rol legibles sin hover. Retratos reales d-* y o-office de preview; revisar foco y proporciones. La escena de equipo debe ser diferente de tratamientos.
D5 — Cierre: E experiencia de clínica, ubicación, financiación y cita con jerarquía de lectura, I ATZ-MIC-003 para cita. Evitar bloques de texto redundantes y guías duplicadas.

## 5. Matriz por las 47 páginas canónicas

Los paths siguientes son los 47 del árbol publicado ES (portal + 26 Dental + 20 Ortodoncia). Cada fila hereda su equivalente EN/DE por ID canónico del master; no generar nuevas rutas por traducción literal de slug. Las secuencias son órdenes de composición, no copy nuevo ni autorización clínica. Fotos mencionadas son candidatas del inventario público; el paquete privado debe determinar correspondencia y autorización. Si falta una imagen, conservar el contenido en una composición tipográfica deliberada, no insertar imágenes de stock.

### Dental (26)

| Ruta ES | Secuencia editorial y foco | Componentes |
|---|---|---|
| /dental/ | D1–D5 anteriores | I SEC-002; C SEC-004 alternativo, SVC-001, MIC-004; I MIC-003 |
| /dental/clinica/ | Introducción de experiencia → foto amplia d-room → narrativa humana/tecnología según fuente → acceso galería y cita | E; C SEC-005 solo con fotos adicionales |
| /dental/clinica/galeria/ | Apertura fotográfica → secuencia de espacios autorizados → vista ampliada nativa y regreso | C SEC-005; E galería accesible si insuficiente |
| /dental/especialistas/ | Introducción de equipo → nombres/roles y retratos con jerarquía → perfil → cita | I MIC-004 con gate de retratos; E fallback |
| /dental/especialistas/veronica-de-apel/ | Retrato principal → formación y experiencia → cronología acreditada → credenciales completas → cita | E; I NAV-002 si capítulos suficientes |
| /dental/especialistas/minerva-quevedo/ | Retrato → especialidad → formación/experiencia según fuente → trayectoria documentada → cita | E; C NAV-002 solo si extensa |
| /dental/especialistas/david-arguello/ | Retrato → identidad profesional reconciliada entre versiones → trayectoria → credenciales → cita | E; C NAV-002; gate de discrepancias |
| /dental/especialistas/jaime-fuentes/ | Retrato → especialidad → formación/experiencia → credenciales → cita | E; C NAV-002 |
| /dental/especialistas/mirna-arevalo/ | Retrato → especialidad → experiencia/formación → credenciales → cita | E; C NAV-002 |
| /dental/tratamientos/ | Apertura tipográfica/fotográfica de unidad → estética e integral como dos capítulos → índice completo → cita | E; C MIC-004 / SVC-001 bajo gate |
| /dental/tratamientos/ortodoncia/ | Explicación del tratamiento → acceso claro a unidad Ortodoncia → información original restante → cita | E; MIC-003 CTA |
| /dental/tratamientos/obturaciones-de-resina/ | Definición → contenido fuente por conceptos → cuidados/indicaciones solo si presentes → cita | E; C foto clínica específica autorizada |
| /dental/tratamientos/protesis-removibles/ | Definición → tipos existentes en fuente → lectura de detalles → cita | E; C imagen específica autorizada |
| /dental/tratamientos/valplast/ | Presentación del material/tratamiento según fuente → características en jerarquía tipográfica → cita | E; C imagen específica autorizada |
| /dental/tratamientos/carillas/ | Apertura de tratamiento → explicación/indicaciones según fuente → lectura completa → cita | E; C imagen específica autorizada |
| /dental/tratamientos/coronas/ | Definición → tipos o indicaciones documentadas → lectura completa → cita | E; C imagen específica autorizada |
| /dental/tratamientos/limpieza-dental/ | H1 + introducción clara → explicación en bloques legibles con subtítulos semánticos → beneficios/cuidados solo de fuente → cita | E; C foto propia específica. No repetir H1 ni índice de dos capítulos |
| /dental/tratamientos/blanqueamiento/ | Apertura → explicación y modalidades si acreditadas → detalles → cita | E; C foto propia específica. No antes/después inventado |
| /dental/tratamientos/cirugias-extracciones/ | Información directa → desarrollo por conceptos documentados → cuidados si constan → cita/contacto | E; C NAV-002 si larga. Sin imágenes gráficas innecesarias |
| /dental/tratamientos/endodoncia/ | Apertura → qué es → secciones de origen organizadas → cita | E; C NAV-002 si larga |
| /dental/tratamientos/implantes/ | Introducción → qué son/sujeción/finalidad → fases acreditadas → mantenimiento → preguntas y consejos de fuente → cita | I NAV-002; C MOT-006 solo si fotos por fase auténticas; E capítulos sin fotos |
| /dental/tratamientos/odontologia-infantil/ | Introducción orientada a familias → atención según fuente → FAQ agrupada, todas las preguntas accesibles → cita | E acordeón nativo y C NAV-002 si facilita lectura; sin imágenes de menores no autorizadas |
| /dental/tratamientos/sedacion-consciente/ | Información clínica clara → secciones de origen y preguntas, si constan → cita | E; sin claims de seguridad o resultados nuevos |
| /dental/contacto/ | Datos verificados → contacto directo → ubicación si fuente confirmada → cruce de unidad | E; sin motion bloqueante |
| /dental/citas/ | Acción de cita inmediata → método y datos comprobados → información útil mínima | E; no simular envío/reserva |
| /dental/privacidad/ | Texto legal validado → estructura accesible | E; bloquear producción si no hay texto verificado |

### Ortodoncia (20)

| Ruta ES | Secuencia editorial y foco | Componentes |
|---|---|---|
| /ortodoncia/ | O1–O5 anteriores | I MOT-005; R SEC-007; C MIC-004; I MIC-003 |
| /ortodoncia/clinica/filosofia/ | Titular de filosofía → principios de fuente con lectura editorial → vínculo al método y equipo | E; C SEC-002 con foto apropiada y texto legible |
| /ortodoncia/clinica/caracteristicas/ | Presentación → características verificadas → conexión con visita e instalaciones | E; C MOT-006 solo con capítulos y fotos reales |
| /ortodoncia/clinica/instalaciones/ | Foto a sangre → secuencia de espacios o-room/o-chair/o-reception/o-garden si autorizados y pertinentes → visita/contacto | C SEC-005; E secuencia estática |
| /ortodoncia/clinica/galeria/ | Galería editorial → imágenes únicas → ampliación nativa → retorno | C SEC-005; E galería |
| /ortodoncia/doctores-apel/ | Retrato conjunto o-pair → relación profesional según fuente → accesos a perfiles → contacto | E; C SEC-002 si recorte conserva rostros |
| /ortodoncia/doctores/andre-apel/ | Retrato → especialidad y maestría acreditadas → estudios → actividad profesional/docente → investigación y demás credenciales → contacto | I NAV-002; E cronología semántica, todas las credenciales |
| /ortodoncia/equipo/ | Presentación humana → equipo documentado → perfiles/enlaces cuando existan → contacto | E; C MIC-004 solo si cada persona tiene foto autorizada |
| /ortodoncia/tratamientos/ | Introducción → índice por modalidades auténticas y método → enlaces a cada destino → contacto | E; C MIC-004 si imágenes clínicas pertinentes |
| /ortodoncia/tratamientos/concepto/ | Definición del concepto → diagnóstico/planificación en secuencia de fuente → enlace inicio y contacto | E; C MOT-006 con capítulos reales y medios específicos |
| /ortodoncia/tratamientos/aparatos/ | Introducción → tipos removibles/funcionales/rompehábitos/brackets/férulas tal como constan → índice por familias → contacto | I NAV-002; E entradas tipográficas; C medios auténticos por tipo; sin equivalencias inventadas |
| /ortodoncia/tratamientos/alineadores/ | Definición de ortodoncia invisible → tipos descritos en original → información completa → contacto | E; C MOT-006 solo con secuencia acreditada; sin prometer duración/resultados |
| /ortodoncia/tratamientos/interdisciplinarios/ | Explicación → capítulos según disciplinas documentadas → lectura de casos si autorizados → contacto | E; I NAV-002 si capítulos diferenciados; sin casos ilustrativos inventados |
| /ortodoncia/pacientes/ | Entrada de ayuda → accesos por intención (inicio, FAQ, SOS, ligas) → contacto | E controles nativos; SOS visible y directo |
| /ortodoncia/pacientes/inicio-tratamiento/ | Información de inicio → instrucciones fuente en orden → acceso a SOS/contacto | E; no pin ni animación que oculte instrucciones |
| /ortodoncia/pacientes/preguntas-frecuentes/ | Preguntas agrupadas según contenido existente → acordeones nativos accesibles → contacto | E; C NAV-002 solo si grupos largos reales |
| /ortodoncia/pacientes/sos/ | Contacto inmediato → problemas listados por fuente → instrucciones visibles/accesibles | E; sin transición que bloquee ayuda ni inventar consejos |
| /ortodoncia/pacientes/ligas-de-colores/ | Herramienta primero → controles claros → previsualización/exportación solo si validada → nota explicativa | E controles nativos; paleta actual de demo no aprobada, cotejar; no sustituir por motion decorativo |
| /ortodoncia/contacto/ | Contacto inmediato → datos verificados y ubicación → acceso a otras unidades | E |
| /ortodoncia/privacidad/ | Texto legal validado → estructura accesible | E; bloquear producción si no hay texto verificado |

## 6. Cambio técnico obligatorio en Codex

Implementar esta partitura como un contrato de datos separado de los textos. Conservar el paquete privado y su trazabilidad; no subir matrices privadas a Git. El siguiente esquema es una especificación, no una ruta existente ni una implementación ya realizada.

```json
{
  "page_id": "ID canónico del master",
  "family": "tratamiento | perfil | ...",
  "scenes": [
    {
      "scene_id": "ID estable",
      "purpose": "intención comunicativa",
      "source_section_ids": ["IDs del master"],
      "source_block_ids": ["IDs del inventario"],
      "layout": "composición estática o renderer específico",
      "component_id": null,
      "component_requirement": "R | I | C | E",
      "asset_ids": [],
      "destination_ids": [],
      "desktop": "dirección de composición",
      "mobile": "recomposición",
      "fallback": "lectura y acción sin motion",
      "acceptance": ["estados de captura y comportamiento"]
    }
  ]
}
```

- `render()` selecciona portal/Home y un renderizador de escenas por ID de página; `interior()` no debe decidir la secuencia completa solo con `family`. Eliminar dependencia de `scenes[0].photos`: recorrer todas las escenas y asignar medios a su papel. Familias comparten primitivas, no una plantilla rígida.
- Renderizadores estáticos semánticos para portada editorial, sección fotográfica, lectura por capítulos, cronología, directorio, índice, FAQ, CTA y contacto. No inventar motores visuales. Preservar listas y niveles de encabezado por semántica, no convertir todo a H2/párrafo.
- Integración de componentes a partir de un mapa validado por ID: cargar únicamente CSS/JS/runtime necesarios para escenas activas, sin hardcodear solo Home; instanciar y destruir según ficha, no montar dos variantes incompatibles. No editar archivos originales. No modificar biblioteca.
- La comprobación debe fallar si falta un ID de página, un bloque queda sin destino, una escena requiere un componente ausente, se usan medios no autorizados o un fallback desaparece. Para C con gate fallido: registrar razón y composición estática deliberada; para I bloqueado: registrar y resolver o elevar a dirección creativa, no simular.
- La partitura tiene que cubrir 47 IDs canónicos y 141 rutas renderizadas; conservar localización por idioma, rutas y enlaces. Comparar contra master privado; no inferir que la preview pública es el total del contenido válido.
- No repetir secciones ni añadir claims para encajar una plantilla. Si la fuente carece de un bloque de la secuencia, no inventarlo. Registrar agrupación o omisión de duplicado con IDs y aprobación correspondiente.

## 7. Gate de calidad antes de presentar otra versión

**Primero, implementar y verificar de forma integral; no presentar un hero aislado ni reabrir diseño ya cerrado.** Orden de trabajo interno: reconciliar master/medios → partitura 47 IDs → montar componentes exactos → construcción de las 141 rutas → QA → revisión creativa.

1. **Cobertura:** manifest de 47 IDs/141 rutas con escenas, medios, componentes y fallback; 0 rutas/enlaces internos rotos; cada bloque original trazado; ES/EN/DE revisados por semántica y terminología; discrepancias de perfiles, teléfono, datos y avisos clínicos resueltas por fuente autorizada.
2. **Prueba de procedencia:** para cada ID, commit de biblioteca, ficha, demo, archivos/hashes, licencia, adaptación permitida. Comparativa demo vs APEL a los mismos estados: inicio estabilizado, intermedio, final y regreso; hover/foco/touch donde corresponda. Capturas y vídeo de recorrido de navegador real, no mockups ni captura generada. Hash y test no sustituyen revisión visual.
3. **Prueba visual:** capturas full-page del portal, dos Home y las 44 interiores ES; vistas 1440 y 375, además 768/1024 para familias y componentes; comprobar variantes EN/DE especialmente textos largos, navegación y encuadres. Registrar las composiciones sin imágenes y por qué. Comparar con website original como mínimo de calidad y referencias solo como estándar artístico. Ningún rostro oculto, texto superpuesto ilegible, contenido de demo, título duplicado sin propósito, huecos vacíos, botones sin destino o scroll horizontal accidental.
4. **Prueba funcional:** Chrome + WebKit/Safari y Firefox cuando disponible, móvil físico si accesible; teclado, foco, anclas, Escape, touch, zoom 200%, contraste WCAG AA, reduced motion, sin JS, scroll inverso, retorno del portal, contacto y SOS. Revisar errores consola, recursos 404, estabilidad de layout y tiempos de carga en móvil; documentar mediciones reales, no proclamar rendimiento sin medir.
5. **Cierre:** PR revisable con diff, manifest, enlaces a preview autorizada, informe de fallos y evidencia no privada. No publicar medios sensibles, capturas privadas ni fuentes en repositorio público. No activar dominio/DNS ni quitar noindex sin autorización. La preview es revisión, no sitio para cliente. `client_ready:false` y fase 08 abierta hasta aceptación integral expresa.

## 8. Instrucción de arranque para Codex

Lee AGENTS.md, ATREZZO-PROJECT-STATUS.md, el paquete privado V2 verificado y este blueprint. Este documento dirige composición; no reemplaza fuentes, contratos ni decisiones de privacidad. Confirma HEAD y compatibilidad con decisiones posteriores. Refactoriza el generador para que la partitura determine cada escena. No maquilles la V1/V2 ni reconstruyas efectos. Utiliza IDs reales, gate de medios y evidencia. Trabaja en la rama de implementación correspondiente con PR; no mezcles esta rama de documentación con cambios locales sin comprobar HEAD. Entrega el conjunto integral de portal + dos websites en los tres idiomas, no solo una portada. Mantén informado el estado y los bloqueos mediante el registro del proyecto.

**Límite de esta auditoría:** revisión de código publicado, árbol de rutas, assets públicos, muestras de páginas y fichas del catálogo. No se ha abierto/ejecutado visualmente cada demo ni inspeccionado el paquete privado. Los IDs y ubicación son dirección creativa; la aptitud de cada recurso y fidelidad de destino son gates de implementación. No se autoriza ningún nuevo contenido clínico ni nueva publicación.