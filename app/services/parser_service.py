import re

class ParserService:

    SECTION_HEADERS = {
        "skills": [
            "skills",
            "technical skills",
            "key skills"
        ],
        "education": [
            "education",
            "academic background",
            "academic qualifications"
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment"
        ],
        "projects": [
            "projects",
            "academic projects"
        ],
        "certifications": [
            "certifications",
            "certificates"
        ]
    }
    def __init__(self, text):

        self.text = text

        self.sections = {}

    def parse_resume(self):
        info = self.extract_personal_info()
        sections = self.split_sections()

        return {
            "name": info["name"],
            "email": info["email"],
            "phone": info["phone"],
            "links": info["links"],
            "skills": self.parse_skills(sections.get("skills", [])),
            "education": self.parse_education(sections.get("education", [])),
            "experience": self.parse_experience(sections.get("experience", [])),
            "projects": self.parse_projects(sections.get("projects", [])),
            "certifications": self.parse_certifications(
                sections.get("certifications", [])
            )
        }

    def extract_personal_info(self):

        lines = [line.strip() for line in self.text.split("\n") if line.strip()]

        name = lines[0] if lines else ""

        email = ""

        phone = ""

        github = ""

        linkedin = ""

        portfolio = ""

        email_match = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            self.text
        )

        if email_match:
            email = email_match.group()

        phone_match = re.search(
            r'(\+91[\s-]?)?[6-9]\d{9}',
            self.text
        )

        if phone_match:
            phone = phone_match.group()

        github_match = re.search(
            r'https?://github\.com/\S+',
            self.text,
            re.I
        )

        if github_match:
            github = github_match.group()

        linkedin_match = re.search(
            r'https?://(www\.)?linkedin\.com/\S+',
            self.text,
            re.I
        )

        if linkedin_match:
            linkedin = linkedin_match.group()

        urls = re.findall(r'https?://\S+', self.text)

        for url in urls:
            if "github" not in url.lower() and \
            "linkedin" not in url.lower():
                portfolio = url
                break

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "links": {
                "github": github,
                "linkedin": linkedin,
                "portfolio": portfolio
            }
        }

    def split_sections(self, headers=SECTION_HEADERS):

        sections = {}

        current = None

        for line in self.text.split("\n"):

            line = line.strip()

            if not line:
                continue

            lower = line.lower()

            found = False

            for key, headers in headers.items():

                if lower in headers:
                    current = key
                    sections[current] = []
                    found = True
                    break

            if found:
                continue

            if current:
                sections[current].append(line)

        return sections


    def parse_skills(self, lines):

        skills = []

        for line in lines:

            line = line.strip("-• ")

            if "," in line:
                skills.extend(
                    [s.strip() for s in line.split(",") if s.strip()]
                )
            else:
                skills.append(line)

        return skills


    def parse_education(self, lines):

        text = "\n".join(lines)

        degree = ""

        institution = ""

        cgpa = ""

        year = ""

        degree_keywords = [
            "b.tech",
            "b.e",
            "m.tech",
            "bachelor",
            "master",
            "mba",
            "bca",
            "mca",
            "phd"
        ]

        for line in lines:

            if any(keyword in line.lower()
                for keyword in degree_keywords):

                degree = line
                break

        for line in lines:

            if "college" in line.lower() or \
            "university" in line.lower() or \
            "institute" in line.lower():

                institution = line
                break

        cgpa_match = re.search(
            r'CGPA[: ]*([\d.]+)',
            text,
            re.I
        )

        if cgpa_match:
            cgpa = cgpa_match.group(1)

        years = re.findall(r'\b(19|20)\d{2}\b', text)

        if years:
            year = years[-1]

        return [{
            "degree": degree,
            "institution": institution,
            "cgpa": cgpa,
            "year": year
        }] if degree else []


    def parse_experience(self, lines):

        if not lines:
            return []

        return [{
            "description": "\n".join(lines)
        }]


    def parse_projects(self, lines):

        if not lines:
            return []
        projects = []
        current = None
        for line in lines:
            if len(line.split()) <= 5:
                if current:
                    projects.append(current)
                current = {
                    "title": line,
                    "description": ""
                }
            else:
                if current:
                    current["description"] += line + " "
        if current:
            projects.append(current)
        return projects
    def parse_certifications(self, lines):

        certs = []

        for line in lines:

            line = line.strip("-• ")

            if line:
                certs.append(line)

        return certs