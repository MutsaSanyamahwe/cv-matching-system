from .utils.pdf_reader import extract_text_from_pdf
from .utils.text_cleaner import clean_text
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, File, UploadFile, Form
from sentence_transformers import SentenceTransformer
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


def get_spacy():
    global nlp
    if nlp is None:
        nlp=spacy.load("en_core_web_sm")

    return nlp

def get_embed_model():
    global embed_model
    if embed_model is None:
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embed_model


# Domain-specific skills dictionary
DOMAIN_SKILLS = {
    "Accountant": ["excel", "quickbooks", "sap", "tax compliance", "financial analysis", "audit", "budgeting", "accounts payable", "accounts receivable"],
    "Advocate": ["legal research", "case management", "drafting", "litigation", "contracts", "compliance", "arbitration"],
    "Agriculture": ["irrigation", "crop management", "soil analysis", "farm machinery", "harvesting", "fertilization"],
    "Apparel": ["pattern making", "sewing", "garment production", "textile design", "quality control"],
    "Arts": ["drawing", "painting", "illustration", "graphic design", "sculpture", "creative writing"],
    "Automobile": ["engine repair", "vehicle diagnostics", "autoCAD", "mechanical systems", "safety inspection"],
    "Aviation": ["flight operations", "air traffic control", "maintenance", "aviation safety", "piloting"],
    "Banking": ["risk management", "financial reporting", "loans", "investment analysis", "compliance"],
    "BPO": ["customer service", "call handling", "crm", "process improvement", "ticketing systems"],
    "Business-development": ["sales strategy", "client acquisition", "market research", "negotiation"],
    "Chef": ["recipe development", "menu planning", "food safety", "culinary techniques", "kitchen management"],
    "Construction": ["project management", "safety standards", "blueprint reading", "contract management"],
    "Consultant": ["business analysis", "process improvement", "strategic planning", "stakeholder engagement"],
    "Designer": ["ui design", "ux design", "adobe suite", "prototyping", "branding"],
    "Digital-media": ["social media", "content creation", "seo", "analytics", "digital campaigns"],
    "Engineering": ["c++", "python", "matlab", "circuit design", "rf systems", "mechanical design", "project design","full-stack development", "front-end", "back-end", "api integration"],
    "Finance": ["budgeting", "financial analysis", "investment", "accounting", "forecasting"],
    "Fitness": ["personal training", "exercise programming", "nutrition", "wellness coaching"],
    "Healthcare": ["patient care", "diagnosis", "medical terminology", "hipaa", "clinical trials"],
    "HR": ["recruitment", "employee relations", "talent management", "performance reviews"],
    "Information technology": ["python","Docker", "java", "sql", "cloud", "networking", "security", "devops", "aws", "azure","node.js", "express", "full-stack", "end-to-end", 
                               "integration", "mobile deployment", "expo build services", "real-world data","end-to-end-solutions","expo build services","feature engineering",
                               "structured data extraction","data analysis", "predictive modelling","real-time-systems", "C#", "javascript","java","php", "R", "Machine Learning","ML", "ml", "deployment", "relational databases"],
    "Public relations": ["media relations", "press releases", "branding", "events management"],
    "Sales": ["lead generation", "crm", "negotiation", "account management"],
    "Teacher": ["lesson planning", "curriculum design", "classroom management", "student assessment"],
}

# Soft skills applicable across all domains
SOFT_SKILLS = ["communication","analytical thinking", "teamwork", "leadership", "problem solving", "organization",
               "time management", "adaptability", "creativity", "critical thinking", "attention to detail",
               "end-to-end system design", "real-world data analysis", "api integration", "mobile deployment", "hands-on", "impact"]

# Words to ignore 
NOISE_WORDS = {
    "job", "experience", "work", "role", "team", "company", "field", "project", "task", "ability", 
    "education", "graduate", "position", "requirement", "responsibility", "skills", "career", "check", 
    "technology", "enhance", "exposure", "sector", "numerical", "passion", "cuttingedge", "skill", "drive",
    "mindset", "performance", "practice", "understanding", "tool", "mentor", "knowledge", "contribute"
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

def compute_embedding_score(cv_text, jd_text):
    model = get_embed_model()
    cv_embed = model.encode(cv_text)
    jd_embed = model.encode(jd_text)

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
    embedding_score = compute_embedding_score(cv_text, jd_text)

    #final score
    final_score = 0.7*embedding_score + 0.3*skill_score

    return {
    "fit_score": round(float(final_score), 2),
    "matched_skills": matched_skills,
    "missing_skills": missing_skills
}





