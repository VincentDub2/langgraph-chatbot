from __future__ import annotations
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
import re
import hashlib
from typing import List, Dict, Tuple, Optional

TZ = ZoneInfo("Europe/Rome")

# --- Fenêtre de recherche ---
def _parse_window(window: str, now: Optional[datetime] = None) -> Tuple[datetime, datetime, Optional[str]]:
    """
    window exemples:
      - "today", "tomorrow", "next 7 days"
      - "2025-08-12"
      - ajoute: "morning" | "afternoon"  (ex: "tomorrow afternoon", "2025-08-12 morning")
    Retourne (start_dt, end_dt, daypart)
    """
    now = (now or datetime.now(TZ)).replace(minute=0, second=0, microsecond=0)
    w = window.strip().lower()

    daypart = None
    if "morning" in w:
        daypart = "morning"
        w = w.replace("morning", "").strip()
    elif "afternoon" in w:
        daypart = "afternoon"
        w = w.replace("afternoon", "").strip()

    if w in ("today", ""):
        start = now.replace(hour=0)
        end = (start + timedelta(days=1))
    elif w == "tomorrow":
        start = (now + timedelta(days=1)).replace(hour=0)
        end = (start + timedelta(days=1))
    elif m := re.match(r"next\s+(\d+)\s+days", w):
        n = int(m.group(1))
        start = now
        end = now + timedelta(days=n)
    elif re.match(r"\d{4}-\d{2}-\d{2}$", w):
        d = datetime.fromisoformat(w).replace(tzinfo=TZ)
        start = d.replace(hour=0)
        end = start + timedelta(days=1)
    else:
        # fallback: 7 jours
        start = now
        end = now + timedelta(days=7)

    return start, end, daypart

# --- Horaires de travail ---
def _working_blocks(day: datetime, daypart: Optional[str]) -> List[Tuple[datetime, datetime]]:
    """
    Retourne les blocs de travail du jour (matin/après-midi ou les deux).
    """
    if day.weekday() >= 5:  # 5=Sam, 6=Dim
        return []

    morning = (day.replace(hour=9), day.replace(hour=12))
    afternoon = (day.replace(hour=14), day.replace(hour=18))

    if daypart == "morning":
        return [morning]
    if daypart == "afternoon":
        return [afternoon]
    return [morning, afternoon]

# --- Ocupations simulées (déterministes) ---
def _mock_busy(agent_id: str, day: datetime) -> List[Tuple[datetime, datetime]]:
    """
    Simule 0-2 événements occupés par jour, déterministes via hash(agent_id+date).
    """
    seed_src = f"{agent_id}:{day.date().isoformat()}".encode()
    h = hashlib.sha256(seed_src).hexdigest()
    # Utilise quelques octets du hash pour décider
    k1, k2 = int(h[:2], 16), int(h[2:4], 16)
    busy = []

    def clamp_hour(x: int, lo: int, hi: int) -> int:
        return max(lo, min(hi, x))

    # Event 1 (matin) ~50% de chance
    if k1 % 4 in (0, 1):  # 50%
        start_h = clamp_hour(9 + (k1 % 3), 9, 11)  # 9..11
        s = day.replace(hour=start_h, minute=0)
        busy.append((s, s + timedelta(minutes=45)))

    # Event 2 (aprem) ~50% de chance
    if k2 % 4 in (0, 1):  # 50%
        start_h = clamp_hour(14 + (k2 % 3), 14, 17)  # 14..17
        s = day.replace(hour=start_h, minute=0)
        busy.append((s, s + timedelta(minutes=45)))

    return busy

def _overlaps(s1: datetime, e1: datetime, s2: datetime, e2: datetime) -> bool:
    return not (e1 <= s2 or e2 <= s1)

# --- Génération de slots ---
def _generate_slots_for_day(agent_id: str, day: datetime, daypart: Optional[str]) -> List[Dict]:
    slots = []
    busy = _mock_busy(agent_id, day)
    for block_start, block_end in _working_blocks(day, daypart):
        # Créneaux de 45 minutes, départ à H:00 uniquement (sobre pour la démo)
        start = block_start
        while start + timedelta(minutes=45) <= block_end:
            end = start + timedelta(minutes=45)
            is_free = all(not _overlaps(start, end, b_s, b_e) for b_s, b_e in busy)
            slots.append({
                "start_iso": start.isoformat(),
                "end_iso": end.isoformat(),
                "duration_min": 45,
                "agent_id": agent_id,
                "timezone": "Europe/Rome",
                "is_available": bool(is_free),
                "source": "calendar:mock",
                "confidence": 0.82 if is_free else 0.7,
                "reason": None if is_free else "Busy event overlaps (mock)",
            })
            start += timedelta(hours=1)  # on avance d'une heure (créneau suivant)
    return slots

# --- API publique ---
def check_availability(agent_id: str, window: str) -> List[Dict]:
    """
    Retourne une liste de slots triés, avec 'is_available' True/False.
    Exemple d'entrée: "today", "tomorrow afternoon", "next 7 days", "2025-08-12 morning"
    """
    start, end, daypart = _parse_window(window)
    results: List[Dict] = []
    day = start.astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    while day < end:
        results.extend(_generate_slots_for_day(agent_id, day, daypart))
        day += timedelta(days=1)

    # Filtrer les slots passés si la fenêtre inclut "today"
    now = datetime.now(TZ)
    results = [s for s in results if datetime.fromisoformat(s["end_iso"]) > now]

    # Tri par start_iso puis dispo d'abord
    results.sort(key=lambda s: (s["start_iso"], not s["is_available"]))
    return results

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    demo = check_availability("AGENT_42", "next 3 days morning")
    # Affiche les 8 premiers slots pour aperçu
    for s in demo[:8]:
        mark = "✅" if s["is_available"] else "⛔"
        print(mark, s["start_iso"], "→", s["end_iso"])
