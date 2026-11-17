"""Scene copy and media choices for the two APEL editorial journeys."""

# Titles preserve the original three-line and two-line ATREZZO hierarchies.
ORTHO_CHAPTERS = (
    (
        "o-chair", "o-concepto",
        (("Un plan", "para", "cada caso"), ("A plan", "for", "each case"), ("Ein Plan", "für", "Ihren Fall")),
        ("Consulta, diagnóstico y planificación del tratamiento.",
         "Consultation, diagnosis and treatment planning.",
         "Beratung, Diagnostik und Behandlungsplanung."),
    ),
    (
        "o-standing", "o-andre",
        (("Estudio", "y", "práctica"), ("Study", "and", "practice"), ("Studium", "und", "Praxis")),
        ("Formación en Rostock y trayectoria del Dr. Carlos André Apel.",
         "Dr Carlos André Apel’s training in Rostock and professional background.",
         "Ausbildung in Rostock und beruflicher Werdegang von Dr. Carlos André Apel."),
    ),
    (
        "o-reception", "o-instalaciones",
        (("Tu visita", "a nuestra", "clínica"), ("Your visit", "to our", "clinic"), ("Ihr Besuch", "in unserer", "Praxis")),
        ("Conoce los espacios de atención de APEL Ortodoncia.",
         "See the treatment facilities at APEL Orthodontics.",
         "Lernen Sie die Räume der kieferorthopädischen Praxis kennen."),
    ),
)
DENTAL_CHAPTERS = (
    (
        "d-standing", "d-veronica",
        (("Formación", "y experiencia"), ("Training", "and experience"), ("Ausbildung", "und Erfahrung")),
        ("La trayectoria de la Dra. Verónica de Apel, de El Salvador a Alemania.",
         "Dr Verónica de Apel’s professional background, from El Salvador to Germany.",
         "Der Werdegang von Dr. Verónica de Apel, von El Salvador nach Deutschland."),
    ),
    (
        "d-room", "d-clinica",
        (("Tu visita", "a APEL Dental"), ("Your visit", "to APEL Dental"), ("Ihr Besuch", "bei APEL Dental")),
        ("Conoce la clínica y los espacios donde el equipo atiende.",
         "Explore the clinic and its treatment rooms.",
         "Lernen Sie die Praxis und ihre Behandlungsräume kennen."),
    ),
)

PORTRAITS = {
    "o-andre": "o-office",
    "d-veronica": "d-veronica",
    "d-minerva": "d-minerva",
    "d-david": "d-david",
    "d-jaime": "d-jaime",
    "d-mirna": "d-mirna",
}
