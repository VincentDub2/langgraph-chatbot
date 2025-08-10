from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List, Dict, Optional
from uuid import uuid5, NAMESPACE_DNS
import os
import re
from tools.check_availability import _mock_busy, _overlaps

TZ = ZoneInfo("Europe/Rome")

# --- Registry mémoire (fake DB) ---
_EVENTS: Dict[str, Dict] = {}                 # event_id -> event dict
_AGENT_BUSY_EXTRA: Dict[str, List[tuple]] = {}  # agent_id -> list[(start_dt, end_dt)]

# --- Exceptions métier ---
class EventConflictError(Exception):
    """Le créneau demandé chevauche un événement occupé (mock ou déjà créé)."""

class BadRequestError(Exception):
    """Paramètre invalide ou manquant."""

# --- Utilitaires ---
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _norm_dt(dt: str | datetime) -> datetime:
    if isinstance(dt, datetime):
        d = dt
    else:
        # supporte "2025-08-12T14:00:00+02:00" ou UTC "Z" ou naive
        d = datetime.fromisoformat(dt.replace("Z", "+00:00")) if isinstance(dt, str) else dt
    if d.tzinfo is None:
        d = d.replace(tzinfo=TZ)
    return d.astimezone(TZ)

def _validate_attendees(attendees: List[Dict]) -> List[Dict]:
    norm = []
    for a in attendees or []:
        email = a.get("email")
        name = a.get("name") or ""
        if email and not _EMAIL_RE.match(email):
            raise BadRequestError(f"Email invalide: {email}")
        norm.append({"email": email, "name": name})
    return norm

def _ensure_agent_registry(agent_id: str):
    if agent_id not in _AGENT_BUSY_EXTRA:
        _AGENT_BUSY_EXTRA[agent_id] = []

def _existing_busy_for_agent(agent_id: str) -> List[tuple]:
    # Combine les busy “mock” de la journée + les events déjà créés pour l’agent
    busy = []
    # 1) mock occupé (même logique que check_availability)
    #    On ne peut pas appeler _mock_busy pour chaque jour sans date, donc on le fera à la volée:
    return busy

def _collect_busy(agent_id: str, start: datetime, end: datetime) -> List[tuple]:
    """Construit la liste des plages occupées (mock + events déjà créés) pour la période concernée."""
    busy = []
    # Mock occupé jour par jour (réutilise _mock_busy si présent dans ton module)
    day_cursor = start.replace(hour=0, minute=0, second=0, microsecond=0)
    while day_cursor < end:
        try:
            # suppose que _mock_busy(agent_id, day_cursor) est défini dans le module précédent
            busy.extend(_mock_busy(agent_id, day_cursor))
        except NameError:
            # si _mock_busy n'existe pas dans ce module, on n'ajoute rien (toujours OK pour la démo)
            pass
        day_cursor += timedelta(days=1)
    # Événements déjà créés (mémoire)
    for ev in _EVENTS.values():
        if ev["agent_id"] != agent_id:
            continue
        busy.append((ev["start_dt"], ev["end_dt"]))
    return busy

def _to_ics_dt(dt: datetime) -> str:
    # format UTC en ICS: YYYYMMDDTHHMMSSZ
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y%m%dT%H%M%SZ")

def _make_ics_content(event: Dict) -> str:
    uid = event["event_id"] + "@demo.local"
    dtstamp = _to_ics_dt(datetime.now(TZ))
    dtstart = _to_ics_dt(event["start_dt"])
    dtend = _to_ics_dt(event["end_dt"])
    summary = event["title"]
    location = event["location"] or ""
    description = event["description"] or ""
    attendees = ""
    for a in event["attendees"]:
        if a.get("email"):
            cn = a.get("name") or ""
            attendees += f"\nATTENDEE;CN={cn}:mailto:{a['email']}"
    ics = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Chatbot Demo//EN\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:PUBLISH\n"
        "BEGIN:VEVENT\n"
        f"UID:{uid}\n"
        f"DTSTAMP:{dtstamp}\n"
        f"DTSTART:{dtstart}\n"
        f"DTEND:{dtend}\n"
        f"SUMMARY:{summary}\n"
        f"LOCATION:{location}\n"
        f"DESCRIPTION:{description}\n"
        f"STATUS:CONFIRMED{attendees}\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )
    return ics

def _write_ics_file(event_id: str, ics_content: str, folder: Optional[str] = None) -> str:
    folder = folder or os.path.join(os.getcwd(), "ics_out")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{event_id}.ics")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ics_content)
    # URL de fichier local pour la démo
    return f"file://{path}"

# --- API publique ---
def create_event(
    agent_id: str,
    start: str | datetime,
    end: str | datetime,
    title: str,
    attendees: Optional[List[Dict]] = None,
    location: Optional[str] = None,
    description: Optional[str] = None,
    allow_conflict: bool = False,
) -> Dict:
    """
    Crée un événement (fake) si le créneau est libre.
    Retour: { event_id, ics_url, start_iso, end_iso, agent_id }
    - Lève EventConflictError si conflit (sauf allow_conflict=True).
    - Lève BadRequestError si params invalides.
    """
    if not title or len(title.strip()) < 3:
        raise BadRequestError("Title requis (>=3 caractères).")

    start_dt = _norm_dt(start)
    end_dt = _norm_dt(end)
    if end_dt <= start_dt:
        raise BadRequestError("end doit être > start.")
    if (end_dt - start_dt) < timedelta(minutes=15):
        raise BadRequestError("Durée minimale 15 minutes.")

    atts = _validate_attendees(attendees or [])
    _ensure_agent_registry(agent_id)

    # Conflits
    busy = _collect_busy(agent_id, start_dt, end_dt)
    conflicts = [(b_s, b_e) for (b_s, b_e) in busy if _overlaps(start_dt, end_dt, b_s, b_e)]
    if conflicts and not allow_conflict:
        # On expose le premier conflit pour “faire vrai”
        b_s, b_e = conflicts[0]
        raise EventConflictError(
            f"Créneau indisponible: chevauchement {b_s.isoformat()}–{b_e.isoformat()}"
        )

    # Crée l'enregistrement fake
    payload_for_id = f"{agent_id}|{start_dt.isoformat()}|{end_dt.isoformat()}|{title}|{location or ''}"
    event_id = str(uuid5(NAMESPACE_DNS, payload_for_id))

    event = {
        "event_id": event_id,
        "agent_id": agent_id,
        "title": title.strip(),
        "start_dt": start_dt,
        "end_dt": end_dt,
        "attendees": atts,
        "location": location or "",
        "description": description or "",
        "created_at": datetime.now(TZ),
        "source": "calendar:mock",
    }

    # Ajoute à la "DB"
    _EVENTS[event_id] = event
    _AGENT_BUSY_EXTRA[agent_id].append((start_dt, end_dt))

    # ICS
    ics = _make_ics_content(event)
    ics_url = _write_ics_file(event_id, ics)

    return {
        "event_id": event_id,
        "ics_url": ics_url,
        "start_iso": start_dt.isoformat(),
        "end_iso": end_dt.isoformat(),
        "agent_id": agent_id,
    }

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    # Cas nominal
    try:
        res = create_event(
            agent_id="AGENT_42",
            start="2025-08-12T10:00:00+02:00",
            end="2025-08-12T10:45:00+02:00",
            title="Visite REF-123",
            attendees=[{"email": "client@example.com", "name": "Client Demo"}],
            location="12 Via Torino, Milano",
            description="Premier contact, apporter pièce d'identité.",
        )
        print("✅ Event créé:", res)
    except EventConflictError as e:
        print("⛔ Conflit:", e)

    # Tentative volontaire sur un créneau probablement occupé (déclenche une erreur réaliste)
    try:
        res2 = create_event(
            agent_id="AGENT_42",
            start="2025-08-12T11:00:00+02:00",
            end="2025-08-12T11:45:00+02:00",
            title="Visite REF-456",
        )
        print("✅ Event créé:", res2)
    except EventConflictError as e:
        print("⛔ Conflit:", e)
