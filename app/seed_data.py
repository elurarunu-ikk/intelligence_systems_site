import os
import sqlite3
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

def _sqlite_file_from_uri(uri: str):
    # sqlite:///instance/site.db  -> instance/site.db
    # sqlite:////var/data/site.db -> /var/data/site.db
    if not uri.startswith("sqlite:"):
        return None
    if uri.startswith("sqlite:////"):
        return uri.replace("sqlite:////", "/")
    return uri.replace("sqlite:///", "")

def seed_if_empty(app):
    """
    Seeds SQLite DB from seed/seed.sql if DB is empty.
    Runs only when env var SEED_DEMO=1.
    """
    if os.getenv("SEED_DEMO", "0") != "1":
        return

    with app.app_context():
        db.create_all()

        # If any table already has data -> skip
        for t in TABLES_TO_CHECK:
            try:
                n = db.session.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar() or 0
                if n > 0:
                    print(f"Seed skip: '{t}' already has {n} rows")
                    return
            except Exception:
                pass

        seed_path = os.path.abspath(os.path.join(app.root_path, "..", "seed", "seed.sql"))
        if not os.path.exists(seed_path):
            print("Seed file missing:", seed_path)
            return

        uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        db_path = _sqlite_file_from_uri(uri)

        if not db_path:
            print("Seed: non-sqlite DB or invalid URI, skipping.")
            return

        # Make relative sqlite path relative to project root
        if not os.path.isabs(db_path):
            project_root = os.path.abspath(os.path.join(app.root_path, ".."))
            db_path = os.path.join(project_root, db_path)

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        sql = open(seed_path, "r", encoding="utf-8").read()

        # Only INSERT statements (avoid schema conflicts)
        inserts = []
        for line in sql.splitlines():
            s = line.strip()
            if s.upper().startswith("INSERT INTO"):
                inserts.append(line)
        insert_sql = "\n".join(inserts)

        if not insert_sql.strip():
            print("Seed: no INSERT statements found.")
            return

        conn = sqlite3.connect(db_path)
        try:
            conn.execute("PRAGMA foreign_keys=OFF;")
            conn.executescript("BEGIN;\n" + insert_sql + "\nCOMMIT;")
            print("✅ Seeded demo data into:", db_path)
        finally:
            conn.close()
