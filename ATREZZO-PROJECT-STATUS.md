# ATREZZO PROJECT STATUS — APEL

2026-11-17 — Etapa 08 abierta. Etapas 01–07 cerradas.

## Preview web autorizada

El usuario autorizó la creación de una preview en vivo. `main` contiene el generador adaptado y las 108 rutas estáticas con prefijo GitHub Pages. El repositorio sigue público. No se han subido fotografías, logotipos binarios, archivos clínicos ni paquetes maestros. Fotografías y logos no clínicos enlazados desde URLs públicas originales. Los textos clínicos extensos no validados y las imágenes de tratamientos se excluyeron de la preview. Se conserva el paquete integral privado previamente entregado. No se modificó el dominio original ni DNS.

## QA ejecutada antes de transferir

108 rutas compiladas, 0 enlaces internos rotos, 3.888 referencias del árbol Smart Guide verificadas, 0 fotografías binarias. `noindex,nofollow` en páginas. Las pruebas de interfaz previas de la maqueta local no certifican el nuevo hosting. Pendiente comprobar disponibilidad real de Pages, carga de recursos remotos y navegación en navegador.

## Funcionalidades

Se conserva ATZ-NAV-001 original, Smart Guide, Braces Studio, galería, llamada y selector de idioma. WhatsApp desactivado hasta confirmar vigencia. Motion avanzado, traducciones completas, contenido clínico, fuentes y validación editorial pendientes. `client_ready:false`. No se declara etapa 08 cerrada.

## Decisión de aceptación visual — 17/11/2026

**Diseño V1 rechazado por el usuario: no representa el estándar ATREZZO Design in Motion.** No utilizar como referencia estética ni como diseño aprobado. Se conserva la arquitectura y el código funcional verificable, no la composición visual. El cumplimiento de rutas no equivale a cumplimiento creativo. El handoff ya rechazaba la estética template y exigía cinco actos editoriales, fotografía narrativa, retícula asimétrica, familias diferenciadas y motion real. La V1 no satisface ese criterio: bloques estáticos convencionales, ritmo tipográfico y fotográfico insuficiente, jerarquía y narrativa sin desarrollo, únicamente ATZ-NAV-001 integrado; motion narrativo pendiente. La evidencia local de portada muestra además un retrato no renderizado. La preview queda como versión rechazada, no como versión para cliente. La etapa 08 permanece ABIERTA; no avanzar a etapa 09 ni publicación definitiva. La siguiente construcción debe intervenir las familias visuales y el motion desde la dirección aprobada, preservar rutas/identidad/funcionalidades y verificarse integralmente antes de presentar otra entrega. No repetir etapas 01–07 ni solicitar aprobación de un hero aislado.

## Rectificación de alcance del rechazo — 17/11/2026

**RECHAZO INTEGRAL DE LA IMPLEMENTACIÓN V1.0.** El usuario aclara expresamente que no considera correcto nada de lo creado: percibe un retroceso frente al website original, sin elegancia ni Design in Motion. Esta decisión sustituye cualquier interpretación anterior de aceptación parcial. Ninguna interfaz, funcionalidad, traducción, composición ni código de V1 se considera aprobado por el usuario. La arquitectura y los requisitos de las etapas 01–07 siguen vigentes como decisiones del proyecto, no como aprobación de su implementación en V1. El código V1 se mantiene en el historial únicamente como evidencia técnica; cualquier reutilización exige comprobar su fidelidad a los requisitos originales, no se presume válida. No presentar la preview V1 al cliente ni invertir más trabajo en maquillar esa implementación. La etapa 08 permanece abierta y la construcción deberá partir del handoff aprobado, con el website original como umbral mínimo de calidad, integración verificable de los motores ATREZZO y control de calidad visual y funcional integral. No se ha efectuado aún una reconstrucción ni se ha desactivado el hosting con este cambio documental.

## Cambio de alcance autorizado — portal + dos websites (17/11/2026)

El usuario revoca la unificación anterior: recuperar la entrada histórica con dos mitades de igual protagonismo, APEL Ortodoncia y APEL Dental, reinterpretadas visualmente con elegancia contemporánea 2026. Cada entrada conduce a un website independiente, con su propio inicio, menú, identidad intacta y recorrido. El portal es exclusivamente de elección, no una tercera marca. Mantener idiomas ES/EN/DE, acceso directo entre unidades, contenido auténtico y funciones pertinentes. La estructura anterior de 36 IDs/108 rutas deja de ser una cifra obligatoria por este cambio confirmado; elaborar mapa separado con trazabilidad y redirecciones antes de implementar. Exclusividad de biblioteca ATREZZO: no importar patrones de otras fuentes ni reconstruir efectos. Consultar registro vigente, ficha y demo; importar archivos y runtime exactos, comprobar hashes y fidelidad visual/funcional. Composición estática, contenido y accesibilidad propios de APEL; ningún motor o interacción visual inventada. Si falta un patrón exacto, declararlo y no simularlo. V1 continúa rechazada. Esta actualización es documental: no se ha modificado la implementación ni publicado una nueva versión.

## V2 · Gate de entrada y procedencia — 17/11/2026

**Fase activa: 08 — EN PROCESO.** Rama local `design/apel-v2-codex`, desde `main` en `7814c46b75253e6878360626e3e70238616ef81e`. El único cambio frente a la base citada por el contrato es la incorporación del gate de arranque a `AGENTS.md`. El árbol inicial fue verificado limpio.

### Trabajo realizado y verificado

- El verificador del handoff y la comprobación del manifiesto SHA-256 pasaron. Se confirmaron 47 originales, 47 IDs propuestos, 141 rutas sin duplicados, 3.942 nodos y 376 recursos inventariados. Cada nodo del inventario se cotejó por posición, etiqueta, texto normalizado y SHA-256 con el HTML original.
- Se cotejaron los alias de inicio por orden, contenido, enlaces y medios. Se registraron las diferencias de ambos perfiles cruzados, los datos de contacto divergentes y las referencias a recursos sin recuperación. Existe un borrador privado de clasificación por nodo con los originales intactos. Faltan reconciliación y secciones de destino definitivas, traducciones EN/DE y selección de medios y encuadres por página.
- Se verificó el catálogo y se exportaron los siete IDs de la partitura desde `9ee01f9e4de7208e0f1ec16882239b9124e68f78`, con el blob de registro previsto. Se cotejaron los archivos exportados byte por byte y se registraron guías, licencias y huellas. `client_ready:false`.
- Las siete demos originales pasaron las comprobaciones específicas en Chrome a 375, 768, 1024 y 1440 px. Las comprobaciones incluyen Split multipágina y retroceso, teclado del menú, scroll de ida y vuelta en ambas escenas narrativas, foco de microinteracciones y visibilidad del texto animado. El `npm test` global del catálogo sí se detuvo en `tests/brand-contract.mjs` por la huella del favicon del propio catálogo. Esta prueba es independiente de los archivos que exportó APEL.
- El borrador y la evidencia de catálogo se conservan localmente en `qa/v2-preflight/` del paquete privado.

### Pendiente y restricciones de entrega

La construcción V2, el build y las pruebas en páginas cliente están pendientes. No existe PR ni preview V2. El repositorio APEL sigue público según GitHub. La transferencia de material del cliente requiere verificar destino privado y acceso autorizado. Las fuentes, matrices sensibles y comparativas con material privado permanecen fuera de Git y del webroot.

**Siguiente acción:** completar en local el master editorial ES/EN/DE y la partitura por página para iniciar el piloto de integración.

## V2 · Compilación privada navegable — 17/11/2026

**Fase activa: 08 — EN PROCESO.** Compilación local de portal y ambos websites, con 47 páginas canónicas y 141 rutas ES/EN/DE. El código V2 está en `v2/`. El build de revisión está en `qa/v2-review/` del paquete privado. Las fuentes y las evidencias están fuera del webroot y de Git.

- Master por página y partitura de las 47 páginas en `qa/v2-editorial/`. El borrador enlaza 871 IDs de texto a DOM y conserva el inventario completo de 3.942 nodos con razones y trazabilidad preliminares. 587 traducciones únicas por idioma generadas localmente; DE por pivote EN. Pendiente revisión clínica y editorial, cotejo completo de fuentes y terminología.
- Cuatro IDs integrados desde archivos exactos: ATZ-PGT-002, ATZ-NAV-001, ATZ-SEC-004 y ATZ-SEC-007. El modo reducido original del Handoff se activa también a 760 px o menos para mantener el flujo normal en móvil. Los tres IDs opcionales de la matriz sin escena aplicada siguen en modo estático. 14 derivados WebP, dos logos de bytes intactos y Poppins/Lora servidas localmente bajo OFL.
- 141/141 rutas verificadas estáticamente, también bajo prefijo. El verificador detectó deliberadamente la eliminación de un bloque, una traducción ausente y un enlace roto. 64 comprobaciones Chromium pasaron: portal a ambas Home, teclado y Escape, scroll inicial/intermedio/final/inverso, fallbacks sin JS y con movimiento reducido, familias representativas en alemán y FAQ, galería, guía y ligas. Se conservaron capturas comparadas del portal y las Home en `qa/v2-client/`; `client_ready:false`.
- Pendientes: validación semántica y clínica de la cobertura y traducciones, revisión visual y de fidelidad integral por familia, WebKit, zoom, dispositivos, contacto, derechos de publicación y privacidad. La guía local es un selector de navegación y las ligas usan una paleta de demostración. No hay PR ni publicación; el remoto APEL sigue público según la verificación de entrada.

**Siguiente acción:** cotejar editorialmente el master navegable con las fuentes y variantes ES/EN/DE, empezando por implantes, infantil, perfiles André/David y FAQ/SOS.

## V2 · Preview pública autorizada para revisión — 17/11/2026

La autorización expresa para GitHub Pages sustituye la restricción de visibilidad de la preview. El dominio oficial y su DNS quedan fuera de esta intervención. Etapa 08 en validación integral, pendiente de aceptación.

- Compilación estática del commit V2 `458ec143c6f8245f2f90bfc445c8625c5f9e3884`, con las 141 rutas bajo `/apel-ortodoncia`. Se conservan las advertencias visibles de revisión clínica y de traducción. Se aplicó la corrección aprobada de la mención a Brident en el texto público.
- Se cotejaron procedencia y consentimiento general documentado para fotos originales de clínica y equipo. Tres fotos de procedimientos se cambiaron por los retratos correspondientes del directorio original. Otras dos imágenes se sustituyeron por originales sin radiografía ni documentación visible. Se incluyeron 14 fotos y dos logos, sin material de pacientes identificado en la revisión. Los archivos privados y las evidencias quedan fuera de Pages.
- Se conservaron los motores ATREZZO originales y el historial V1. La revisión pública no certifica contenido clínico, traducciones ni la aprobación del website definitivo.
