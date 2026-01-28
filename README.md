# Department of Intelligence Systems — Saveetha University (SIMATS) Website + Simple CMS

This project is a lightweight, editable department website built with **Flask + Bootstrap 5** and a **simple CMS** using **Flask-Admin**.

## Features
- SIMATS-aligned header + navigation
- CMS modules: Pages, Programs, Faculty, News, Events, Achievements, Funded Projects, MoUs, Placement Stats, Newsletter, Enquiries
- Admin authentication (Flask-Login)
- Editable placeholders for tagline, programs, placements, etc.

## Quick Start (Windows / Mac / Linux)
1) Create a virtual environment and install deps:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

2) Create a `.env` file (copy from example):
```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Mac/Linux
```

3) Run the site:
```bash
python run.py
```
Open: http://127.0.0.1:5000

## Admin Login
- Admin URL: http://127.0.0.1:5000/admin
- Default dev credentials come from `.env`:
  - `ADMIN_EMAIL`
  - `ADMIN_PASSWORD`

> Note: the app auto-creates the first admin user if none exist (dev-friendly). For production, use a proper user onboarding process.

## Content Setup Checklist (Recommended)
1. Admin → Settings → SiteSettings: update phone/email/address, hero text, tagline.
2. Admin → Programs: add UG/PG/Research.
3. Admin → Pages: create `about` page (slug: `about`) and add Aim & Scope content.
4. Admin → Faculty: add faculty profiles.
5. Admin → News / Events: add posts and upcoming events.
6. Admin → Placement Stats / MoUs: enable numbers later when ready.

## Production Notes (Recommended)
- Switch DB to PostgreSQL using `DATABASE_URL`
- Use Gunicorn + Nginx
- Set a strong `SECRET_KEY`
- Disable debug mode
