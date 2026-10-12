from typing import Dict, List, Any, Optional

GOVERNMENT_SCHEMES: List[Dict[str, Any]] = [
    {
        "id": "pm-kisan",
        "name": "PM-Kisan Samman Nidhi",
        "hindi_name": "प्रधानमंत्री किसान सम्मान निधि",
        "category": "Agriculture & Farmers",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "benefit_summary": "₹6,000 per year in three equal installments of ₹2,000 directly transferred into the farmer's bank account.",
        "hindi_benefit": "सालाना ₹6,000 की वित्तीय सहायता, तीन समान किस्तों (₹2,000 प्रत्येक) में सीधे बैंक खाते में।",
        "criteria": {
            "occupation": ["farmer", "kisan", "agriculture"],
            "landholding": True,
            "min_age": 18,
            "excludes_taxpayers": True
        },
        "documents": [
            "Aadhaar Card (आधार कार्ड)",
            "Land ownership records / Khasra-Khatauni (जमीन के कागजात / खसरा-खतौनी)",
            "Active Bank Account with Aadhaar seeded (आधार से लिंक बैंक पासबुक)",
            "Mobile number linked to Aadhaar (मोबाइल नंबर)"
        ],
        "application_steps": [
            "Step 1: Visit pmkisan.gov.in or Common Service Centre (CSC / जन सेवा केंद्र).",
            "Step 2: Enter Aadhaar Number and land survey details.",
            "Step 3: Complete e-KYC via OTP or biometric authentication.",
            "Step 4: Verification by Local Village Patwari / Nodal Agriculture Officer."
        ],
        "official_url": "https://pmkisan.gov.in"
    },
    {
        "id": "ayushman-bharat",
        "name": "Ayushman Bharat PM-JAY",
        "hindi_name": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
        "category": "Healthcare & Wellness",
        "ministry": "Ministry of Health and Family Welfare / NHA",
        "benefit_summary": "Cashless health cover up to ₹5 Lakh per family per year for secondary and tertiary hospitalization across empanelled hospitals.",
        "hindi_benefit": "प्रति परिवार प्रति वर्ष ₹5 लाख तक का मुफ्त कैशलेस इलाज देश के सरकारी व सूचीबद्ध निजी अस्पतालों में।",
        "criteria": {
            "max_income_lakhs": 2.5,
            "socio_economic": ["BPL", "SECC 2011 Deprived", "EWS", "low_income"],
            "all_ages": True
        },
        "documents": [
            "Aadhaar Card of all family members",
            "Ration Card / BPL Card (राशन कार्ड)",
            "Mobile number for OTP verification"
        ],
        "application_steps": [
            "Step 1: Check eligibility on beneficiaries.nha.gov.in or call 14555.",
            "Step 2: Visit nearest Ayushman Mitra at any district hospital or CSC center.",
            "Step 3: Biometric verification and instant generation of Golden Card (Ayushman Card)."
        ],
        "official_url": "https://beneficiary.nha.gov.in"
    },
    {
        "id": "pmay",
        "name": "Pradhan Mantri Awas Yojana (PMAY)",
        "hindi_name": "प्रधानमंत्री आवास योजना (ग्रामीण एवं शहरी)",
        "category": "Housing & Shelter",
        "ministry": "Ministry of Housing and Urban Affairs / MoRD",
        "benefit_summary": "Financial grant of ₹1.20 Lakh (plains) to ₹1.30 Lakh (hilly areas) for building a pucca house + 90 days MGNREGA wages + ₹12,000 for toilet construction.",
        "hindi_benefit": "पक्का मकान बनाने के लिए ₹1.20 लाख से ₹1.30 लाख की सीधी सहायता, साथ ही शौचालय निर्माण और मनरेगा मजदूरी का लाभ।",
        "criteria": {
            "houseless_or_kutcha": True,
            "no_pucca_house_in_india": True,
            "max_income_lakhs": 3.0
        },
        "documents": [
            "Aadhaar Card",
            "Ration Card",
            "Bank Account linked with Aadhaar",
            "Job Card Number (MGNREGA)",
            "Swachh Bharat Mission (SBM) toilet registration number"
        ],
        "application_steps": [
            "Step 1: Contact Gram Panchayat / Gram Sevak or visit pmayg.nic.in / pmaymis.gov.in.",
            "Step 2: Geo-tagging of current kutcha dwelling by official inspector.",
            "Step 3: Sanction order issued; funds credited in 3 construction milestone phases."
        ],
        "official_url": "https://pmayg.nic.in"
    },
    {
        "id": "pm-vishwakarma",
        "name": "PM Vishwakarma Scheme",
        "hindi_name": "प्रधानमंत्री विश्वकर्मा योजना",
        "category": "Artisans & Crafts",
        "ministry": "Ministry of Micro, Small and Medium Enterprises (MSME)",
        "benefit_summary": "Skill training with ₹500/day stipend, ₹15,000 modern toolkit incentive, and collateral-free enterprise loans up to ₹3 Lakh at concessional 5% interest.",
        "hindi_benefit": "कारीगरों को ₹15,000 का टूलकिट अनुदान, ₹500/दिन प्रशिक्षण वजीफा, और बिना गारंटी ₹3 लाख तक का सस्ता ऋण (5% ब्याज)।",
        "criteria": {
            "min_age": 18,
            "occupation": [
                "carpenter", "blacksmith", "potter", "sculptor", "cobbler", "mason",
                "basket_maker", "doll_maker", "barber", "garland_maker", "washerman", "tailor", "fishing_net_maker", "artisan"
            ]
        },
        "documents": [
            "Aadhaar Card",
            "Mobile linked with Aadhaar",
            "Bank details",
            "Skill / Artisan Trade declaration"
        ],
        "application_steps": [
            "Step 1: Biometric registration at CSC Center on pmvishwakarma.gov.in.",
            "Step 2: Gram Panchayat & Urban Local Body 3-tier verification.",
            "Step 3: 5-7 days basic skill training at designated Skill India Centre."
        ],
        "official_url": "https://pmvishwakarma.gov.in"
    },
    {
        "id": "pm-svanidhi",
        "name": "PM SVANidhi (Street Vendor Loan)",
        "hindi_name": "पीएम स्वनिधि योजना (स्ट्रीट वेंडर आत्मनिर्भर निधि)",
        "category": "Micro Credit & Livelihood",
        "ministry": "Ministry of Housing and Urban Affairs",
        "benefit_summary": "Collateral-free working capital loan of ₹10,000 (1st tranche), ₹20,000 (2nd tranche), and ₹50,000 (3rd tranche) with 7% interest subsidy & cashback on digital transactions.",
        "hindi_benefit": "रेहड़ी-पटरी विक्रेताओं को बिना किसी गारंटी के ₹10,000 से ₹50,000 तक का सस्ता व्यापार ऋण और डिजिटल लेनदेन पर कैशबैक।",
        "criteria": {
            "occupation": ["street_vendor", "hawker", "thelawala", "small_vendor", "daily_wager"],
            "urban_or_periurban": True
        },
        "documents": [
            "Certificate of Vending (CoV) / Identity Card issued by Urban Local Body",
            "Aadhaar Card",
            "Bank Account Passbook"
        ],
        "application_steps": [
            "Step 1: Apply online on pmsvanidhi.mohua.gov.in or through lending bank / CSC.",
            "Step 2: Urban local body verification.",
            "Step 3: Direct loan disbursal into bank account within 7 to 10 days."
        ],
        "official_url": "https://pmsvanidhi.mohua.gov.in"
    },
    {
        "id": "sukanya-samriddhi",
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "hindi_name": "सुकन्या समृद्धि योजना (बेटी बचाओ, बेटी पढ़ाओ)",
        "category": "Girl Child & Education",
        "ministry": "Ministry of Finance",
        "benefit_summary": "High guaranteed interest rate (8.2%), 100% tax exemption under Section 80C, matures when daughter turns 21 years old.",
        "hindi_benefit": "बेटियों के उज्ज्वल भविष्य के लिए 8.2% की उच्चतम ब्याज दर, आयकर छूट और 21 वर्ष में परिपक्वता पर सुरक्षित मोटी रकम।",
        "criteria": {
            "gender": "female",
            "max_age": 10,
            "target": "girl_child"
        },
        "documents": [
            "Birth Certificate of girl child (बेटी का जन्म प्रमाण पत्र)",
            "Identity and Address proof of Guardian (माता-पिता का आधार/पैन)",
            "Passport size photos"
        ],
        "application_steps": [
            "Step 1: Visit nearest Post Office (डाकघर) or commercial bank branch.",
            "Step 2: Fill Form-1 with minimum deposit of ₹250.",
            "Step 3: Passbook issued on the spot; deposit up to ₹1.5 Lakh annually."
        ],
        "official_url": "https://www.indiapost.gov.in"
    },
    {
        "id": "atal-pension",
        "name": "Atal Pension Yojana (APY)",
        "hindi_name": "अटल पेंशन योजना",
        "category": "Social Security & Pension",
        "ministry": "Ministry of Finance / PFRDA",
        "benefit_summary": "Guaranteed monthly pension of ₹1,000 to ₹5,000 for life starting from age 60, followed by spouse pension and full corpus returned to nominee.",
        "hindi_benefit": "60 वर्ष की आयु के बाद ₹1,000 से ₹5,000 प्रति माह की आजीवन निश्चित सरकारी पेंशन।",
        "criteria": {
            "min_age": 18,
            "max_age": 40,
            "excludes_taxpayers": True,
            "unorganized_sector": True
        },
        "documents": [
            "Savings Bank Account with Auto-Debit facility",
            "Aadhaar Card",
            "Nominee details"
        ],
        "application_steps": [
            "Step 1: Contact your bank branch or use Internet Banking / mobile app.",
            "Step 2: Fill APY registration form and choose pension slab (₹1000 - ₹5000).",
            "Step 3: PRAN (Permanent Retirement Account Number) generated instantly."
        ],
        "official_url": "https://www.npscra.nsdl.co.in"
    },
    {
        "id": "mgnrega",
        "name": "MGNREGA (Job Card)",
        "hindi_name": "महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार गारंटी अधिनियम (मनरेगा)",
        "category": "Rural Employment",
        "ministry": "Ministry of Rural Development",
        "benefit_summary": "Legal guarantee of 100 days of unskilled wage employment per fiscal year to every rural household whose adult members volunteer to do manual work.",
        "hindi_benefit": "ग्रामीण परिवारों को हर वर्ष कम से कम 100 दिनों के अकुशल रोजगार की कानूनी गारंटी और समय पर सीधे बैंक खाते में पारिश्रमिक।",
        "criteria": {
            "min_age": 18,
            "rural": True,
            "manual_labor_willingness": True
        },
        "documents": [
            "Aadhaar Card",
            "Passport photograph of adult members",
            "Ration Card / proof of residence in Gram Panchayat",
            "Bank / Post Office account passbook"
        ],
        "application_steps": [
            "Step 1: Submit written application or oral request to Gram Panchayat / Rozgar Sahayak.",
            "Step 2: Job Card issued within 15 days of application free of charge.",
            "Step 3: Submit application for work; employment must be provided within 15 days or unemployment allowance is paid."
        ],
        "official_url": "https://nrega.nic.in"
    }
]

def match_schemes(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Intelligently match user profile against government welfare schemes.
    """
    eligible = []
    potential = []
    
    age = user_profile.get("age")
    gender = str(user_profile.get("gender", "")).lower()
    occupation = str(user_profile.get("occupation", "")).lower()
    income = float(user_profile.get("annual_income_lakhs", 2.0))
    has_land = bool(user_profile.get("has_land", False))
    is_rural = bool(user_profile.get("is_rural", True))
    is_taxpayer = bool(user_profile.get("is_taxpayer", False))

    for scheme in GOVERNMENT_SCHEMES:
        crit = scheme.get("criteria", {})
        reasons_eligible = []
        missing_criteria = []

        # Age check
        if "min_age" in crit and age is not None:
            if age < crit["min_age"]:
                missing_criteria.append(f"Age must be at least {crit['min_age']}")
        if "max_age" in crit and age is not None:
            if age > crit["max_age"]:
                missing_criteria.append(f"Age must be at most {crit['max_age']}")

        # Taxpayer check
        if crit.get("excludes_taxpayers") and is_taxpayer:
            missing_criteria.append("Income taxpayers are excluded from this scheme")

        # Occupation check
        if "occupation" in crit:
            occ_list = crit["occupation"]
            matched_occ = any(o in occupation for o in occ_list)
            if matched_occ:
                reasons_eligible.append(f"Occupation matches: {occupation}")
            else:
                missing_criteria.append(f"Designated for {', '.join(occ_list[:4])}")

        # Land check
        if crit.get("landholding"):
            if has_land or "kisan" in occupation or "farmer" in occupation:
                reasons_eligible.append("Landholder / Cultivator status confirmed")
            else:
                missing_criteria.append("Requires cultivable agricultural land")

        # Income check
        if "max_income_lakhs" in crit:
            if income <= crit["max_income_lakhs"]:
                reasons_eligible.append(f"Income within threshold (<= ₹{crit['max_income_lakhs']} Lakhs)")
            else:
                missing_criteria.append(f"Income exceeds ₹{crit['max_income_lakhs']} Lakh limit")

        # Rural check
        if crit.get("rural") and not is_rural:
            missing_criteria.append("Applicable for rural residents")

        # Evaluate score
        if len(missing_criteria) == 0:
            eligible.append({
                **scheme,
                "status": "ELIGIBLE",
                "confidence": "High",
                "qualification_points": reasons_eligible
            })
        elif len(missing_criteria) <= 1:
            potential.append({
                **scheme,
                "status": "PARTIALLY_ELIGIBLE",
                "confidence": "Medium",
                "missing_reasons": missing_criteria,
                "qualification_points": reasons_eligible
            })

    # Generate Hindi & English spoken guidance summary
    total_found = len(eligible) + len(potential)
    if eligible:
        top_scheme = eligible[0]
        hindi_summary = f"बधाई हो! आपकी जानकारी के अनुसार आप मुख्य रूप से '{top_scheme['hindi_name']}' के लिए पात्र हैं। {top_scheme['hindi_benefit']}"
        english_summary = f"Great news! Based on your profile, you are strongly eligible for '{top_scheme['name']}'. {top_scheme['benefit_summary']}"
    elif potential:
        top_scheme = potential[0]
        hindi_summary = f"आप '{top_scheme['hindi_name']}' के लिए विचार कर सकते हैं, हालांकि कुछ विवरणों की पुष्टि आवश्यक है।"
        english_summary = f"You may qualify for '{top_scheme['name']}', subject to verification of documents."
    else:
        hindi_summary = "हमने योजनाओं की समीक्षा की है। कृपया अपनी आय या व्यवसाय का सटीक विवरण दर्ज करें।"
        english_summary = "Please provide additional details regarding your occupation or family status to match specific schemes."

    return {
        "eligible_schemes": eligible,
        "potential_schemes": potential,
        "total_matched": total_found,
        "hindi_summary": hindi_summary,
        "english_summary": english_summary
    }
