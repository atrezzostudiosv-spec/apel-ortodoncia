# APEL — Instrucciones de ejecución para Codex

## Estado obligatorio
Leer ATREZZO-PROJECT-STATUS.md antes de editar. La implementación V1 está rechazada integralmente. Fase 08 abierta. El alcance vigente es portal dividido (Dental izquierda, Ortodoncia derecha) y dos websites independientes, ES/EN/DE. No usar la V1 ni el blueprint unificado como diseño aprobado.

## Gate de arranque
No empezar la construcción sin acceso efectivo al paquete privado APEL-CODEX-HANDOFF-V2.zip, su AGENTS.md específico, los cuatro protocolos maestros, DECISIONES-VIGENTES.md, CONTRATO-CODEX.md, partitura, matrices de contenido y fuentes originales. El paquete es material de trabajo privado: no está subido a este repositorio público. Ejecutar su scripts/verify_intake.py. No sustituir originales por copy resumido de V1, no inventar datos. Si falta acceso, registrar el bloqueo en vez de generar una plantilla.

## Componentes
Biblioteca única: https://github.com/atrezzostudiosv-spec/atrezzo-repositorio
Registro: registry/components.json. Commit consultado: 9ee01f9e4de7208e0f1ec16882239b9124e68f78. Verificar ID, ficha, demo, archivos originales y runtime; comprobar hash, licencias y fidelidad visual y funcional en destino. No recrear ni importar efectos externos. Composición estática y controles funcionales nativos cuando no exista un ID adecuado, sin motion inventado. No modificar la biblioteca.

## Construcción y entrega
Main es fuente de verdad; inspeccionar HEAD actual y trabajar en design/apel-v2-codex con PR revisable hacia main. No tocar la preview rechazada ni desplegar hasta revisión. Mantener decisiones cerradas salvo nuevo alcance confirmado. Construcción integral, no hero aislado, no plantilla genérica. Completar contenido y traducciones, partitura y QA de navegador, responsive, movimiento y accesibilidad. Registrar evidencia y pendientes en ATREZZO-PROJECT-STATUS.md. No declarar fase cerrada sin aceptación integral del usuario.

## Privacidad
No subir ZIP maestros, originales, inventarios sensibles, fotografías clínicas, pacientes identificables, datos privados ni material no autorizado al repositorio público. Noindex no equivale a privacidad. Verificar acceso privado y autorización antes de transferir contenido del cliente; no activar Pages ni cambiar dominio/DNS. Mantener los originales fuera de Git y del webroot aun en privado.
