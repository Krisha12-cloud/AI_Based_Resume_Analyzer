"""
Resume Parser - Extracts information from PDF resumes
FIXED VERSION - No duplicate functions!
"""
import re
import spacy
from spacy.matcher import Matcher
from pdfminer.high_level import extract_text

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        return extract_text(pdf_path)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_contact_number(text):
    """Extract contact number using regex"""
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_email(text):
    """Extract email using regex"""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_name(resume_text):
    """Extract name using spaCy"""
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    ]
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        if span.start_char < 2000:
            return span.text
    return None


def extract_education(text):
    """Extract education information"""
    education = []
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.?\w*|\bBachelor(?:'s)?(?:\s+of)?|\bMaster(?:'s)?(?:\s+of)?|\bPh\.?D\.?)\s(?:\w+\s){0,5}?\w+"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())
    return education


def _is_valid_skill(skill_text: str) -> bool:
    """
    Validate if extracted text is actually a skill
    ONLY ONE DEFINITION - NO DUPLICATES!
    """
    # Convert to lowercase for comparison
    skill_lower = skill_text.lower().strip()

    # Remove any leading/trailing whitespace and punctuation
    skill_lower = skill_lower.strip(" .,-;:/|()[]")

    # Too short or too long
    if len(skill_lower) < 2 or len(skill_lower) > 30:
        return False

    # Contains numbers (likely dates or addresses)
    if any(char.isdigit() for char in skill_lower):
        return False

    # Comprehensive exclusion list (ALL LOWERCASE)
    exclude_phrases = {
        # Locations
        'ahmedabad', 'gujarat', 'india', 'mumbai', 'delhi', 'bangalore',
        # Time/Date
        'present', 'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december',
        'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
        # Job titles/roles
        'intern', 'interns', 'internship', 'developer', 'engineer', 'analyst',
        'scientist', 'manager', 'specialist', 'consultant', 'architect',
        # Actions/Verbs
        'work', 'working', 'employed', 'focusing', 'aligning', 'construct',
        'effectively', 'rigorous', 'using', 'with', 'for',
        'processing', 'testing', 'validation', 'development', 'forecasting',
        # Generic terms - EXPANDED
        'insights', 'objectives', 'individuals', 'services', 'business',
        'accurate', 'backend', 'frameworks', 'the', 'and', 'to', 'on',
        'pvt', 'ltd', 'company', 'technologies', 'experience', 'tool', 'studio',
        # Company names
        'infolabz', 'technishal', 'pvt ltd', 'services',
        # Too generic tech terms
        'weather app', 'app using', 'projects', 'project', 'application',
        'data engineering', 'model development', 'data scientist',
        # Educational/Personal - KEY ADDITIONS
        'hindi', 'gujarati', 'english', 'hobbies', 'hobby', 'cooking',
        'school', 'college', 'university', 'indus university',
        'travelling', 'listening music', 'memorabilia', 'collecting memorabilia',
        'collecting', 'languages', 'language',
        # Generic CS terms that are too broad
        'management', 'internships', 'progress', 'understanding',
        'knowledge', 'familiarity', 'current', 'basic',
        'computer', 'programming', 'web', 'database', 'networks',
        'operating system', 'operating', 'system', 'structures',
        'algorithms', 'cyber', 'security', 'cyber security',
        'data structures', 'data', 'android', 'canva',
        # Single letters or very generic
        'of', 'c++', 'c', 'in', 'at', 'a', 'an', 'is', 'are', 'be',
    }

    # EXACT MATCH CHECK FIRST
    if skill_lower in exclude_phrases:
        return False

    # Split into words
    words = skill_lower.split()

    # Reject if ANY word in the phrase is in exclude list
    for word in words:
        if word in exclude_phrases:
            return False

    # Must contain at least one letter
    if not any(c.isalpha() for c in skill_lower):
        return False

    # Reject sentences (too many words)
    if len(words) > 4:
        return False

    # Reject common stop words
    stop_words = {'the', 'and', 'for', 'with', 'using', 'to', 'on', 'in', 'at', 'of', 'a', 'an'}
    if skill_lower in stop_words:
        return False

    return True


def _clean_skill_token(tok: str) -> str:
    """Clean individual skill tokens"""
    tok = tok.strip()
    # Remove bullets, numbers, brackets from start
    tok = re.sub(r"^[\-\u2022\•\*\)\(\[\]\d\.]+\s*", "", tok)
    # Remove brackets from end
    tok = re.sub(r"[\(\)\[\]\.]+$", "", tok)
    # Strip punctuation
    tok = tok.strip(" .,-;:/|")
    return tok


def extract_skills(text: str, debug=False) -> list:
    """
    Extract skills from resume text - FIXED VERSION
    Only extracts from Skills section
    """
    if debug:
        print("\n" + "="*70)
        print("DEBUG: Starting skill extraction")
        print("="*70)

    lines = text.split('\n')
    skills_content = []
    in_skills_section = False

    # Skills section headers
    skill_headers = [
        'technical skills', 'core skills', 'key skills', 'skills',
        'technical competencies', 'technologies', 'programming languages',
        'tech stack', 'technical stack', 'it skills', 'professional skills',
        'skill', 'competencies', 'technology'
    ]

    # Section headers that END the skills section
    other_headers = [
        'experience', 'work experience', 'professional experience',
        'education', 'projects', 'project', 'certifications', 'summary',
        'objective', 'internship', 'employment', 'achievements',
        'work history', 'employment history', 'career history',
        'academic', 'qualification', 'training', 'courses',
        'hobbies', 'interests', 'languages', 'language', 'personal'
    ]

    for i, line in enumerate(lines):
        line_clean = line.strip().lower()

        if not line_clean:
            continue

        # Check for skills header
        is_skill_header = False
        for header in skill_headers:
            if line_clean == header or line_clean.startswith(header + ':') or line_clean.startswith(header + ' '):
                is_skill_header = True
                break

        # Check for section end
        is_other_header = False
        if in_skills_section:
            for header in other_headers:
                if (line_clean == header or
                    line_clean.startswith(header + ':') or
                    (line_clean.startswith(header + ' ') and len(line_clean.split()) <= 3)):
                    if len(line_clean) <= 50:
                        is_other_header = True
                        break

        if is_skill_header:
            in_skills_section = True
            if debug:
                print(f"\n✓ SKILLS SECTION FOUND at line {i}: '{line.strip()}'")

            # Extract skills from header line itself
            for header in skill_headers:
                if line_clean.startswith(header):
                    remaining = line[len(header):].strip()
                    remaining = re.sub(r'^[::\-\•]+\s*', '', remaining)
                    if remaining and len(remaining) > 2:
                        skills_content.append(remaining)
            continue

        if is_other_header:
            if debug:
                print(f"\n✗ SKILLS SECTION ENDED at line {i}: '{line.strip()}'")
            in_skills_section = False
            break

        if in_skills_section:
            skills_content.append(line.strip())

    if not skills_content:
        if debug:
            print("\n❌ No skills section found!")
        return []

    if debug:
        print(f"\n📝 Raw skills content ({len(skills_content)} lines):")
        for idx, content in enumerate(skills_content):
            print(f"  {idx+1}. {content[:100]}")

    # Parse skills from content
    all_skills = []

    for content in skills_content:
        if len(content.strip()) < 2:
            continue

        # Split by various delimiters
        parts = []
        if ',' in content:
            parts = content.split(',')
        elif '|' in content:
            parts = content.split('|')
        elif ';' in content:
            parts = content.split(';')
        elif '•' in content or '●' in content or '○' in content:
            parts = re.split(r'[•●○]', content)
        elif '\t' in content:
            parts = content.split('\t')
        else:
            # Split by 2+ spaces
            parts = re.split(r'\s{2,}', content)
            if len(parts) == 1:
                parts = [content]

        for part in parts:
            cleaned = _clean_skill_token(part)
            if cleaned and len(cleaned) > 1:
                all_skills.append(cleaned)

    if debug:
        print(f"\n🔍 Extracted {len(all_skills)} items before validation")
        print(f"Items: {all_skills}")

    # VALIDATE and filter
    final_skills = []
    seen = set()
    excluded_items = []

    for skill in all_skills:
        skill_normalized = skill.lower().strip()

        # Skip duplicates
        if skill_normalized in seen:
            continue

        # VALIDATE - this is where filtering happens
        if _is_valid_skill(skill):
            seen.add(skill_normalized)
            final_skills.append(skill.title())
        else:
            excluded_items.append(skill)

    if debug:
        print(f"\n✅ VALID SKILLS ({len(final_skills)}):")
        for s in final_skills:
            print(f"  ✓ {s}")

        print(f"\n❌ EXCLUDED ({len(excluded_items)}):")
        for s in excluded_items:
            print(f"  ✗ {s}")

    print(f"\n✓ Final count: {len(final_skills)} valid skills")
    return final_skills


def parse_resume(pdf_path, debug=False):
    """
    Complete resume parsing
    Returns dict with all extracted information
    """
    text = extract_text_from_pdf(pdf_path)

    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'contact': extract_contact_number(text),
        'education': extract_education(text),
        'skills': extract_skills(text, debug=debug),
        'raw_text': text
    }