import re
import unicodedata

from app.schemas.support import AnalysisResult


CONFIRMED_INCIDENT = re.compile(
    r"\b(?:ransomware|(?:filtracion|fuga|robo)(?: activa)? de (?:datos|credenciales|informacion)|"
    r"(?:se filtran|han filtrado|estan filtrando) (?:datos|credenciales|informacion)|"
    r"(?:credenciales|contrasenas|tokens?|claves? (?:privadas?|de api)|datos personales) "
    r"(?:(?:fueron|estan|quedaron) )?(?:filtrad[oa]s?|expuest[oa]s?|publicad[oa]s?)|"
    r"(?:atacante|intruso) (?:tiene|tomo) (?:el )?control)\b"
)

SECURITY = re.compile(
    r"\b(?:vulnerabilidad(?:es)?|phishing|malware|intrusion(?:es)?|"
    r"hackeo|hackead[oa]s?|brecha de seguridad|incidente de seguridad|"
    r"accesos? (?:no autorizados?|sospechosos?)|actividad sospechosa|"
    r"(?:inicio(?:s)?|intentos?) de sesion sospechosos?|"
    r"(?:accedieron|entraron) (?:a|en) (?:mi|nuestra) cuenta|"
    r"(?:cuenta|servidor|sistema) comprometid[oa]|"
    r"(?:ver|acceder a) (?:los )?datos de otros (?:clientes|usuarios)|"
    r"correo(?:s)? sospechoso(?:s)?|suplantacion|inyeccion sql|xss)\b"
)

FEATURE = re.compile(
    r"\b(?:nueva (?:funcion|funcionalidad|opcion)|solicitud de mejora|"
    r"sugiero|sugerencia|(?:quisiera|queremos|podrian|podriamos|seria util|seria bueno) "
    r"(?:que (?:se )?)?(?:agregar\w*|anadir\w*|permitir\w*|incorporar\w*|"
    r"incluir\w*|habilitar\w*|poder|tener|implementar\w*))\b"
)

ACCESS = re.compile(
    r"\b(?:iniciar sesion|inicio de sesion|login|contrasena|credenciales invalidas|"
    r"credenciales incorrectas|cuenta (?:(?:esta|quedo|fue) )?bloqueada|bloqueo de cuenta|"
    r"acceso denegado|sin permisos|permisos insuficientes|autenticacion|"
    r"no (?:puedo|podemos|logro) (?:acceder|entrar|ingresar))\b"
)

TOTAL_OUTAGE = re.compile(
    r"\b(?:caida (?:total|general)|produccion (?:detenida|paralizada)|"
    r"(?:todo el sistema|toda la plataforma) (?:esta )?(?:caid[oa]|inaccesible)|"
    r"(?:sistema|plataforma)(?: de produccion)? (?:esta )?(?:totalmente|por completo) (?:caid[oa]|inaccesible)|"
    r"(?:nadie|ningun usuario) puede (?:trabajar|usar (?:el sistema|la plataforma))|"
    r"perdida masiva de datos)\b"
)

WIDE_IMPACT = re.compile(
    r"\b(?:servicio (?:caido|no disponible)|sistema caido|plataforma caida|"
    r"(?:varios|muchos|todos los) usuarios|todo el equipo|"
    r"bloquea (?:el trabajo|la operacion)|no (?:puedo|podemos) trabajar)\b"
)

RESPONSES = {
    "ACCESS": "Verifique que utiliza la cuenta correcta y, si es necesario, use el proceso oficial de recuperación de acceso. Si el problema continúa, indique a soporte el mensaje que aparece sin compartir su contraseña.",
    "BUG": "Gracias por reportar el problema. Indique qué función falla, qué pasos siguió y el mensaje de error para que soporte pueda revisarlo.",
    "FEATURE": "Gracias por su sugerencia. Cuéntenos qué tarea facilitaría la función y cómo la usaría para que el equipo de producto pueda evaluar la propuesta.",
    "SECURITY": "Gracias por avisar. El caso requiere revisión del equipo de seguridad. Informe cuándo observó el incidente y por qué canal ocurrió. Use el canal oficial y evite compartir contraseñas o claves.",
}


def normalize(message: str) -> str:
    text = unicodedata.normalize("NFKD", message.casefold())
    unaccented = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(unaccented.split())


def has_security_signal(message: str) -> bool:
    text = normalize(message)
    return bool(CONFIRMED_INCIDENT.search(text) or SECURITY.search(text))


def classify(message: str) -> AnalysisResult:
    text = normalize(message)
    confirmed_incident = bool(CONFIRMED_INCIDENT.search(text))
    requires_review = confirmed_incident or bool(SECURITY.search(text))
    if requires_review:
        category = "SECURITY"
        priority = "CRITICAL" if confirmed_incident else "HIGH"
    elif FEATURE.search(text):
        category, priority = "FEATURE", "LOW"
    else:
        category = "ACCESS" if ACCESS.search(text) else "BUG"
        if TOTAL_OUTAGE.search(text):
            priority = "CRITICAL"
        elif WIDE_IMPACT.search(text):
            priority = "HIGH"
        else:
            priority = "MEDIUM"

    return AnalysisResult(
        category=category,
        priority=priority,
        response=RESPONSES[category],
        requiresHumanReview=requires_review,
    )
