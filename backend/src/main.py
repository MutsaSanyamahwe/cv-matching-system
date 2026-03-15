from .utils.pdf_reader import extract_text_from_pdf
import pickle
from .utils.text_cleaner import clean_text
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, File, UploadFile, Form
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from fastapi.middleware.cors import CORSMiddleware

#Loading the models
nlp = None
embed_model = None



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("/app/tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)


def get_spacy():
    global nlp
    if nlp is None:
        nlp=spacy.load("en_core_web_sm")

    return nlp

def compute_similarity(cv_text, jd_text):
    #transforming
    cv_vectorizer = tfidf_vectorizer.transform([cv_text])
    jd_vectorizer = tfidf_vectorizer.transform([jd_text])


    similarity = cosine_similarity(cv_vectorizer,jd_vectorizer)[0][0]

    return similarity * 100


# Domain-specific skills dictionary
DOMAIN_SKILLS = {
    "Accountant": ["excel", "quickbooks", "sap", "tax compliance", "financial analysis", "audit", "budgeting", "accounts payable", "accounts receivable", "ledger management", "financial reporting", "reconciliation", "payroll", "tax filing", "variance analysis"],
    "Advocate": ["legal research", "case management", "drafting", "litigation", "contracts", "compliance", "arbitration", "client counseling", "court filings", "negotiation", "legal writing", "policy interpretation"],
    "Agriculture": ["irrigation", "crop management", "soil analysis", "farm machinery", "harvesting", "fertilization", "pest management", "greenhouse management", "plant breeding", "livestock care", "agronomy"],
    "Apparel": ["pattern making", "sewing", "garment production", "textile design", "quality control", "fabric sourcing", "fashion illustration", "tailoring", "fitting", "production planning"],
    "Arts": ["drawing", "painting", "illustration", "graphic design", "sculpture", "creative writing", "animation", "photography", "video editing", "art curation", "typography"],
    "Automobile": ["engine repair", "vehicle diagnostics", "autoCAD", "mechanical systems", "safety inspection", "automotive electronics", "chassis repair", "brake systems", "vehicle maintenance", "fuel systems"],
    "Aviation": ["flight operations", "air traffic control", "maintenance", "aviation safety", "piloting", "navigation systems", "flight planning", "crew management", "aviation regulations", "aircraft inspection"],
    "Banking": ["risk management", "financial reporting", "loans", "investment analysis", "compliance", "portfolio management", "customer accounts", "credit assessment", "bank reconciliation", "treasury management"],
    "BPO": ["customer service", "call handling", "crm", "process improvement", "ticketing systems", "inbound calls", "outbound calls", "quality monitoring", "data entry", "client escalation handling"],
    "Business-development": ["sales strategy", "client acquisition", "market research", "negotiation", "lead generation", "pitching", "proposal writing", "networking", "business analysis", "strategic partnerships"],
    "Chef": ["recipe development", "menu planning", "food safety", "culinary techniques", "kitchen management", "inventory management", "baking", "catering", "nutrition planning", "presentation skills"],
    "Construction": ["project management", "safety standards", "blueprint reading", "contract management", "cost estimation", "site supervision", "material procurement", "quality assurance", "risk assessment", "civil engineering"],
    "Consultant": ["business analysis", "process improvement", "strategic planning", "stakeholder engagement", "change management", "gap analysis", "presentation skills", "report writing", "workflow optimization", "project consulting"],
    "Designer": ["ui design", "ux design", "adobe suite", "prototyping", "branding", "wireframing", "design thinking", "illustration", "typography", "color theory", "motion graphics"],
    "Digital-media": ["social media", "content creation", "seo", "analytics", "digital campaigns", "email marketing", "content strategy", "paid media", "community management", "digital advertising"],
    "Engineering": ["c++", "python", "matlab", "circuit design", "rf systems", "mechanical design", "project design", "full-stack development", "front-end", "back-end", "api integration", "embedded systems", "control systems", "software architecture", "testing and debugging", "CAD modeling", "simulation", "data analysis"],
    "Finance": ["budgeting", "financial analysis", "investment", "accounting", "forecasting", "financial modeling", "capital budgeting", "cost analysis", "variance reporting", "portfolio management"],
    "Fitness": ["personal training", "exercise programming", "nutrition", "wellness coaching", "strength training", "cardio planning", "group fitness instruction", "rehabilitation exercises", "yoga", "pilates"],
    "Healthcare": ["patient care", "diagnosis", "medical terminology", "hipaa", "clinical trials", "medication administration", "vital signs monitoring", "treatment planning", "wound care", "telemedicine", "patient education"],
    "HR": ["recruitment", "employee relations", "talent management", "performance reviews", "onboarding", "policy development", "training and development", "compliance", "conflict resolution", "HRIS"],
    "Information technology": ["python","Docker", "java", "sql", "cloud", "networking", "security", "devops", "aws", "azure", "node.js", "express", "full-stack", "end-to-end", 
                               "integration", "mobile deployment", "expo build services", "real-world data","end-to-end-solutions","feature engineering",
                               "structured data extraction","data analysis", "predictive modelling","real-time-systems", "C#", "javascript","php", "R", "Machine Learning","ML", "deployment", "relational databases", 
                               "kubernetes","ci/cd pipelines","microservices","api development","serverless","react","angular","vue","tensorflow","pytorch","nlp","data visualization","sql optimization","database design"],
    "Public relations": ["media relations", "press releases", "branding", "events management", "crisis communication", "stakeholder engagement", "speech writing", "public speaking", "campaign planning"],
    "Sales": ["lead generation", "crm", "negotiation", "account management", "cold calling", "pipeline management", "customer retention", "upselling", "sales strategy", "proposal development"],
    "Teacher": ["lesson planning", "curriculum design", "classroom management", "student assessment", "grading", "educational technology", "learning objectives", "lesson delivery", "differentiated instruction", "parent communication"],
}

# Soft skills applicable across all domains
SOFT_SKILLS = [
    "communication", "verbal communication", "written communication", "presentation skills",
    "analytical thinking", "critical thinking", "problem solving", "decision making", "research",
    "teamwork", "collaboration", "interpersonal skills", "relationship building", "conflict resolution",
    "leadership", "mentoring", "coaching", "delegation", "supervision", "strategic thinking", "vision",
    "organization", "time management", "prioritization", "planning", "attention to detail", "multitasking",
    "adaptability", "flexibility", "resilience", "creativity", "innovation", "curiosity", "initiative",
    "emotional intelligence", "empathy", "active listening", "patience", "negotiation", "persuasion",
    "critical observation", "project management", "stakeholder management", "decision making",
    "end-to-end system design", "real-world data analysis", "api integration", "mobile deployment",
    "hands-on", "impact", "continuous learning", "self-motivation", "problem identification", "process improvement",
    "collaborative problem solving", "analytical reporting", "adaptable communication", "conflict management",
    "team leadership", "cross-functional collaboration", "creative problem solving"
]

NOISE_WORDS = {
    # Existing words
    "job", "experience", "work", "role", "team", "company", "field", "project", "task", "ability", 
    "education", "graduate", "position", "requirement", "responsibility", "skills", "career", "check", 
    "technology", "enhance", "exposure", "sector", "numerical", "passion", "cuttingedge", "skill", "drive",
    "mindset", "performance", "practice", "understanding", "tool", "mentor", "knowledge", "contribute",

    # Dates / numbers / time
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
    "november", "december", "year", "years", "month", "months", "week", "weeks", "day", "days",
    "00", "01", "02","03","04","05","06","07","08","09","10","11","12","2000","2001","2002","2003","2004",
    "2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018",
    "2019","2020","2021","2022","2023","2024","2025","1990","1980","1970",

    # Generic verbs / adjectives
    "responsible", "managed", "managed", "assisted", "performed", "conducted", "led", "coordinated",
    "organized", "implemented", "maintained", "monitored", "attended", "participated", "provided",
    "support", "effective", "efficient", "excellent", "strong", "good", "basic", "proficient", "advanced",
    "experienced", "familiar", "knowledgeable", "skilled", "capable", "able", "dedicated", "teamwork",
    "leadership", "communication", "collaborative", "adaptable", "reliable",

    # Miscellaneous CV clutter
    "city", "state", "companyname", "department", "hospital", "center", "unit", "school", "college", "university",
    "admin", "assistant", "office", "medical", "resident", "patient", "nursing", "care", "manager",
    "mr", "ms", "mrs", "dr", "rn", "aa", "adn", "bsn"
}



def extract_skills(text: str) -> list[str]:
    cleaned_text = clean_text(text.lower())
    skills_set: set[str] = set()
    
    doc = get_spacy()(cleaned_text)
    
    # Add nouns/proper nouns, but skip noise words
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"]:
            token_text = token.text.strip()
            if token_text not in NOISE_WORDS:
                skills_set.add(token_text)
    
    # Add named entities
    for ent in doc.ents:
        skills_set.add(ent.text.strip().lower())
    
    # Match domain-specific skills
    cleaned_text_words = set(cleaned_text.split())
    for domain, skills in DOMAIN_SKILLS.items():
        for skill in skills:
            skill_clean = clean_text(skill)
            skill_words = skill_clean.split()
            if all(word in cleaned_text_words for word in skill_words):
                skills_set.add(skill.lower())
    
    # Match soft skills
    for skill in SOFT_SKILLS:
        skill_clean = clean_text(skill)
        if all(word in cleaned_text_words for word in skill_clean.split()):
            skills_set.add(skill.lower())
    
    # Final cleanup
    skills_set = {s.replace("\n", "").strip() for s in skills_set if len(s) > 1}
    
    return sorted(list(skills_set))



    return cosine_similarity([cv_embed],[jd_embed])[0][0] * 100

@app.post("/match")
async def match(
    cv_file:UploadFile = File(...),
      job_description:str = Form(...)
    ):

    #Extract text from PDF
    cv_text = extract_text_from_pdf(cv_file.file)

    #Extract job description pasted
    jd_text = job_description

    cv_text_cleaned = clean_text(cv_text)
    jd_text_cleaned = clean_text(jd_text)

    cv_skills = extract_skills(cv_text_cleaned)
    jd_skills = extract_skills(jd_text_cleaned)

    #skill comparison
    matched_skills = [s for s in cv_skills if s in jd_skills]
    missing_skills = [s for s in jd_skills if s not in cv_skills]
    skill_score = len(matched_skills)/max(len(jd_skills),1)*100

     #semantic embedding score
    similarity_score = compute_similarity(cv_text, jd_text)

    #final score
    final_score = 0.7*similarity_score + 0.3*skill_score

    return {
    "fit_score": round(float(final_score), 2),
    "matched_skills": matched_skills,
    "missing_skills": missing_skills
}





