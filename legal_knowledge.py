"""
Legal knowledge base for common Indian legal topics.
Each topic contains keywords for intent detection and a structured response.
"""

LEGAL_TOPICS = {
    "consumer_rights": {
        "keywords": [
            "consumer", "product", "defective", "refund", "warranty", "complaint",
            "cheated", "fraud", "seller", "service", "deficiency", "e-commerce",
            "online shopping", "purchased", "goods", "उपभोक्ता", "शिकायत", "धोखा",
        ],
        "title": "Consumer Rights",
        "summary": (
            "Under the Consumer Protection Act, 2019, every consumer has the right to "
            "be protected against defective goods and deficient services."
        ),
        "details": [
            "**Right to Safety** – Protection against hazardous goods and services.",
            "**Right to Information** – Know the quality, quantity, purity, and price of goods.",
            "**Right to Choose** – Access to a variety of goods at competitive prices.",
            "**Right to be Heard** – Your complaints must be addressed by Consumer Forums.",
            "**Right to Redressal** – Seek compensation for unfair trade practices.",
            "**Right to Consumer Education** – Awareness about consumer rights.",
        ],
        "steps": [
            "1. File a complaint with the National Consumer Helpline: **1800-11-4000** (toll-free).",
            "2. Visit the Consumer Disputes Redressal Commission (CDRC) at your district level.",
            "3. For online complaints, visit: **consumerhelpline.gov.in**",
            "4. File a complaint online at the **CONFONET** portal (confonet.nic.in).",
        ],
        "law": "Consumer Protection Act, 2019",
    },

    "rti": {
        "keywords": [
            "rti", "right to information", "information", "government", "public authority",
            "application", "file rti", "transparency", "सूचना का अधिकार", "जानकारी",
        ],
        "title": "Right to Information (RTI)",
        "summary": (
            "The Right to Information Act, 2005 empowers every citizen to request "
            "information from public authorities within 30 days."
        ),
        "details": [
            "Any citizen can file an RTI application to any government body.",
            "Public authorities must respond within **30 days** (48 hours if life/liberty is at stake).",
            "Fee: **₹10** (BPL cardholders are exempt from fees).",
            "Applies to all central, state, and local government bodies.",
            "First Appeal to the senior officer if response is unsatisfactory.",
            "Second Appeal to the Information Commission (CIC/SIC).",
        ],
        "steps": [
            "1. Write an application addressing the Public Information Officer (PIO) of the department.",
            "2. Clearly state the information you seek.",
            "3. Pay ₹10 via demand draft, postal order, or cash.",
            "4. Submit to the PIO of the concerned public authority.",
            "5. File online at: **rtionline.gov.in** for central government departments.",
        ],
        "law": "Right to Information Act, 2005",
    },

    "labor_rights": {
        "keywords": [
            "labour", "labor", "worker", "employee", "salary", "wages", "fired",
            "dismissed", "employer", "job", "work", "overtime", "minimum wage",
            "provident fund", "pf", "esi", "gratuity", "श्रमिक", "मजदूर", "वेतन",
            "नौकरी", "काम",
        ],
        "title": "Labour Rights",
        "summary": (
            "Indian labour laws protect workers from exploitation and ensure fair wages, "
            "safe working conditions, and social security benefits."
        ),
        "details": [
            "**Minimum Wages** – Every worker is entitled to state-notified minimum wages.",
            "**Payment of Wages** – Wages must be paid on time (Wages Act, 1936).",
            "**Provident Fund (EPF)** – Mandatory 12% contribution from employer for establishments with 20+ employees.",
            "**ESI** – Medical benefits for workers earning up to ₹21,000/month.",
            "**Gratuity** – Payable after 5 years of continuous service (15 days' salary per year).",
            "**Equal Pay** – Equal pay for equal work regardless of gender.",
            "**No Child Labour** – Children below 14 cannot be employed in hazardous work.",
        ],
        "steps": [
            "1. File a complaint with the **Labour Commissioner** in your district.",
            "2. Contact the **Labour Helpline: 1800-11-6090** (toll-free).",
            "3. For EPF/ESI grievances, visit **epfindia.gov.in** or **esic.in**.",
            "4. File online complaint at **Shram Suvidha Portal**: shramsuvidha.gov.in",
        ],
        "law": "Minimum Wages Act 1948, Payment of Wages Act 1936, Industrial Disputes Act 1947",
    },

    "domestic_violence": {
        "keywords": [
            "domestic violence", "abuse", "husband", "wife", "beaten", "threat",
            "harassment", "dowry", "marital", "protection order", "shelter",
            "घरेलू हिंसा", "मारपीट", "दहेज", "पत्नी", "महिला",
        ],
        "title": "Protection from Domestic Violence",
        "summary": (
            "The Protection of Women from Domestic Violence Act, 2005 protects women from "
            "physical, emotional, sexual, and economic abuse within households."
        ),
        "details": [
            "Covers physical, verbal, emotional, sexual, and economic abuse.",
            "Women can seek **Protection Orders** to stop the abuser from repeating violence.",
            "Right to **Residence Orders** – the woman cannot be evicted from the shared household.",
            "Right to **Monetary Relief** – compensation for losses and maintenance.",
            "**Custody Orders** – temporary custody of children can be obtained.",
            "Applies to marriages, live-in relationships, and family relationships.",
        ],
        "steps": [
            "1. **Emergency: Call 112** (Police) or **1091** (Women Helpline).",
            "2. Contact the **Protection Officer** in your area (appointed by the state government).",
            "3. Approach the **Magistrate's Court** to file for a protection/residence order.",
            "4. Visit a **One Stop Centre (Sakhi)** for integrated support: **181** helpline.",
            "5. Contact **NCW** (National Commission for Women): ncwapps.nic.in",
        ],
        "law": "Protection of Women from Domestic Violence Act, 2005; Dowry Prohibition Act, 1961",
    },

    "fundamental_rights": {
        "keywords": [
            "fundamental rights", "constitution", "rights", "equality", "freedom",
            "discrimination", "caste", "religion", "speech", "liberty", "education",
            "मौलिक अधिकार", "संविधान", "समानता", "स्वतंत्रता",
        ],
        "title": "Fundamental Rights",
        "summary": (
            "Part III of the Indian Constitution (Articles 12–35) guarantees six fundamental "
            "rights to all citizens."
        ),
        "details": [
            "**Article 14** – Right to Equality: Equal treatment before the law.",
            "**Article 15** – No discrimination on grounds of religion, race, caste, sex, or place of birth.",
            "**Article 17** – Abolition of Untouchability (a criminal offence).",
            "**Article 19** – Freedom of speech, assembly, movement, and profession.",
            "**Article 21** – Right to Life and Personal Liberty.",
            "**Article 21A** – Right to free and compulsory education (6–14 years).",
            "**Article 22** – Protection against arbitrary arrest and detention.",
            "**Article 32** – Right to move the Supreme Court for enforcement of fundamental rights.",
        ],
        "steps": [
            "1. If your fundamental rights are violated, file a **Writ Petition** in the High Court (Article 226) or Supreme Court (Article 32).",
            "2. Contact the **National Human Rights Commission (NHRC)**: nhrc.nic.in",
            "3. Call NHRC helpline: **14433**",
            "4. Contact State Human Rights Commissions for state-level violations.",
        ],
        "law": "Constitution of India, Articles 12–35",
    },

    "legal_aid": {
        "keywords": [
            "legal aid", "lawyer", "advocate", "free legal", "poor", "affordable",
            "court", "case", "help", "nalsa", "slsa", "dlsa", "मुफ्त कानूनी",
            "वकील", "सहायता", "कोर्ट",
        ],
        "title": "Free Legal Aid",
        "summary": (
            "Under the Legal Services Authorities Act, 1987, eligible individuals are entitled "
            "to free legal representation and advice."
        ),
        "details": [
            "Free legal aid is available to: women, children, SC/ST persons, workers, persons with disabilities, "
            "victims of trafficking, and people with annual income below ₹3 lakh (central) or state-fixed limits.",
            "Services include: free legal advice, representation in courts/tribunals, printing of documents.",
            "**NALSA** (National Legal Services Authority) oversees legal aid at the national level.",
            "**SLSA** (State Legal Services Authority) at state level.",
            "**DLSA** (District Legal Services Authority) at district level.",
            "**Lok Adalats** offer fast, free, and amicable dispute resolution.",
        ],
        "steps": [
            "1. Visit your nearest **District Legal Services Authority (DLSA)** office.",
            "2. Call the **NALSA Helpline: 15100** (toll-free).",
            "3. Apply online at: **nalsa.gov.in**",
            "4. For Lok Adalat dates, contact your district court.",
        ],
        "law": "Legal Services Authorities Act, 1987",
    },

    "tenant_rights": {
        "keywords": [
            "tenant", "rent", "landlord", "eviction", "house", "lease", "rent agreement",
            "rent increase", "deposit", "accommodation", "किरायेदार", "मकान मालिक",
            "किराया", "बेदखल",
        ],
        "title": "Tenant Rights",
        "summary": (
            "Tenants in India are protected against arbitrary eviction, unfair rent hikes, "
            "and harassment by landlords under state Rent Control Acts."
        ),
        "details": [
            "Landlords **cannot evict** tenants without a valid reason (e.g., non-payment, personal need).",
            "Eviction requires a notice period (usually 15–30 days depending on the state).",
            "**Security deposit** is capped at 2 months' rent in many states.",
            "Rent cannot be increased arbitrarily—check your state's Rent Control Act.",
            "Always get a **registered rent agreement** (notarised/registered with sub-registrar).",
            "The **Model Tenancy Act, 2021** provides a modern framework for tenancy disputes.",
        ],
        "steps": [
            "1. If facing illegal eviction, approach the **Rent Controller** in your city.",
            "2. File a complaint with the local **Rent Tribunal/Authority**.",
            "3. Contact a legal aid centre if you cannot afford a lawyer.",
            "4. Always maintain a written rent agreement and keep payment receipts.",
        ],
        "law": "State Rent Control Acts; Model Tenancy Act, 2021",
    },

    "property_rights": {
        "keywords": [
            "property", "land", "inheritance", "succession", "will", "deed",
            "registration", "dispute", "encroachment", "mutation", "सम्पत्ति",
            "जमीन", "वसीयत", "विरासत",
        ],
        "title": "Property & Land Rights",
        "summary": (
            "Indian law protects citizens' rights over immovable property, including land, "
            "houses, and ancestral property."
        ),
        "details": [
            "**Registration** – Property transactions above ₹100 must be registered under Registration Act, 1908.",
            "**Mutation** – After purchase, get property mutated in your name in municipal records.",
            "**Women's Inheritance** – Daughters have equal rights in Hindu Undivided Family (HUF) property (Hindu Succession Amendment Act, 2005).",
            "**Will** – A registered Will is the safest way to pass property to heirs.",
            "**Encroachment** – File an FIR or civil suit if someone encroaches on your land.",
            "**RERA** – Homebuyers are protected by the Real Estate (Regulation and Development) Act, 2016.",
        ],
        "steps": [
            "1. For property disputes, file a civil suit in the **Civil Court** of jurisdiction.",
            "2. For RERA complaints (real estate fraud), approach the **State RERA Authority**.",
            "3. For land records, visit your **Tehsildar/Patwari** or check state land record portals.",
            "4. Contact the **National Land Records Modernisation Programme (DILRMP)**: dilrmp.gov.in",
        ],
        "law": "Transfer of Property Act 1882, Hindu Succession Act 1956 (as amended 2005), RERA 2016",
    },

    "child_rights": {
        "keywords": [
            "child", "children", "minor", "school", "education", "child labour",
            "abuse", "adoption", "juvenile", "pocso", "बच्चा", "बाल", "शिक्षा",
            "बाल मजदूरी",
        ],
        "title": "Child Rights",
        "summary": (
            "Indian law ensures children's rights to education, protection from exploitation, "
            "and safety from abuse."
        ),
        "details": [
            "**Right to Education (RTE)** – Free and compulsory education for children aged 6–14 (Article 21A).",
            "**Child Labour** – Employment of children below 14 is prohibited (Child Labour Act, 1986, amended 2016).",
            "**POCSO Act** – Protection of Children from Sexual Offences Act, 2012 provides strict punishment for child abuse.",
            "**Juvenile Justice** – Children in conflict with law are treated under Juvenile Justice Act, 2015.",
            "**Child Marriage** – Prohibited under Prohibition of Child Marriage Act, 2006 (boys <21, girls <18).",
            "**Adoption** – Governed by Hindu Adoption and Maintenance Act / CARA guidelines.",
        ],
        "steps": [
            "1. Report child abuse to **Childline: 1098** (24/7 toll-free helpline).",
            "2. For child labour complaints, contact the **District Labour Commissioner**.",
            "3. For POCSO complaints, file an FIR at the nearest police station immediately.",
            "4. Contact **NCPCR** (National Commission for Protection of Child Rights): ncpcr.gov.in",
        ],
        "law": "RTE Act 2009, POCSO Act 2012, Child Labour (Prohibition & Regulation) Act 1986",
    },
}

GREETINGS = [
    "hello", "hi", "hey", "namaste", "namaskar", "help", "start",
    "नमस्ते", "नमस्कार", "हेलो", "হ্যালো", "வணக்கம்", "నమస్కారం",
]

GRATITUDE = [
    "thank", "thanks", "dhanyawad", "shukriya", "धन्यवाद", "शुक्रिया",
    "நன்றி", "ధన్యవాదాలు",
]


def find_topic(query: str) -> dict | None:
    """
    Match user query to a legal topic using keyword matching.
    Returns the topic dict or None if no match found.
    """
    query_lower = query.lower()
    best_match = None
    best_score = 0

    for topic_key, topic_data in LEGAL_TOPICS.items():
        score = sum(1 for kw in topic_data["keywords"] if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = topic_data

    return best_match if best_score > 0 else None


def is_greeting(query: str) -> bool:
    """Return True if query is a greeting."""
    query_lower = query.lower().strip()
    return any(g in query_lower for g in GREETINGS)


def is_gratitude(query: str) -> bool:
    """Return True if query expresses thanks."""
    query_lower = query.lower().strip()
    return any(g in query_lower for g in GRATITUDE)


def get_topics_list() -> list[dict]:
    """Return a list of all available topics with title and key."""
    return [
        {"key": key, "title": data["title"]}
        for key, data in LEGAL_TOPICS.items()
    ]


def get_topic_by_key(key: str) -> dict | None:
    """Retrieve a topic by its key."""
    return LEGAL_TOPICS.get(key)
