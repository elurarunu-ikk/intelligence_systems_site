from app import create_app
from app.extensions import db
from app.models import SiteSettings, Program, Page, PlacementStat, MoU

app = create_app()

with app.app_context():
    s = SiteSettings.query.first()
    s.phone = "+91-XXXXXXXXXX"
    s.enquiry_email = "intelligencesystems@saveetha.edu.in"
    s.tagline = "Shaping Intelligent Systems for a Smarter Future"

    # Programs
    if Program.query.count() == 0:
        db.session.add_all([
            Program(level="UG", name="B.Tech – Intelligence Systems", duration="Editable", eligibility="Editable"),
            Program(level="PG", name="M.Tech – Intelligence Systems", duration="Editable", eligibility="Editable"),
            Program(level="Research", name="Ph.D – Intelligence Systems", duration="Editable", eligibility="Editable"),
        ])

    # About page
    if not Page.query.filter_by(slug="about").first():
        db.session.add(Page(slug="about", title="About the Department", body_html="<p>Edit this content from the CMS.</p>"))

    # Placement stats
    if PlacementStat.query.count() == 0:
        db.session.add_all([
            PlacementStat(label="Highest Package", value="Editable"),
            PlacementStat(label="Average Package", value="Editable"),
            PlacementStat(label="Placement Rate", value="Editable"),
            PlacementStat(label="Internship Partners", value="Editable"),
        ])

    # MoU
    if MoU.query.count() == 0:
        db.session.add(MoU(partner_name="Editable Industry Partner", area="MoU / Collaboration"))

    db.session.commit()
    print("Seed complete.")
