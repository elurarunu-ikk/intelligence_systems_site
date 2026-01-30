import os
from sqlalchemy import text
from .extensions import db

def seed_if_empty(app):
    seed_path = os.path.join(app.root_path, "..", "seed", "seed.sql")
    seed_path = os.path.abspath(seed_path)

    with app.app_context():
        db.create_all()

        # If already seeded, do nothing
        try:
            count = db.session.execute(text("SELECT COUNT(*) FROM faculty")).scalar() or 0
        except Exception:
            count = 0

        if count > 0:
            return

        if not os.path.exists(seed_path):
            print("Seed file not found:", seed_path)
            return

        sql = open(seed_path, "r", encoding="utf-8").read()
        db.session.execute(text("PRAGMA foreign_keys=OFF;"))
        for stmt in sql.split(";\n"):
            s = stmt.strip()
            if s:
                db.session.execute(text(s))
        db.session.commit()
        print("✅ Seeded demo data")
