import re
from datetime import datetime
from typing import Dict, Any, Optional

DEPARTMENT_RULES = [
    {
        "keywords": ["bijli", "transformer", "power", "electric", "current", "wire", "voltage", "meter", "line"],
        "ministry": "Ministry of Power / State Electricity Distribution Company (DISCOM)",
        "sub_category": "Electricity Supply / Burnt Transformer / Infrastructure Delay",
        "act_citation": "Section 43 & Section 57 of the Electricity Act, 2003 read with State Electricity Regulatory Commission (Consumer Grievance Redressal Forum & Ombudsman) Regulations",
        "urgency": "HIGH",
        "stipulated_timeframe": "48 Hours (Under Citizen Charter for transformer restoration)"
    },
    {
        "keywords": ["ration", "kotedar", "pds", "food", "dealer", "quota", "grain", "wheat", "rice", "bpl card"],
        "ministry": "Department of Food and Public Distribution, Ministry of Consumer Affairs",
        "sub_category": "Targeted Public Distribution System (TPDS) / Fair Price Shop Irregularity",
        "act_citation": "National Food Security Act (NFSA), 2013 (Sections 3, 15, and 40) & Essential Commodities Act, 1955",
        "urgency": "HIGH",
        "stipulated_timeframe": "7 Working Days"
    },
    {
        "keywords": ["kisan", "farmer", "patwari", "khasra", "khatauni", "crop", "fasal", "dbt", "pm-kisan", "pm kisan"],
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "sub_category": "Direct Benefit Transfer (DBT) Disbursement / PM-Kisan Portal Discrepancy",
        "act_citation": "PM-Kisan Operational Guidelines (Chapter IV: Fund Transfer Mechanism) & Aadhaar (Targeted Delivery of Financial Subsidies) Act, 2016",
        "urgency": "MEDIUM",
        "stipulated_timeframe": "15 Working Days"
    },
    {
        "keywords": ["paani", "water", "jal", "nal", "sewer", "drainage", "pipe", "drinking water", "tap"],
        "ministry": "Ministry of Jal Shakti / Department of Drinking Water and Sanitation",
        "sub_category": "Jal Jeevan Mission / Public Water Supply Contamination & Outage",
        "act_citation": "Constitution of India Article 21 (Right to Safe Drinking Water) & Jal Jeevan Mission Operational Framework",
        "urgency": "HIGH",
        "stipulated_timeframe": "72 Hours"
    },
    {
        "keywords": ["bank", "account", "dbt", "manager", "pension", "branch", "atm", "unauthorized debit"],
        "ministry": "Department of Financial Services, Ministry of Finance",
        "sub_category": "Banking Services / DBT Inactivation / Branch Unresponsiveness",
        "act_citation": "Reserve Bank - Integrated Ombudsman Scheme, 2021 & Banking Regulation Act, 1949",
        "urgency": "MEDIUM",
        "stipulated_timeframe": "30 Working Days"
    },
    {
        "keywords": ["sadak", "road", "pothole", "highway", "panchayat", "kachha rasta", "contractor", "bridge"],
        "ministry": "Ministry of Rural Development / State PWD",
        "sub_category": "Pradhan Mantri Gram Sadak Yojana (PMGSY) / Rural Road Infrastructure",
        "act_citation": "PMGSY Standard Bidding Document Quality Control Norms & State Panchayati Raj Act",
        "urgency": "MEDIUM",
        "stipulated_timeframe": "15 Working Days"
    },
    {
        "keywords": ["hospital", "doctor", "medicine", "dawa", "ayushman", "nurse", "clinic", "health", "bed"],
        "ministry": "Ministry of Health and Family Welfare",
        "sub_category": "Government Healthcare Facility / PM-JAY Cashless Denial",
        "act_citation": "Clinical Establishments (Registration and Regulation) Act, 2010 & National Health Authority (NHA) Grievance Guidelines",
        "urgency": "HIGH",
        "stipulated_timeframe": "48 Hours"
    }
]

DEFAULT_DEPARTMENT = {
    "ministry": "Department of Administrative Reforms and Public Grievances (DARPG)",
    "sub_category": "General Administrative Non-feasance / Public Service Delivery Delay",
    "act_citation": "Right to Public Services Act (State-specific) & Citizens' Charter Mandate",
    "urgency": "MEDIUM",
    "stipulated_timeframe": "30 Days"
}

def analyze_and_draft_grievance(
    raw_text: str,
    citizen_name: str = "Aggrieved Citizen",
    location: str = "Rural District, India",
    contact_phone: str = "[Citizen Contact]",
    complaint_ref_no: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parses conversational or raw grievance text and produces a high-level, cited CPGRAMS petition.
    """
    text_lower = raw_text.lower()
    
    # 1. Classify Department & Regulatory Framework
    matched_dept = DEFAULT_DEPARTMENT
    for dept in DEPARTMENT_RULES:
        if any(kw in text_lower for kw in dept["keywords"]):
            matched_dept = dept
            break

    today_str = datetime.now().strftime("%d-%B-%Y")
    ref_id = complaint_ref_no or f"CPG/{datetime.now().strftime('%Y%m')}/{abs(hash(raw_text)) % 1000000:06d}"

    # Generate title/subject
    first_sentence = raw_text.strip().split(".")[0][:120]
    subject_en = f"GRIEVANCE REGARDING: {matched_dept['sub_category'].upper()} - IMMEDIATE REDRESSAL SOUGHT"
    subject_hi = f"शिकायत पत्र: {matched_dept['sub_category']} के संबंध में त्वरित निस्तारण हेतु प्रार्थना"

    # Build Formal English Petition
    petition_english = f"""BEFORE THE COMPETENT ADMINISTRATIVE AUTHORITY
CPGRAMS / PUBLIC GRIEVANCE REGISTRATION PORTAL

Grievance Tracking Reference: {ref_id}
Date of Submission: {today_str}
Complainant: {citizen_name}
Jurisdiction / Location: {location}
Contact Details: {contact_phone}

TO:
The Nodal Grievance Officer,
{matched_dept['ministry']}
Government of India / Competent State Authority

SUBJECT: {subject_en}

RESPECTED SIR / MADAM,

1. PRELIMINARY STATEMENT & JURISDICTION:
The Complainant is a bonafide citizen and resident of {location}. This formal grievance is instituted under the mandate of the Public Grievance Redressal Mechanism and Citizens' Charter, seeking immediate intervention regarding administrative omission and public service failure.

2. FACTUAL BACKGROUND & CHRONOLOGY:
The grievance arose from the following documented circumstances:
"{raw_text.strip()}"

Despite verbal intimations and reasonable opportunity afforded to the concerned local field functionaries, the grievance has remained unresolved, thereby causing severe public distress, financial loss, and violation of citizen welfare entitlements.

3. STATUTORY FRAMEWORK & VIOLATIONS:
The failure or delay in question constitutes a violation of:
- Statutory Reference: {matched_dept['act_citation']}
- Citizens' Charter Mandate: Prescribed resolution timeline of {matched_dept['stipulated_timeframe']}
- Principles of Natural Justice and administrative accountability.

4. PRAYER FOR RELIEF (SPECIFIC REMEDY SOUGHT):
In light of the facts and statutory mandates, the Complainant respectfully prays that the Competent Authority may be pleased to:
(a) Direct the jurisdictional executive officers to immediately redress the issue on top priority within the stipulated charter window;
(b) Conduct an administrative inquiry to ascertain accountability for the unaddressed delay;
(c) Provide written or digital confirmation of resolution and upload the final Action Taken Report (ATR) to the CPGRAMS portal for citizen verification.

VERIFICATION:
I, {citizen_name}, do hereby solemnly verify and affirm that the contents stated above are true and correct to the best of my knowledge and belief.

Sincerely,
{citizen_name}
Dated: {today_str}
"""

    # Build Formal Vernacular Hindi Petition
    petition_hindi = f"""सेवा में,
श्रीमान नोडल लोक शिकायत अधिकारी / सक्षम प्राधिकारी,
{matched_dept['ministry']},
भारत सरकार / संबंधित राज्य प्रशासन।

शिकायत संदर्भ संख्या: {ref_id}
दिनांक: {today_str}
आवेदक का नाम: {citizen_name}
स्थान / पता: {location}
संपर्क सूत्र: {contact_phone}

विषय: {subject_hi}

महोदय / महोदया,

सविनय निवेदन है कि प्रार्थी {citizen_name}, निवासी {location} का स्थायी नागरिक है। प्रार्थी अत्यंत क्षुब्ध होकर निम्नलिखित जनहित एवं व्यक्तिगत समस्या को आपके संज्ञान में ला रहा है:

१. समस्या का विवरण (तथ्यात्मक स्थिति):
"{raw_text.strip()}"

२. पूर्व में किए गए प्रयास एवं लापरवाही:
इस विषय में स्थानीय संबंधित कर्मचारियों एवं अधिकारियों को बार-बार मौखिक व व्यक्तिगत रूप से अवगत कराया गया, परंतु आज तक कोई ठोस उपचारात्मक कार्यवाही नहीं की गई है। इस लापरवाही से प्रार्थी एवं स्थानीय निवासियों को अत्यधिक मानसिक, शारीरिक एवं आर्थिक परेशानी का सामना करना पड़ रहा है।

३. वैधानिक संदर्भ एवं नागरिक अधिकार:
यह समस्या निम्नलिखित वैधानिक प्रावधानों के अंतर्गत समाधान योग्य है:
- संबंधित विधान/अधिनियम: {matched_dept['act_citation']}
- नागरिक अधिकार पत्र (Citizens' Charter) के तहत निर्धारित निस्तारण अवधि: {matched_dept['stipulated_timeframe']}

४. प्रार्थना / राहत की मांग:
अतः श्रीमान जी से विनम्र प्रार्थना है कि:
(क) संबंधित अधीनस्थ अधिकारियों को अविलंब मौके पर स्थलीय निरीक्षण एवं समस्या के तत्काल समाधान का आदेश पारित किया जाए;
(ख) नागरिक अधिकार पत्र की समय-सीमा के भीतर कृत कार्यवाही आख्या (ATR) प्रार्थी को प्रेषित की जाए।

भवदीय,
{citizen_name}
दिनांक: {today_str}
"""

    # CPGRAMS Portal Compact Text (under 2000 chars, ideal for text area copy-paste)
    cpgrams_compact = f"REF:{ref_id} | DEPT:{matched_dept['ministry']} | SUB:{matched_dept['sub_category']} | DETAILS:{raw_text.strip()} | LEGAL:{matched_dept['act_citation']} | PRAYER:Immediate resolution within {matched_dept['stipulated_timeframe']}. Applicant: {citizen_name}, Loc: {location}"

    spoken_summary_hi = f"आपकी शिकायत को {matched_dept['ministry']} के लिए आधिकारिक प्रारूप में तैयार कर दिया गया है। संदर्भ संख्या है {ref_id}। इसमें नागरिक अधिकार पत्र और {matched_dept['stipulated_timeframe']} की समय-सीमा का उल्लेख किया गया है।"

    return {
        "reference_id": ref_id,
        "ministry": matched_dept["ministry"],
        "sub_category": matched_dept["sub_category"],
        "act_citation": matched_dept["act_citation"],
        "urgency": matched_dept["urgency"],
        "stipulated_timeframe": matched_dept["stipulated_timeframe"],
        "subject_en": subject_en,
        "subject_hi": subject_hi,
        "petition_english": petition_english.strip(),
        "petition_hindi": petition_hindi.strip(),
        "cpgrams_compact": cpgrams_compact[:1950],
        "spoken_summary_hi": spoken_summary_hi,
        "date": today_str
    }
