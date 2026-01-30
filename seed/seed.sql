import os
import sqlite3
from flask import current_app
from sqlalchemy import text
from .extensions import db


TABLES_TO_CHECK = [
    "site_settings",
    "page",
    "faculty",
    "gallery_album",
    "gallery_images",
    "hero_slides",
    "news",
    "event",
]


def _sqlite_file_from_uri(uri: str) -> str | None:
    # Expected formats:
    # sqlite:///instance/site.db   (relative)
    # sqlite:////abs/path/site.db  (absolute)
    if not uri.startswith("sqlite:"):
        return None

    path = uri.replace("sqlite:///", "", 1)
    path = path.replace("sqlite:////", "/", 1)  # safety for absolute unix paths
    return path


def seed_if_empty():
    """
    Seeds the SQLite DB from seed/seed.sql if the DB is empty.
    Enabled only when env var SEED_DEMO=1.
    """
    if os.getenv("SEED_DEMO", "0") != "1":
        return

    # Ensure tables exist
    with current_app.app_context():
        db.create_all()

        # If any of these tables already has rows, skip seeding
        for t in TABLES_TO_CHECK:
            try:
                n = db.session.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar() or 0
                if n > 0:
                    print(f"Seed skip: '{t}' already has {n} rows")
                    return
            except Exception:
                # Table may not exist yet; create_all should handle, but ignore and continue
                pass

        seed_path = os.path.abspath(os.path.join(current_app.root_path, "..", "seed", "seed.sql"))
        if not os.path.exists(seed_path):
            print("Seed file missing:", seed_path)
            return

        uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
        db_path = _sqlite_file_from_uri(uri)

        # For sqlite:///instance/site.db (relative), make it relative to project root
        if db_path and not os.path.isabs(db_path):
            project_root = os.path.abspath(os.path.join(current_app.root_path, ".."))
            db_path = os.path.join(project_root, db_path)

        if not db_path:
            print("Seed: non-sqlite DB or invalid URI, skipping seeding.")
            return

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        sql = open(seed_path, "r", encoding="utf-8").read()

        # Keep only INSERT lines (ignore CREATE TABLE, PRAGMA, etc.)
        lines = []
        for line in sql.splitlines():
            s = line.strip()
            if not s:
                continue
            upper = s.upper()
            if upper.startswith("INSERT INTO"):
                lines.append(line)
        insert_sql = "\n".join(lines)
        if not insert_sql.strip():
            print("Seed: no INSERT statements found in seed.sql")
            return

        conn = sqlite3.connect(db_path)
        try:
            conn.execute("PRAGMA foreign_keys=OFF;")
            conn.executescript("BEGIN;\n" + insert_sql + "\nCOMMIT;")
            print("✅ Seeded demo data into:", db_path)
        finally:
            conn.close()
