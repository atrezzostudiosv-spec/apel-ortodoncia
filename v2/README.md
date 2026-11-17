# APEL V2 · Compilación local

Sitio estático. Python 3.11 o 3.12 y las dependencias fijadas en `requirements.txt`.
La entrada de producción es el paquete privado V2 verificado. Los textos, las fotos y las capturas de revisión residen fuera de este checkout.

```sh
python3 -m venv /tmp/apel-v2-build-venv
/tmp/apel-v2-build-venv/bin/python -m pip install -r v2/requirements.txt
/tmp/apel-v2-build-venv/bin/python v2/build.py --package "$APEL_PACKAGE" --fonts v2/fonts --output "$APEL_PREVIEW"
/tmp/apel-v2-build-venv/bin/python v2/verify.py --package "$APEL_PACKAGE" --output "$APEL_PREVIEW"
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$APEL_PREVIEW"
```

Usar rutas absolutas para `APEL_PACKAGE` y `APEL_PREVIEW`. El directorio de salida debe ser nuevo. La vista arranca en `http://127.0.0.1:8765/`. Servir únicamente la salida de build, con acceso local. El build con `--public-review --prefix /apel-ortodoncia` se puede incorporar al árbol público de Pages después de verificar los recursos autorizados.

La entrada que consulta el generador es `qa/v2-editorial/master-es.json`, `translations-draft.json` y `visual-plan.json` del paquete privado. Los exports y el registro con hashes se leen de `qa/v2-preflight/`. Los recursos referenciados se cotejan con el inventario de originales antes de generar derivados WebP. Los dos logos PNG se copian byte a byte. Poppins y Lora se sirven localmente con las licencias OFL en `fonts/`.

`--pilot` genera las nueve páginas localizadas de portal y de ambas Home. `--prefix /revision` ajusta rutas de navegación y recursos cuando un servidor monta la salida en esa subruta.

## Integración original

| ID | Uso | Adaptación |
|---|---|---|
| ATZ-PGT-002 | Portal → Dental u Ortodoncia | Preflight, runtime y CSS exactos. Dos enlaces HTML marcados. Colores de APEL. La llegada se resuelve desde el documento de destino. |
| Navegación estática nativa | Cabeceras visibles de ambas unidades | Grupos y submenús originales con `details/summary`, sin motor visual añadido. Se sustituye la integración del menú inmersivo según la corrección expresa del usuario. |
| ATZ-SEC-004 | Home Dental, secuencia de autoridad → clínica | Dos escenas, fotografías de archivo, rótulos localizados. En pantallas de hasta 760 px se utiliza el modo estático que ofrece el motor original. |
| ATZ-SEC-007 | Home Ortodoncia, tres capítulos | Fragmento de tres capítulos, imágenes de archivo, enlaces localizados y motor de scroll original. Fallback original integrado. |

Biblioteca fijada en `9ee01f9e4de7208e0f1ec16882239b9124e68f78`. La procedencia y licencias de los archivos están en el registro privado. Estado del build de revisión `client_ready:false`. Los borradores de traducción y los datos de contacto históricos requieren cotejo específico.

## Composición de la revisión

`composition.py` fija los textos de escena y las fotos de ambos recorridos. `navigation.py` fija los destinos de cabecera por unidad. Los títulos de escena se localizan por idioma conservando la jerarquía del fragmento ATREZZO.

La Home Dental incorpora los seis perfiles dentro de su escena de equipo. Las páginas interiores distinguen trayectoria profesional, directorio, clínica, catálogo, tratamiento, ayuda al paciente y contacto. El texto de origen conserva su ID al cambiar de ubicación.
