import sqlite3

def init_database():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS companies")

    cursor.execute("""
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            location TEXT NOT NULL,
            apply_link TEXT NOT NULL
        )
    """)

    vacancies = [
        (
            "MTC Namibia", 
            "Junior Cloud & Infrastructure Administrator", 
            "Linux, Networking, Cybersecurity, Docker", 
            "Windhoek", 
            "https://www.mtc.com.na/careers"
        ),
        (
            "Green Enterprise Solutions", 
            "Junior Full-Stack Developer", 
            "Python, FastAPI, HTML, CSS, JavaScript", 
            "Windhoek", 
            "https://www.green.com.na"
        ),
        (
            "Telecom Namibia", 
            "Network Security Associate", 
            "Networking, Linux, Cybersecurity, Python", 
            "Windhoek", 
            "https://www.telecom.na"
        ),
        (
            "CyberConnect Solutions", 
            "Trainee DevOps Engineer", 
            "Python, Linux, Docker, AWS Cloud, CI/CD Pipelines", 
            "Remote / Windhoek", 
            "https://github.com/rubenmatias8222-hub"
        )
    ]

    cursor.executemany("""
        INSERT INTO companies (company_name, job_title, required_skills, location, apply_link)
        VALUES (?, ?, ?, ?, ?)
    """, vacancies)

    conn.commit()
    conn.close()
    print("Successfully created 'jobs.db' and populated it with local tech vacancies!")

if __name__ == "__main__":
    init_database()
