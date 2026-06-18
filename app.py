import os
from services.jd_parser import extract_jd_text
from flask import send_file
from reportlab.pdfgen import canvas
from database import get_all_candidates
from database import (
    init_db,
    create_job,
    get_latest_job,
    save_candidate,
    get_candidates,
    clear_candidates,
    get_dashboard_stats,
    get_candidate_by_id,
    get_resume_file
)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    send_file,
    send_from_directory
)

from werkzeug.utils import secure_filename

from config import Config



from services.parser import parse_resume
from services.skill_extractor import extract_skills
from services.matcher import calculate_match_score
from services.classifier import classify_candidate
from services.gap_analyzer import analyze_skills
app = Flask(__name__)

app.config.from_object(Config)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

os.makedirs(
    app.config["REPORT_FOLDER"],
    exist_ok=True
)

init_db()
def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in app.config["ALLOWED_EXTENSIONS"]
    )
@app.route("/")
def home():

    return render_template(
        "index.html"
    )
@app.route("/create-job")
def create_job_page():

    return render_template(
        "create_job.html"
    )
@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    return render_template(
        "dashboard.html",
        stats=stats
    )
@app.route("/upload")
def upload():

    return render_template(
        "upload_resume.html"
    )
@app.route(
    "/save-job",
    methods=["POST"]
)
def save_job():

    description = request.form[
        "description"
    ]

    jd_file = request.files.get(
        "jd_file"
    )

    if jd_file and jd_file.filename:

        filename = secure_filename(
            jd_file.filename
        )

        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        jd_file.save(path)

        description = extract_jd_text(
            path
        )

    create_job(

        request.form["job_title"],

        request.form["company_name"],

        request.form["required_skills"],

        request.form[
            "required_experience"
        ],

        description
    )

    flash(
    "Job Created Successfully",
    "success"
)

    return redirect("/upload")
@app.route(
    "/upload-resume",
    methods=["POST"]
)
def upload_resume():

    job = get_latest_job()

    clear_candidates()

    if not job:

        flash(
            "Create a job first",
            "danger"
        )

        return redirect("/create-job")

    job_text = (
        job["job_title"] + " " +
        job["job_description"] + " " +
        job["required_skills"]
    )

    jd_skills = extract_skills(
        job_text
    )

    print("JD Skills:", jd_skills)

    files = request.files.getlist(
        "resumes"
    )

    for file in files:

        if file and allowed_file(
            file.filename
        ):

            filename = secure_filename(
                file.filename
            )

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(path)

            parsed = parse_resume(path)
            print("\nFIRST 20 LINES")

            for i, line in enumerate(
                parsed["text"].split("\n")[:20]
            ):
                print(i, repr(line))
            print("FILENAME:", filename)
            print("PARSED NAME:", parsed["name"])

            print("\n====================")
            print("FILE:", filename)
            print("NAME:", parsed["name"])
            print("EMAIL:", parsed["email"])
            print("PHONE:", parsed["phone"])
            print("====================\n")

            candidate_skills = extract_skills(
                parsed["text"]
            )

            analysis = analyze_skills(
                jd_skills,
                candidate_skills
            )

            matched_count = len(
                analysis["matched"]
            )

            total_required = len(
                jd_skills
            )

            if total_required > 0:

                skill_score = (
                    matched_count /
                    total_required
                    ) * 100

                semantic_score = calculate_match_score(
                    job_text,
                    parsed["text"]
                )

                score = round(
                    (skill_score * 0.7) +
                    (semantic_score * 0.3),
                    2
                )

            else:

                score = 0

            classification = classify_candidate(
                score
            )

            candidate = {

                "name":
                parsed["name"],

                "email":
                parsed["email"],

                "phone":
                parsed["phone"],

                "skills":
                candidate_skills,

                "score":
                score,

                "classification":
                classification,

                "matched":
                analysis["matched"],

                "missing":
                analysis["missing"],

                "additional":
                analysis["additional"],

                "resume_file":
                filename
            }

            save_candidate(
                job["id"],
                candidate
            )

    return redirect(
        "/results"
    )
clear_candidates()
@app.route("/results")
def results():

    candidates = get_candidates()

    return render_template(
        "results.html",
        candidates=candidates
    )
@app.route("/test-jobs")
def test_jobs():

    import sqlite3

    conn = sqlite3.connect("database.db")

    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM jobs"
    ).fetchall()

    conn.close()

    return "<br>".join(
        [str(dict(row)) for row in rows]
    )
@app.route("/count")
def count():

    import sqlite3

    conn = sqlite3.connect("database.db")

    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM candidates"
    )

    total = cur.fetchone()[0]

    conn.close()

    return f"Candidates: {total}"

@app.route("/candidate/<int:candidate_id>")
def candidate_details(candidate_id):

    candidate = get_candidate_by_id(candidate_id)

    return render_template(
        "candidate_details.html",
        candidate=candidate
    )
@app.route("/download-report/<int:id>")
def download_report(id):

    candidate = get_candidate_by_id(id)

    if not candidate:
        return "Candidate not found"

    pdf_path = os.path.join(
        app.config["REPORT_FOLDER"],
        f"candidate_{id}.pdf"
    )

    c = canvas.Canvas(pdf_path)

    y = 800

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Candidate Report")

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Name: {candidate['name']}")
    y -= 20

    c.drawString(50, y, f"Email: {candidate['email']}")
    y -= 20

    c.drawString(50, y, f"Phone: {candidate['phone']}")
    y -= 20

    c.drawString(
        50,
        y,
        f"Score: {candidate['match_score']}%"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Classification: {candidate['classification']}"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Skills: {candidate['skills']}"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Matched Skills: {candidate['matched_skills']}"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Missing Skills: {candidate['missing_skills']}"
    )
    y -= 20

    c.drawString(
        50,
        y,
        f"Additional Skills: {candidate['additional_skills']}"
    )

    c.save()

    return send_file(
        pdf_path,
        as_attachment=True
    )
@app.route("/resume/<int:id>")
def view_resume(id):

    row = get_resume_file(id)

    if not row:
        return "Resume not found"

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        row["resume_file"]
    )

if __name__ == "__main__":
    clear_candidates()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )


