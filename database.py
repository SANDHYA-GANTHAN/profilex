import sqlite3

DB_NAME = "database.db"

def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn
def get_candidates():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM candidates
        ORDER BY match_score DESC
        """
    ).fetchall()

    conn.close()

    return rows

def init_db():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_title TEXT,

            company_name TEXT,

            required_skills TEXT,

            required_experience TEXT,

            job_description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_id INTEGER,

            name TEXT,

            email TEXT,

            phone TEXT,

            education TEXT,

            experience TEXT,

            skills TEXT,

            match_score REAL,

            classification TEXT,

            recommended_role TEXT,

            matched_skills TEXT,

            missing_skills TEXT,

            additional_skills TEXT,

recruiter_decision TEXT DEFAULT 'Pending',

resume_file TEXT,

report_file TEXT
        )
        """
    )

    conn.commit()

    conn.close()
def create_job(
        job_title,
        company_name,
        required_skills,
        required_experience,
        description
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO jobs(
        job_title,
        company_name,
        required_skills,
        required_experience,
        job_description
        )
        VALUES(?,?,?,?,?)
        """,
        (
            job_title,
            company_name,
            required_skills,
            required_experience,
            description
        )
    )

    conn.commit()

    conn.close()


def get_latest_job():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM jobs
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cur.fetchone()

    conn.close()

    return row


def save_candidate(job_id, candidate):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO candidates(
            job_id,
            name,
            email,
            phone,
            education,
            experience,
            skills,
            match_score,
            classification,
            matched_skills,
            missing_skills,
            additional_skills,
            recruiter_decision,
            resume_file,
            report_file
        )
        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
    job_id,
    candidate["name"],
    candidate["email"],
    candidate["phone"],
    "",
    "",
    ",".join(candidate["skills"]),
    candidate["score"],
    candidate["classification"],

    ",".join(candidate["matched"]),
    ",".join(candidate["missing"]),
    ",".join(candidate["additional"]),

    "Pending",

    candidate["resume_file"],

    ""
)
    )

    conn.commit()

    conn.close()

def clear_candidates():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM candidates"
    )

    conn.commit()

    conn.close()
def get_all_candidates():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM candidates
        ORDER BY match_score DESC
        """
    ).fetchall()

    conn.close()

    return rows
def get_dashboard_stats():

    conn = get_connection()

    cur = conn.cursor()

    total_candidates = cur.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        """
    ).fetchone()[0]

    excellent = cur.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        WHERE classification='Excellent Fit'
        """
    ).fetchone()[0]

    good = cur.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        WHERE classification='Good Fit'
        """
    ).fetchone()[0]

    average = cur.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        WHERE classification='Average Fit'
        """
    ).fetchone()[0]

    poor = cur.execute(
        """
        SELECT COUNT(*)
        FROM candidates
        WHERE classification='Poor Fit'
        """
    ).fetchone()[0]

    top_score = cur.execute(
        """
        SELECT MAX(match_score)
        FROM candidates
        """
    ).fetchone()[0]

    conn.close()

    return {
        "total": total_candidates,
        "excellent": excellent,
        "good": good,
        "average": average,
        "poor": poor,
        "top_score": top_score
    }
def get_candidate(candidate_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    row = cur.fetchone()

    conn.close()

    return row
def get_candidate_by_id(candidate_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    ).fetchone()

    conn.close()

    return row
def get_resume_file(candidate_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT resume_file
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    ).fetchone()

    conn.close()

    return row