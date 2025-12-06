import os
import django
from fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Initialisation Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_conference.settings")
django.setup()

# Charger les modèles via le registre Django (évite les ImportError d'import direct)
from django.apps import apps
Conference = apps.get_model("conferenceApp", "Conference")
Session = apps.get_model("SessionApp", "Session")

# ===========================
# CREATE MCP SERVER
# ===========================
mcp = FastMCP("Conference Assistant")

# ------------------------------------------------------
# TOOL 1 : LISTER LES CONFÉRENCES
# ------------------------------------------------------
@mcp.tool(name="list_conferences", description="Liste toutes les conférences dans la base.")
async def list_conferences() -> str:
    """
    Liste toutes les conférences disponibles dans la base de données.
    Retour: liste formatée ou 'No conferences found.'
    """

    @sync_to_async
    def get_all():
        return list(Conference.objects.all())

    conferences = await get_all()

    if not conferences:
        return "No conferences found."

    return "\n".join(
        f"- {c.name} ({getattr(c, 'start_date', '')} \u2192 {getattr(c, 'end_date', '')})"
        for c in conferences
    )

# ------------------------------------------------------
# TOOL 2 : DÉTAILS D'UNE CONFÉRENCE
# ------------------------------------------------------
@mcp.tool(name="get_conference_details", description="Donne les détails d'une conférence par nom (recherche partielle).")
async def get_conference_details(name: str) -> str:
    """
    Renvoie les détails d'une conférence correspondant au nom fourni (recherche partielle insensible à la casse).
    Paramètres:
      - name (str)
    Retour:
      - Détails formatés
      - Messages d'erreur si multiple ou non trouvée
    """

    @sync_to_async
    def get_one():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    conf = await get_one()

    if conf == "MULTIPLE":
        return "Multiple conferences found, please be more specific."

    if not conf:
        return f"Conference '{name}' not found."

    theme = conf.get_theme_display() if hasattr(conf, "get_theme_display") else getattr(conf, "theme", "")
    description = getattr(conf, "description", None)
    location = getattr(conf, "location", "")
    start = getattr(conf, "start_date", "")
    end = getattr(conf, "end_date", "")

    lines = [
        f"Name: {conf.name}",
        f"Theme: {theme}",
        f"Location: {location}",
        f"Dates: {start} \u2192 {end}",
    ]
    if description:
        lines.append(f"Description: {description}")

    return "\n".join(lines)

# ------------------------------------------------------
# TOOL 3 : LISTER LES SESSIONS D'UNE CONFÉRENCE
# ------------------------------------------------------
@mcp.tool(name="list_sessions", description="Liste les sessions d'une conférence donnée.")
async def list_sessions(conference_name: str) -> str:
    """
    Liste les sessions associées à une conférence.
    Paramètres:
      - conference_name (str)
    Retour:
      - Liste formatée ou messages d'erreur
    """

    @sync_to_async
    def get_sessions():
        try:
            conf = Conference.objects.get(name__icontains=conference_name)
            # Si related_name='sessions' existe, utilise-le, sinon fallback sur filter
            if hasattr(conf, "sessions"):
                return list(conf.sessions.all()), conf
            return list(Session.objects.filter(conference=conf)), conf
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    result, conf = await get_sessions()

    if result == "MULTIPLE":
        return "Multiple conferences found, be more specific."

    if conf is None:
        return f"Conference '{conference_name}' not found."

    if not result:
        return "No sessions found."

    return "\n".join(
        f"- {s.title} ({getattr(s, 'start_time', '')} \u2192 {getattr(s, 'end_time', '')}) in {getattr(s, 'room', '')}\n"
        f"  Topic: {getattr(s, 'topic', '')}"
        for s in result
    )

# ------------------------------------------------------
# TOOL 4 : RECHERCHER DES SESSIONS PAR THÈME
# ------------------------------------------------------
@mcp.tool(name="search_sessions_by_topic", description="Recherche des sessions par mot-clé de sujet (topic).")
async def search_sessions_by_topic(topic: str) -> str:
    """
    Recherche des sessions par sujet (topic), recherche partielle insensible à la casse.
    Paramètres:
      - topic (str)
    Retour:
      - Liste formatée des sessions
    """

    @sync_to_async
    def search():
        return list(
            Session.objects.filter(topic__icontains=topic).select_related("conference")
        )

    sessions = await search()

    if not sessions:
        return f"No sessions found for topic '{topic}'."

    return "\n".join(
        f"- {s.title}\n"
        f"  Conference: {getattr(s.conference, 'name', '')}\n"
        f"  Topic: {getattr(s, 'topic', '')}\n"
        f"  Time: {getattr(s, 'start_time', '')} \u2192 {getattr(s, 'end_time', '')}\n"
        f"  Room: {getattr(s, 'room', '')}"
        for s in sessions
    )

# ------------------------------------------------------
# LAUNCH
# ------------------------------------------------------
if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        # Graceful exit without noisy traceback on Ctrl+C
        pass