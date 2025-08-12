import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
import time
from datetime import datetime
from io import BytesIO
import os

# --- Safe Import of Supporting Libraries ---
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, BaseDocTemplate, PageTemplate, Frame, ListFlowable
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.graphics.shapes import Drawing, Rect
    from PIL import Image as PILImage
    import google.generativeai as genai
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError as e:
    st.error(f"A required library is missing. Please ensure your `requirements.txt` is correct. Missing library: {e.name}")
    st.stop()

# --- Safe Import of Questionnaire ---
try:
    from questionnaire import questions, career_clusters, aptitude_questions, career_cluster_weights, career_descriptions
except ImportError:
    st.error("FATAL ERROR: The 'questionnaire.py' file is missing. This file is required to run the application.")
    st.stop()


# --- Google Sheets Database Setup ---
def save_results_to_gsheet(profile, recommendations):
    try:
        creds_json_str = os.environ.get("gcp_service_account")
        if not creds_json_str:
            st.error("Database Error: GCP service account credentials not found in environment.")
            return False
        
        creds_dict = json.loads(creds_json_str)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Fixed: Using correct sheet name "Sheet 1" instead of "Career App Results"
        spreadsheet = client.open("Career App Results")
        sheet = spreadsheet.worksheet("Sheet 1")  # Specify Sheet 1 explicitly

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Fixed: Proper handling of profile dictionary
        name = profile.get('name', 'N/A') if isinstance(profile, dict) else str(profile)
        age = str(profile.get('age', 'N/A')) if isinstance(profile, dict) else 'N/A'
        email = profile.get('email', 'N/A') if isinstance(profile, dict) else 'N/A'
        
        # Handle recommendations safely
        top_3 = recommendations[:3] if recommendations else []
        career1, score1 = (top_3[0][0], f"{top_3[0][1]:.0f}") if len(top_3) > 0 else ('N/A', 'N/A')
        career2, score2 = (top_3[1][0], f"{top_3[1][1]:.0f}") if len(top_3) > 1 else ('N/A', 'N/A')
        career3, score3 = (top_3[2][0], f"{top_3[2][1]:.0f}") if len(top_3) > 2 else ('N/A', 'N/A')

        row = [timestamp, name, age, email, career1, score1, career2, score2, career3, score3]
        sheet.append_row(row)
        return True
        
    except Exception as e:
        st.error(f"Database Error: Could not save results to Google Sheets. Error: {str(e)}")
        return False

# --- Gemini API & Secrets Setup ---
def initialize_gemini():
    try:
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            st.warning("Gemini API Key not found. AI analysis will be disabled.")
            return None
        genai.configure(api_key=GEMINI_API_KEY)
        return 'gemini-1.5-flash'
    except Exception as e:
        st.warning(f"Could not configure Gemini API: {e}")
        return None

GEMINI_MODEL = initialize_gemini()

# --- Hardcoded Trait Definitions ---
trait_definitions = {
    'Aptitude': {
        'V': { 'meaning': "Verbal Aptitude (V) measures the ability to understand and reason with language, including reading comprehension and vocabulary.", 'analysis': { 'low': "A lower score suggests a preference for hands-on, numerical, or visual tasks over language-heavy ones.", 'medium': "A moderate score indicates a solid, functional grasp of language.", 'high': "A high score indicates a strong talent for language, suiting roles in writing, law, or education." }},
        'Nu': { 'meaning': "Numerical Aptitude (Nu) assesses the ability to work with numbers and solve mathematical problems quickly and accurately.", 'analysis': { 'low': "A lower score indicates a preference for qualitative, creative, or interpersonal work over tasks that are heavily reliant on numbers.", 'medium': "A moderate score shows you are competent with day-to-day numerical tasks like budgeting or metrics.", 'high': "A high score signals a strong ability in mathematics and data interpretation, ideal for finance, data science, or engineering." }},
        'Sp': { 'meaning': "Spatial Aptitude (Sp) evaluates the capacity to visualize and manipulate objects in two and three-dimensional space.", 'analysis': { 'low': "A lower score suggests a preference for abstract or verbal tasks rather than those requiring mental visualization of objects.", 'medium': "A moderate score indicates a functional ability to understand and work with diagrams, maps, and physical spaces.", 'high': "A high score is a key indicator for success in fields like engineering, architecture, design, and surgery." }},
        'LR': { 'meaning': "Logical Reasoning (LR) measures the ability to analyze information, identify patterns, and draw valid conclusions.", 'analysis': { 'low': "A lower score may indicate a more intuitive or creative approach to problem-solving, rather than a step-by-step, formal logic process.", 'medium': "A moderate score shows a solid ability to solve problems logically and make well-reasoned decisions.", 'high': "A high score demonstrates excellent problem-solving and critical thinking skills, perfect for strategy, law, and research roles." }},
        'Me': { 'meaning': "Mechanical Aptitude (Me) assesses understanding of basic mechanical principles and physical laws.", 'analysis': { 'low': "A lower score suggests strengths lie outside of hands-on mechanical fields, perhaps in work involving data, people, or ideas.", 'medium': "A moderate score indicates a good foundational understanding of how things work, suiting many technical roles.", 'high': "A high score indicates a natural talent for understanding machinery and physical systems, a strong asset for engineering or skilled trades." }},
        'Pe': { 'meaning': "Perceptual Aptitude (Pe) measures the ability to quickly and accurately identify visual patterns, details, and differences.", 'analysis': { 'low': "A lower score suggests your strengths are in areas other than rapid visual processing, preferring tasks that allow for deeper analysis.", 'medium': "A moderate score shows a good eye for detail, making you reliable in tasks that require quality control or data checking.", 'high': "A high score indicates a keen ability to spot errors and inconsistencies quickly, valuable in quality assurance, editing, and data verification." }},
        'Ab': { 'meaning': "Abstract Reasoning (Ab) evaluates the ability to identify patterns and relationships in non-verbal, abstract information.", 'analysis': { 'low': "A lower score may indicate a preference for concrete, practical problem solving over dealing with theoretical and abstract concepts.", 'medium': "A moderate score shows a good capacity for conceptual thinking and adapting to unfamiliar problems.", 'high': "A high score signals a strong ability to think conceptually and strategically, key for complex fields like IT, science, and strategy." }}
    },
    'OCEAN': {
        'Openness': { 'meaning': "Reflects willingness to embrace new ideas, art, and experiences.", 'analysis': { 'low': "You are practical, conventional, and prefer familiar routines and proven approaches.", 'medium': "You balance appreciating new ideas with valuing tradition and practical reality.", 'high': "You are imaginative, curious, and open-minded, thriving in creative and dynamic environments." } },
        'Conscientiousness': { 'meaning': "About being organized, responsible, and hardworking.", 'analysis': { 'low': "You are more spontaneous and flexible, preferring to go with the flow rather than stick to a rigid plan.", 'medium': "You are generally reliable and organized, but can also be flexible when needed.", 'high': "You show exceptional discipline, organization, and a strong sense of duty. You are highly reliable and driven." } },
        'Extraversion': { 'meaning': "The tendency to seek stimulation from social interactions.", 'analysis': { 'low': "You are more reserved and thoughtful (introverted), energized by spending time alone.", 'medium': "You enjoy a mix of social time and solitude (ambiverted), adapting to the situation.", 'high': "You are outgoing and sociable, energized by being around others and thriving in team environments." } },
        'Agreeableness': { 'meaning': "The tendency to be compassionate and cooperative.", 'analysis': { 'low': "You are more competitive and analytical, prioritizing logic over emotion in decisions.", 'medium': "You are cooperative but can also assert your own interests when necessary.", 'high': "You are empathetic, cooperative, and a great team player, skilled at building harmony." } },
        'Neuroticism': { 'meaning': "The tendency to experience negative emotions like anxiety and stress.", 'analysis': { 'low': "You are calm, resilient, and secure (high emotional stability), handling stress well.", 'medium': "You experience a normal range of emotions, generally stable but can feel stress in difficult situations.", 'high': "You are sensitive to stress and prone to worry, experiencing emotions intensely." } }
    },
    'RIASEC': {
        'Realistic': { 'meaning': "Prefers working with objects, tools, and machines.", 'analysis': { 'low': "You prefer working with people, ideas, or data rather than hands-on, physical tasks.", 'medium': "You are comfortable in both practical, hands-on situations and more abstract or people-oriented work.", 'high': "You have a strong interest in physical, hands-on work. Careers in trades, engineering, and outdoors are a great fit." } },
        'Investigative': { 'meaning': "Enjoys analyzing, researching, and solving complex problems.", 'analysis': { 'low': "You prefer practical action or social interaction over deep analytical and research-oriented tasks.", 'medium': "You have a healthy curiosity and enjoy solving problems, but also value practical application.", 'high': "You have a deep curiosity and a passion for analysis. Careers in science, research, and data are a strong match." } },
        'Artistic': { 'meaning': "Creative, intuitive, and expressive, preferring unstructured situations.", 'analysis': { 'low': "You prefer structure, logic, and clear outcomes over ambiguity and self-expression.", 'medium': "You appreciate creativity and can bring an innovative spark to more structured roles.", 'high': "You have a strong need for self-expression and creativity, thriving in fields like design, writing, and arts." } },
        'Social': { 'meaning': "Enjoys working with people; helpful, friendly, and trustworthy.", 'analysis': { 'low': "You prefer working with data, things, or ideas rather than directly helping or instructing people.", 'medium': "You are a good team player but may not want a role that is exclusively focused on helping others.", 'high': "You have a strong desire to help, teach, and connect with others, suiting roles in counseling, healthcare, and education." } },
        'Enterprising': { 'meaning': "Energetic, ambitious, and sociable; enjoys leading and persuading.", 'analysis': { 'low': "You prefer supportive, analytical, or creative roles over those involving leadership or sales.", 'medium': "You are comfortable taking initiative but are not necessarily driven to be in charge at all times.", 'high': "You are a natural leader and persuader, making you a great fit for business, sales, and management." } },
        'Conventional': { 'meaning': "Prefers structured environments with clear rules; detail-oriented.", 'analysis': { 'low': "You have a strong dislike for routine and detailed procedural work, preferring creative or unstructured environments.", 'medium': "You are comfortable with detail-oriented work but also appreciate having some variety and flexibility.", 'high': "You are highly organized, efficient, and reliable, excelling in roles that require structure and data management." } }
    },
    'Hofstede': {
        'PDI': { 'meaning': "Power Distance Index: How a society handles inequalities.", 'analysis': { 'low': "You prefer a flat structure, open communication, and equal distribution of power.", 'medium': "You are adaptable to both hierarchical and egalitarian work environments.", 'high': "You are comfortable with clear hierarchies and respect for authority." } },
        'IDV': { 'meaning': "Individualism vs. Collectivism: Degree of interdependence.", 'analysis': { 'low': "You prioritize group harmony and team success over individual recognition (Collectivist).", 'medium': "You value both personal achievement and group collaboration.", 'high': "You are self-reliant and value personal achievement and autonomy (Individualist)." } },
        'MAS': { 'meaning': "Masculinity vs. Femininity: Assertiveness vs. cooperation.", 'analysis': { 'low': "You value work-life balance, cooperation, and a supportive environment (Feminine).", 'medium': "You are driven to succeed but also highly value a positive work environment.", 'high': "You are highly ambitious, competitive, and motivated by success (Masculine)." } },
        'UAI': { 'meaning': "Uncertainty Avoidance Index: Comfort with ambiguity.", 'analysis': { 'low': "You are comfortable with ambiguity, adaptable to change, and open to taking risks.", 'medium': "You can tolerate uncertainty but also appreciate having clear plans and guidelines.", 'high': "You prefer clear rules, structure, and predictable outcomes." } },
        'LTO': { 'meaning': "Long-Term Orientation: Focus on future vs. past/present.", 'analysis': { 'low': "You value tradition, quick results, and short-term goals.", 'medium': "You respect tradition while also planning pragmatically for the future.", 'high': "You are pragmatic and focused on long-term, sustainable success." } },
        'IVR': { 'meaning': "Indulgence vs. Restraint: Control of desires and impulses.", 'analysis': { 'low': "You are disciplined and prioritize social norms over personal gratification (Restraint).", 'medium': "You have a healthy balance between enjoying life and maintaining control.", 'high': "You value personal freedom, enjoying life, and expressing emotions freely (Indulgence)." } }
    }
}

fallback_content = {
    "development_plan": "- Seek a mentor in a field that interests you to gain practical insights.\n- Dedicate time to online courses or workshops to build specific technical skills.",
    "swot": {
        "S": "Your unique combination of personality and interests allows you to bring a fresh and valuable perspective to this field.", 
        "W": "To excel, you may need to focus on developing specific technical skills or gaining more hands-on experience relevant to this career.", 
        "O": "Emerging trends in this industry provide a great opportunity for new talent to innovate and make a significant impact.", 
        "T": "This is a competitive field, so continuous learning and networking will be crucial to stay ahead of industry changes."
    },
    "conclusion": "This report is a snapshot of your potential. Use these insights as a starting point to explore the recommended career paths and continue your journey of self-discovery."
}

# Color definitions
apple_blue = colors.Color(0, 113/255, 227/255)
apple_dark_gray = colors.Color(45/255, 45/255, 45/255)
apple_light_gray = colors.Color(245/255, 245/255, 247/255)
apple_green = colors.Color(52/255, 199/255, 89/255)
apple_red = colors.Color(255/255, 69/255, 58/255)
apple_orange = colors.Color(255/255, 159/255, 10/255)
apple_teal = colors.Color(90/255, 200/255, 250/255)

# Constants
RIASEC = ["Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional"]
OCEAN = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
HOFSTEDE = ["PDI", "IDV", "MAS", "UAI", "LTO", "IVR"]
APTITUDE = ['V', 'Nu', 'Sp', 'LR', 'Me', 'Pe', 'Ab']
APTITUDE_FULL_NAMES = {'V': 'Verbal', 'Nu': 'Numerical', 'Sp': 'Spatial', 'LR': 'Logical Reasoning', 'Me': 'Mechanical', 'Pe': 'Perceptual', 'Ab': 'Abstract'}
SECTION_TRAITS = {'Aptitude': APTITUDE, 'OCEAN': OCEAN, 'RIASEC': RIASEC, 'Hofstede': HOFSTEDE}
TRAIT_FULL_NAMES = {
    'R': 'Realistic', 'I': 'Investigative', 'A': 'Artistic', 'S': 'Social', 'E': 'Enterprising', 'C': 'Conventional',
    'O': 'Openness', 'C': 'Conscientiousness', 'E': 'Extraversion', 'A': 'Agreeableness', 'N': 'Neuroticism',
    'PDI': 'Power Distance Index', 'IDV': 'Individualism vs. Collectivism', 'MAS': 'Masculinity vs. Femininity',
    'UAI': 'Uncertainty Avoidance Index', 'LTO': 'Long-Term Orientation', 'IVR': 'Indulgence vs. Restraint',
    'V': 'Verbal', 'Nu': 'Numerical', 'Sp': 'Spatial', 'LR': 'Logical Reasoning', 'Me': 'Mechanical', 'Pe': 'Perceptual', 'Ab': 'Abstract'
}

# --- Utility Functions ---
def prepare_client_profile(user_data):
    profile = {
        'name': user_data.get('name', ''),
        'age': user_data.get('age', 0),
        'status': user_data.get('class_or_occupation', ''),
        'email': user_data.get('email', ''),
        'phone': user_data.get('phone', ''),
        'date': datetime.now().strftime("%Y-%m-%d")
    }
    
    text_keys = ['hobbies', 'interests', 'skills', 'competitive_subjects', 'easy_tasks', 'passion', 'big_problems', 'topics_of_interest', 'extra_benefit', 'future_opportunities']
    for key in text_keys:
        if key in user_data and isinstance(user_data[key], str):
            profile[key] = [item.strip() for item in user_data[key].split(',') if item.strip()]
        else:
            profile[key] = []
    
    for section in SECTION_TRAITS.keys():
        profile[section] = calculate_section_scores(section, user_data)
    
    return profile

def get_gemini_analysis(prompt, client_profile, max_retries=2):
    if not GEMINI_MODEL:
        return None
        
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(GEMINI_MODEL)
            full_prompt = f"{prompt}\n\nHere is the relevant data for context:\n{json.dumps(client_profile, default=str)}"
            response = model.generate_content(full_prompt)
            time.sleep(2)  # Increased delay to avoid rate limits
            return response.text
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = 30 * (attempt + 1)  # Progressive backoff
                st.warning(f"Rate limit reached. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                st.warning(f"Could not connect to Gemini API (attempt {attempt + 1}): {e}")
                break
    
    return None

def calculate_section_scores(section_name, user_data):
    section_data = user_data.get(section_name, {})
    scores = {}
    
    if section_name == 'Aptitude':
        for trait in APTITUDE:
            scores[trait] = section_data.get(trait, 0) / 10
    elif section_name in ['OCEAN', 'RIASEC']:
        for trait in globals()[section_name]:
            trait_scores = [
                options.index(section_data[f"{section_name}_{trait}_{i}"]) + 1 
                for i, (q, options) in enumerate(questions[section_name][trait], 1) 
                if f"{section_name}_{trait}_{i}" in section_data
            ]
            scores[trait] = ((sum(trait_scores) / len(trait_scores) if trait_scores else 1) - 1) * 2.5
    elif section_name == 'Hofstede':
        score_mapping = {
            'Not at all': 0, 'Not important': 0, 'Not uncomfortable at all': 0, 'Not resistant at all': 0,
            'Always rely on others': 0, 'Always prefer short-term': 0, 'Not freely at all': 0,
            'Not patient at all': 0, 'Not optimistic at all': 0, 'Very uncomfortable': 0,
            'Slightly': 2.5, 'Somewhat': 5, 'Very': 7.5, 'Extremely': 10,
            'Very important': 10, 'Always': 10
        }
        for trait in HOFSTEDE:
            trait_scores = [
                score_mapping.get(section_data.get(f"Hofstede_{trait}_{i}"), 5) 
                for i in range(1, 6)
            ]
            scores[trait] = sum(trait_scores) / len(trait_scores) if trait_scores else 0
    
    return scores

def recommend_careers(client_profile, career_clusters):
    recommendations = []
    for career, profile in career_clusters.items():
        client_riasec = client_profile['RIASEC']
        career_riasec = profile['RIASEC']
        
        if np.std(list(client_riasec.values())) == 0 or np.std(list(career_riasec.values())) == 0:
            riasec_similarity = 0
        else:
            riasec_similarity = np.corrcoef(list(client_riasec.values()), list(career_riasec.values()))[0, 1]
        
        score = (riasec_similarity + 1) * 50
        
        if not np.isnan(score):
            match_level = (
                "Best Fit" if riasec_similarity >= 0.7 else
                "Great Fit" if riasec_similarity >= 0.5 else
                "Good Fit" if riasec_similarity > 0 else
                "Not a Strong Match"
            )
            recommendations.append((career, score, match_level))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

# --- Graphing Functions ---
def create_aptitude_graph(aptitude_data):
    fig, ax = plt.subplots(figsize=(6, 4))
    traits = list(aptitude_data.keys())
    scores = [s * 10 for s in aptitude_data.values()]
    
    ax.bar(traits, scores, color=apple_blue.rgb())
    ax.set_ylim(0, 100)
    ax.set_title("Aptitude Profile")
    ax.set_ylabel("Score (%)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    plt.close(fig)
    return buf

def create_combined_trait_graph(trait_data, trait_category):
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})
    traits = list(trait_data.keys())
    scores = list(trait_data.values())
    
    angles = np.linspace(0, 2*np.pi, len(traits), endpoint=False).tolist()
    scores += scores[:1]
    angles += angles[:1]
    
    ax.plot(angles, scores, 'o-', linewidth=2, color=apple_green.rgb())
    ax.fill(angles, scores, alpha=0.25, color=apple_green.rgb())
    ax.set_thetagrids(np.degrees(angles[:-1]), traits)
    ax.set_ylim(0, 10)
    ax.spines['polar'].set_visible(False)
    plt.title(f"{trait_category} Profile", fontweight='bold', fontsize=14, pad=20)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def create_hofstede_graph(hofstede_data):
    fig, ax = plt.subplots(figsize=(8, 6))
    dimensions = list(hofstede_data.keys())
    scores = list(hofstede_data.values())
    y_pos = np.arange(len(dimensions))
    
    ax.barh(y_pos, scores, align='center', color=apple_blue.rgb())
    ax.set_yticks(y_pos)
    ax.set_yticklabels([TRAIT_FULL_NAMES.get(d, d) for d in dimensions])
    ax.invert_yaxis()
    ax.set_xlabel('Score')
    ax.set_title("Hofstede's Cultural Dimensions")
    ax.set_xlim(0, 10)
    
    for i, v in enumerate(scores):
        ax.text(v + 0.1, i, f"{v:.2f}", color='black', va='center')
    
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    plt.close(fig)
    return buf

def create_top_10_graph(career_recommendations):
    careers, scores, _ = zip(*career_recommendations)
    fig, ax = plt.subplots(figsize=(8, 5))
    
    bars = ax.barh(careers[::-1], scores[::-1], color=apple_green.rgb())
    ax.set_xlabel("Match Score (out of 100)")
    ax.set_title("Top Career Recommendations")
    
    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                f'{bar.get_width():.0f}', ha='left', va='center')
    
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def create_score_bar(score, width=4*inch, height=0.3*inch):
    drawing = Drawing(width, height)
    num_segments = 10
    segment_width = width / num_segments
    filled_segments = int(round(score / 10 * num_segments))
    
    for i in range(num_segments):
        drawing.add(Rect(
            i * segment_width, 0, segment_width - 2, height,
            fillColor=apple_green if i < filled_segments else apple_light_gray,
            strokeColor=None
        ))
    
    return drawing

# --- PDF Builder Functions ---
def get_score_category(score):
    return 'low' if score < 3.5 else 'high' if score > 6.5 else 'medium'

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 9)
    canvas.setFillColor(apple_blue)
    canvas.drawRightString(doc.width + doc.leftMargin, doc.height + doc.topMargin - 0.5 * inch, "Thinkareer")
    canvas.line(inch, doc.height + doc.topMargin - 0.55 * inch, doc.width + doc.leftMargin, doc.height + doc.topMargin - 0.55 * inch)
    canvas.drawString(inch, 0.75 * inch, f"Page {doc.page}")
    canvas.restoreState()

def _build_cover_page(story, client_profile, styles):
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Career Discovery Report", styles['AppleTitle']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Prepared for {client_profile['name']}", styles['AppleH2']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"Date: {client_profile['date']}", styles['AppleBody']))
    story.append(PageBreak())

def _build_table_of_contents(story, styles):
    story.append(Paragraph("Table of Contents", styles['AppleH1']))
    
    toc_data = [
        ("Personal Profile",),
        ("Aptitude Analysis",),
        ("Personality Analysis (OCEAN)",),
        ("Interest Analysis (RIASEC)",),
        ("Cultural Values Analysis (Hofstede)",),
        ("Top Career Recommendations",),
        ("Detailed Career Analysis",),
        ("Conclusion",)
    ]
    
    toc_table = Table(toc_data, colWidths=[6.5*inch], hAlign='LEFT')
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('TEXTCOLOR', (0,0), (-1,-1), apple_dark_gray),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LINEBELOW', (0,0), (-1,-1), 1, apple_light_gray)
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())

def _build_personal_profile_section(story, client_profile, styles):
    story.append(Paragraph("Personal Profile", styles['AppleH1']))
    
    profile_data = [
        ["Name:", client_profile['name']],
        ["Age:", str(client_profile['age'])],
        ["Email:", client_profile['email']],
        ["Phone:", client_profile['phone']],
        ["Status:", client_profile['status']]
    ]
    
    profile_table = Table(profile_data, colWidths=[1.5*inch, 4.5*inch], hAlign='LEFT')
    profile_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('TEXTCOLOR', (0,0), (-1,-1), apple_dark_gray),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')
    ]))
    
    story.append(profile_table)
    story.append(Spacer(1, 0.5*inch))
    story.append(PageBreak())

def _build_trait_analysis_section(story, client_profile, styles, category, traits):
    category_titles = {
        'Aptitude': 'Aptitude',
        'OCEAN': 'Personality',
        'RIASEC': 'Interest',
        'Hofstede': 'Cultural Values'
    }
    
    story.append(Paragraph(f"{category_titles[category]} Analysis", styles['AppleH1']))
    
    # Create appropriate graph
    if category == 'Aptitude':
        graph = create_aptitude_graph(client_profile[category])
    elif category == 'Hofstede':
        graph = create_hofstede_graph(client_profile[category])
    else:
        graph = create_combined_trait_graph(client_profile[category], category)
    
    if graph:
        story.append(Image(graph, width=6*inch, height=4*inch, hAlign='CENTER'))
    
    story.append(Spacer(1, 0.2*inch))
    
    for trait in traits:
        score = client_profile.get(category, {}).get(trait, 0)
        score_cat = get_score_category(score)
        
        story.append(Paragraph(f"{TRAIT_FULL_NAMES.get(trait, trait)}", styles['AppleH2']))
        story.append(create_score_bar(score))
        story.append(Spacer(1, 0.1*inch))
        
        meaning_text = trait_definitions.get(category, {}).get(trait, {}).get('meaning', 'N/A')
        story.append(Paragraph(f"<b>Meaning:</b> {meaning_text}", styles['AppleBody']))
        
        analysis_text = trait_definitions.get(category, {}).get(trait, {}).get('analysis', {}).get(score_cat, 'N/A')
        story.append(Paragraph(f"<b>Expert Analysis:</b> {analysis_text}", styles['AppleBody']))
        
        dev_plan_prompt = f"Based on a {score_cat} score in {trait} ({category}), suggest 2 very brief, one-line development points."
        dev_plan = get_gemini_analysis(dev_plan_prompt, client_profile) or fallback_content["development_plan"]
        
        story.append(Paragraph(f"<b>Development Plan:</b>", styles['AppleBody']))
        dev_points = [p.strip() for p in dev_plan.split("\n") if p.strip()]
        if dev_points:
            story.append(ListFlowable([Paragraph(p, styles['AppleList']) for p in dev_points], bulletType='bullet'))
        
        story.append(Spacer(1, 0.4*inch))
    
    story.append(PageBreak())

def _build_recommendations_section(story, career_recommendations, styles):
    story.append(Paragraph("Top Career Recommendations", styles['AppleH1']))
    story.append(Spacer(1, 0.2*inch))
    
    if career_recommendations:
        graph = create_top_10_graph(career_recommendations[:10])
        story.append(Image(graph, width=7*inch, height=5*inch, hAlign='CENTER'))
    
    story.append(PageBreak())

def _build_detailed_analysis_section(story, career_recommendations, client_profile, styles):
    story.append(Paragraph("Detailed Career Analysis", styles['AppleH1']))
    story.append(Spacer(1, 0.2*inch))
    
    for i, (career, score, match) in enumerate(career_recommendations[:3], 1):
        story.append(Paragraph(f"{i}. {career}", styles['AppleH2_Boxed']))
        story.append(Paragraph(f"Overall Match Score: {score:.0f}", styles['AppleSubtitle']))
        story.append(Spacer(1, 0.1*inch))
        
        career_desc = career_descriptions.get(career, "No description available for this career.")
        story.append(Paragraph(career_desc, styles['AppleBody']))
        story.append(Spacer(1, 0.3*inch))
        
        # SWOT Analysis
        swot_data = []
        prompts = {
            "S": f"For a person with this profile, what is their single greatest STRENGTH for a career as a {career}? Be concise and explain why in one or two sentences.",
            "W": f"What is their single greatest WEAKNESS or challenge they would face in a career as a {career}? Be concise and explain why in one or two sentences.",
            "O": f"What is a key OPPORTUNITY this person could leverage in a {career} career, based on their profile? Be concise and explain why in one or two sentences.",
            "T": f"What is a potential THREAT or external obstacle they should watch out for in a {career} career? Be concise and explain why in one or two sentences."
        }
        
        for key, prompt in prompts.items():
            response = get_gemini_analysis(prompt, client_profile) or fallback_content["swot"][key]
            swot_data.append([
                Paragraph(key, styles[f'SWOTKey_{key}']),
                Paragraph(response, styles['AppleBody'])
            ])
        
        swot_table = Table(swot_data, colWidths=[0.5*inch, 5.7*inch], hAlign='LEFT')
        swot_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LINEBELOW', (0,0), (-1,-2), 1, colors.lightgrey),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,1), (-1,-1), 12)
        ]))
        
        story.append(swot_table)
        story.append(Spacer(1, 0.5*inch))
        story.append(PageBreak())

def _build_conclusion(story, client_profile, styles):
    story.append(Paragraph("Conclusion", styles['AppleH1']))
    story.append(Spacer(1, 0.2*inch))
    
    conclusion_prompt = "Write a personalized, two-sentence conclusion for this career assessment report, encouraging the student."
    conclusion = get_gemini_analysis(conclusion_prompt, client_profile) or fallback_content["conclusion"]
    story.append(Paragraph(conclusion, styles['AppleBody']))

def generate_pdf_report(client_profile, career_recommendations):
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    doc.client_name = client_profile['name']
    
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=header_footer)])
    
    styles = getSampleStyleSheet()
    
    # Add custom styles
    styles.add(ParagraphStyle(name='AppleTitle', fontName='Helvetica-Bold', fontSize=32, textColor=apple_dark_gray, alignment=0, spaceAfter=24))
    styles.add(ParagraphStyle(name='AppleH1', fontName='Helvetica-Bold', fontSize=20, textColor=apple_blue, spaceAfter=16, leading=24))
    styles.add(ParagraphStyle(name='AppleH2', fontName='Helvetica-Bold', fontSize=14, textColor=apple_dark_gray, spaceAfter=8, leading=18))
    styles.add(ParagraphStyle(name='AppleBody', fontName='Helvetica', fontSize=11, textColor=apple_dark_gray, spaceAfter=12, leading=16))
    styles.add(ParagraphStyle(name='AppleList', parent=styles['AppleBody'], leftIndent=18))
    styles.add(ParagraphStyle(name='AppleSubtitle', fontName='Helvetica', fontSize=11, textColor=colors.grey, spaceBefore=-5, spaceAfter=12))
    styles.add(ParagraphStyle(name='AppleH2_Boxed', parent=styles['AppleH2'], backColor=apple_light_gray, borderColor=colors.lightgrey, borderWidth=1, borderPadding=8))
    
    # SWOT styles
    styles.add(ParagraphStyle(name='SWOTKey_S', fontName='Helvetica-Bold', fontSize=16, textColor=colors.white, backColor=apple_green, alignment=1, borderRadius=5, padding=5))
    styles.add(ParagraphStyle(name='SWOTKey_W', parent=styles['SWOTKey_S'], backColor=apple_orange))
    styles.add(ParagraphStyle(name='SWOTKey_O', parent=styles['SWOTKey_S'], backColor=apple_teal))
    styles.add(ParagraphStyle(name='SWOTKey_T', parent=styles['SWOTKey_S'], backColor=apple_red))
    
    story = []
    
    # Build all sections
    _build_cover_page(story, client_profile, styles)
    _build_table_of_contents(story, styles)
    _build_personal_profile_section(story, client_profile, styles)
    
    for category, traits in SECTION_TRAITS.items():
        _build_trait_analysis_section(story, client_profile, styles, category, traits)
    
    _build_recommendations_section(story, career_recommendations, styles)
    _build_detailed_analysis_section(story, career_recommendations, client_profile, styles)
    _build_conclusion(story, client_profile, styles)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Streamlit UI Page Functions ---
def introduction_page():
    st.header("👋 Welcome to Your Career Discovery Journey")
    st.markdown("This comprehensive assessment will help you understand your strengths, interests, and potential career paths. Please be honest and take your time.")

def basic_information_page():
    st.header("📝 Your Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.user_data['name'] = st.text_input(
            "Name", st.session_state.user_data.get('name', ''), placeholder="Enter your full name"
        )
    with col2:
        st.session_state.user_data['age'] = st.number_input(
            "Age", min_value=0, max_value=120, value=st.session_state.user_data.get('age', 18), step=1
        )
    
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.user_data['email'] = st.text_input(
            "Email", st.session_state.user_data.get('email', ''), placeholder="your.email@example.com"
        )
    with col4:
        st.session_state.user_data['phone'] = st.text_input(
            "Phone", st.session_state.user_data.get('phone', ''), placeholder="+1 (555) 123-4567"
        )

def current_status_page():
    st.header("🎓 Current Status")
    status_options = ["6-8th", "9-10th", "11-12th", "College", "Doing Job"]
    st.session_state.user_data['class_or_occupation'] = st.selectbox(
        "Select your current status:",
        status_options,
        index=status_options.index(st.session_state.user_data.get('class_or_occupation', "6-8th"))
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.user_data['class_or_occupation'] == "6-8th":
            st.session_state.user_data['exact_class'] = st.radio("What's the exact class?", ["6th", "7th", "8th"])
        elif st.session_state.user_data['class_or_occupation'] == "9-10th":
            st.session_state.user_data['exact_class'] = st.radio("What's the exact class?", ["9th", "10th"])
        elif st.session_state.user_data['class_or_occupation'] == "11-12th":
            st.session_state.user_data['exact_class'] = st.radio("What's the exact class?", ["11th", "12th"])
    
    with col2:
        if st.session_state.user_data['class_or_occupation'] == "9-10th":
            st.session_state.user_data['interested_stream'] = st.text_input("Any particular stream you are interested in?")
        elif st.session_state.user_data['class_or_occupation'] == "11-12th":
            st.session_state.user_data['specific_stream'] = st.radio("Stream:", ["Science Bio", "Science Math", "Commerce", "Arts", "Other"])
        elif st.session_state.user_data['class_or_occupation'] == "College":
            st.session_state.user_data['college_year'] = st.radio("In which year are you?", ["1st year", "2nd year", "3rd year", "4th year"])
            st.session_state.user_data['degree_pursuing'] = st.text_input("Which degree are you pursuing?")
        elif st.session_state.user_data['class_or_occupation'] == "Doing Job":
            st.session_state.user_data['years_experience'] = st.number_input("Years of experience?", min_value=0, step=1)
            st.session_state.user_data['current_work_profile'] = st.text_input("Current work profile?")
    
    if st.session_state.user_data['class_or_occupation'] in ["11-12th", "College", "Doing Job"]:
        st.session_state.user_data['given_competitive_exam'] = st.radio(
            "Have you given any competitive exam recently?", ["Yes", "No"], horizontal=True
        )
        if st.session_state.user_data.get('given_competitive_exam') == "Yes":
            st.session_state.user_data['comp_score'] = st.selectbox(
                "Select competitive Score Level", ["Very Bad", "Bad", "Average", "Good", "Very Good"]
            )

def academic_scores_page():
    st.header("📊 Academic Scores")
    class_labels = ["Current/Most Recent", "Previous Year", "Year Before That"]
    subjects = ["Maths", "English", "Overall"]
    score_options = ["<60%", "60%-80%", "80%-95%", ">95%"]
    
    if 'scores' not in st.session_state.user_data:
        st.session_state.user_data['scores'] = {}
    
    for i, year in enumerate(class_labels):
        st.subheader(year)
        cols = st.columns(3)
        for j, subject in enumerate(subjects):
            with cols[j]:
                st.session_state.user_data['scores'][f"{year}_{subject}"] = st.selectbox(
                    f"{subject}", score_options,
                    index=score_options.index(st.session_state.user_data['scores'].get(f"{year}_{subject}", "<60%")),
                    key=f"select_{year}_{subject}"
                )

def aptitude_page():
    st.header("🧠 Aptitude Assessment")
    st.info("Answer based on your ability. There is one correct answer per question.")
    
    aptitude_data = st.session_state.user_data.setdefault('Aptitude', {})
    
    for trait in APTITUDE:
        st.subheader(f"{APTITUDE_FULL_NAMES[trait]} Aptitude")
        for i, (q, opts, ans) in enumerate(aptitude_questions.get(trait, []), 1):
            aptitude_data[f"aptitude_{trait}_{i}"] = st.radio(
                f"{i}. {q}", opts,
                key=f"apt_{trait}_{i}",
                horizontal=True,
                index=opts.index(aptitude_data.get(f"aptitude_{trait}_{i}", opts[0]))
            )
        st.markdown("---")
    
    if st.button("Calculate & Save Aptitude Scores", use_container_width=True):
        scores = {}
        for trait in APTITUDE:
            correct_answers = sum(
                1 for i, (_, _, correct) in enumerate(aptitude_questions[trait], 1)
                if aptitude_data.get(f"aptitude_{trait}_{i}") == correct
            )
            scores[trait] = (correct_answers / len(aptitude_questions[trait])) * 100
        
        st.session_state.user_data['Aptitude'].update(scores)
        st.success("Aptitude scores saved!")

def interest_page():
    st.header("❤️ Interest Check (RIASEC)")
    st.info("Indicate your level of interest for each activity.")
    
    riasec_data = st.session_state.user_data.setdefault('RIASEC', {})
    
    for trait in RIASEC:
        st.subheader(trait)
        for i, (q, opts) in enumerate(questions['RIASEC'][trait], 1):
            riasec_data[f"RIASEC_{trait}_{i}"] = st.select_slider(
                f"{i}. {q}", opts,
                key=f"ria_{trait}_{i}",
                value=riasec_data.get(f"RIASEC_{trait}_{i}", opts[len(opts)//2])
            )
        st.markdown("---")

def personality_page():
    st.header("👤 Personality Check (OCEAN)")
    st.info("Indicate how well each statement describes you.")
    
    ocean_data = st.session_state.user_data.setdefault('OCEAN', {})
    
    for trait in OCEAN:
        st.subheader(trait)
        for i, (q, opts) in enumerate(questions['OCEAN'][trait], 1):
            ocean_data[f"OCEAN_{trait}_{i}"] = st.select_slider(
                f"{i}. {q}", opts,
                key=f"oc_{trait}_{i}",
                value=ocean_data.get(f"OCEAN_{trait}_{i}", opts[len(opts)//2])
            )
        st.markdown("---")

def culture_page():
    st.header("🌍 Cultural Values (Hofstede)")
    st.info("Indicate your agreement with each statement.")
    
    hofstede_data = st.session_state.user_data.setdefault('Hofstede', {})
    
    for trait in HOFSTEDE:
        st.subheader(TRAIT_FULL_NAMES[trait])
        for i, (q, opts) in enumerate(questions['Hofstede'][trait], 1):
            hofstede_data[f"Hofstede_{trait}_{i}"] = st.select_slider(
                f"{i}. {q}", opts,
                key=f"hof_{trait}_{i}",
                value=hofstede_data.get(f"Hofstede_{trait}_{i}", opts[len(opts)//2])
            )
        st.markdown("---")

def hobbies_interests_page():
    st.header("🎨 Hobbies and Interests")
    help_text = "Enter items separated by commas (e.g., Reading, Cooking, Hiking)"
    
    st.session_state.user_data['hobbies'] = st.text_area(
        "Enter your hobbies:",
        value=st.session_state.user_data.get('hobbies', ""),
        key='hobbies',
        help=help_text
    )
    st.session_state.user_data['interests'] = st.text_area(
        "Enter your interest areas:",
        value=st.session_state.user_data.get('interests', ""),
        key='interests',
        help=help_text
    )

def subjects_page():
    st.header("💡 Subjects and Skills")
    help_text = "Enter items separated by commas (e.g., Python, Public Speaking)"
    
    st.session_state.user_data['skills'] = st.text_area(
        "1. Your practical skills",
        value=st.session_state.user_data.get('skills', ""),
        key='skills1',
        help=help_text
    )
    st.session_state.user_data['competitive_subjects'] = st.text_area(
        "2. Easy competitive subjects",
        value=st.session_state.user_data.get('competitive_subjects', ""),
        key='skills2',
        help=help_text
    )
    st.session_state.user_data['easy_tasks'] = st.text_area(
        "3. Tasks you find easy",
        value=st.session_state.user_data.get('easy_tasks', ""),
        key='skills3',
        help=help_text
    )

def other_page():
    st.header("🎯 Other Information")
    help_text = "Enter items separated by commas"
    
    st.session_state.user_data['passion'] = st.text_area(
        "1. Your Passions",
        value=st.session_state.user_data.get('passion', ""),
        key='other1',
        help=help_text
    )
    st.session_state.user_data['big_problems'] = st.text_area(
        "2. Big Problems to Solve",
        value=st.session_state.user_data.get('big_problems', ""),
        key='other2',
        help=help_text
    )
    st.session_state.user_data['topics_of_interest'] = st.text_area(
        "3. Frequent Topics of Interest",
        value=st.session_state.user_data.get('topics_of_interest', ""),
        key='other3',
        help=help_text
    )

def report_page():
    st.header("✅ Final Step: Generate Your Report")
    st.info("You've completed all sections! The final questions below relate to resources and opportunities, which can influence career path choices.")
    
    help_text = "Enter items separated by commas"
    
    st.session_state.user_data['extra_benefit'] = st.text_area(
        '1. Career Advantages (e.g., family background, connections)',
        value=st.session_state.user_data.get('extra_benefit', ""),
        key='report1',
        help=help_text
    )
    st.session_state.user_data['future_opportunities'] = st.text_area(
        '2. Future Opportunities You See',
        value=st.session_state.user_data.get('future_opportunities', ""),
        key='report2',
        help=help_text
    )
    
    st.subheader("3. Financial Considerations")
    st.session_state.user_data['financial_condition'] = st.radio(
        "Financial condition:",
        ['Low', 'Mid', 'Rich'],
        index=['Low', 'Mid', 'Rich'].index(st.session_state.user_data.get('financial_condition', 'Mid')),
        horizontal=True
    )
    
    st.markdown("---")

    # Initialize PDF buffer in session state if not exists
    if 'pdf_buffer' not in st.session_state:
        st.session_state.pdf_buffer = None

    if st.button("Generate My Report & Save Results", use_container_width=True, type="primary"):
        # Validation
        if not st.session_state.user_data.get('name') or not st.session_state.user_data.get('email'):
            st.error("Please enter your name and email on the 'Basic Information' page.")
        else:
            with st.spinner("Analyzing your results... This may take a moment."):
                try:
                    # Prepare client profile
                    client_profile = prepare_client_profile(st.session_state.user_data)
                    
                    # Get career recommendations
                    recommendations = recommend_careers(client_profile, career_clusters)
                    
                    # Save to Google Sheets
                    save_successful = save_results_to_gsheet(client_profile, recommendations)
                    if save_successful:
                        st.success("Results saved to database successfully!")
                    else:
                        st.warning("Could not save results to the database, but you can still download your report.")
                    
                    # Generate PDF
                    st.session_state.pdf_buffer = generate_pdf_report(client_profile, recommendations)
                    
                    if st.session_state.pdf_buffer:
                        st.success("Success! Your report is ready for download below.")
                    else:
                        st.error("Failed to generate PDF report. Please check for errors above.")
                
                except Exception as e:
                    st.error(f"An error occurred while generating your report: {str(e)}")
    
    # Show download button if PDF is ready
    if st.session_state.pdf_buffer:
        user_name = st.session_state.user_data.get('name', 'User').replace(' ', '_')
        st.download_button(
            label="🎉 Download Your Career Report!",
            data=st.session_state.pdf_buffer,
            file_name=f"Career_Report_{user_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# --- Main App Logic ---
def main():
    st.set_page_config(page_title="Career Discovery", page_icon="🚀", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
            .stApp { background-color: #F0F2F6; }
            .stTextArea textarea {height: 80px !important;}
            .st-emotion-cache-16txtl3 { padding-top: 2rem; }
            [data-testid="stHeader"] { background-color: #FFFFFF; border-bottom: 1px solid #E5E5E5; }
            [data-testid="stSidebar"] { background-color: #FAFAFA; border-right: 1px solid #E5E5E5; }
            .stButton>button {
                border-radius: 0.5rem; font-weight: 600; border: 1px solid #0071E3;
                background-color: #FFFFFF; color: #0071E3;
            }
            .stButton>button:hover { border-color: #0056b3; color: #0056b3; }
            .st-emotion-cache-1ghh68j, .st-emotion-cache-gh2jqd {
                background-color: #0071E3; color: white; border: none;
            }
            .st-emotion-cache-1ghh68j:hover, .st-emotion-cache-gh2jqd:hover {
                 background-color: #0056b3; color: white;
            }
            .stProgress > div > div > div > div { background-image: linear-gradient(to right, #0071E3, #87CEFA); }
            h1 { font-weight: 700; color: #1D1D1F; padding-bottom: 1rem; }
            h2 { font-weight: 600; color: #1D1D1F; padding-top: 1rem;}
            h3 { font-weight: 600; color: #1D1D1F; }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'page' not in st.session_state:
        st.session_state.page = 1

    # Sidebar navigation
    with st.sidebar:
        st.title("Uttam Career")
        st.write("Navigate through the sections to complete your assessment.")
        
        PAGES = {
            "Introduction": 1, "Basic Information": 2, "Current Status": 3,
            "Academic Scores": 4, "Aptitude Assessment": 5, "Interest (RIASEC)": 6,
            "Personality (OCEAN)": 7, "Cultural Values": 8, "Hobbies & Interests": 9,
            "Subjects & Skills": 10, "Other Info": 11, "Generate Report": 12
        }
        
        selection = st.radio("Sections", list(PAGES.keys()), index=st.session_state.page - 1, key="nav_radio")
        st.session_state.page = PAGES[selection]
        
        st.markdown("---")
        if st.button("Restart Assessment", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key != 'page':
                    del st.session_state[key]
            st.session_state.page = 1
            st.rerun()
        
        st.info("Your progress is saved as you move between pages.")

    # Main content area
    main_container = st.container()
    
    with main_container:
        # Progress bar
        TOTAL_PAGES = len(PAGES)
        progress_percent = int(((st.session_state.page - 1) / (TOTAL_PAGES - 1)) * 100)
        st.progress(progress_percent, text=f"Step {st.session_state.page} of {TOTAL_PAGES}")
        st.markdown("<hr>", unsafe_allow_html=True)

        # Page routing
        page_functions = {
            1: introduction_page, 2: basic_information_page, 3: current_status_page,
            4: academic_scores_page, 5: aptitude_page, 6: interest_page,
            7: personality_page, 8: culture_page, 9: hobbies_interests_page,
            10: subjects_page, 11: other_page, 12: report_page
        }
        
        # Execute current page function
        page_functions[st.session_state.page]()
        
        # Navigation buttons
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.session_state.page < TOTAL_PAGES:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 3, 1])
            
            if st.session_state.page > 1:
                if col1.button("⬅️ Previous", use_container_width=True):
                    st.session_state.page -= 1
                    st.rerun()
            
            if col3.button("Next ➡️", use_container_width=True, type="primary"):
                st.session_state.page += 1
                st.rerun()

if __name__ == "__main__":
    main()
