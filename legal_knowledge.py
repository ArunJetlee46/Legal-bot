"""
Legal knowledge base for common Indian legal topics.
Each topic contains keywords for intent detection and a structured response.
NLP-enhanced matching uses Porter stemming and synonym expansion.
"""

from __future__ import annotations

from nlp_processor import preprocess_query, stem

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

    "sc_st_rights": {
        "keywords": [
            "dalit", "scheduled caste", "scheduled tribe", "atrocity",
            "atrocities", "untouchability", "caste discrimination", "caste violence",
            "caste abuse", "tribal", "adivasi", "reservation sc", "obc", "backward class",
            "अनुसूचित जाति", "अनुसूचित जनजाति", "दलित", "आदिवासी", "जातिगत भेदभाव",
            "अत्याचार",
        ],
        "title": "SC/ST Rights & Anti-Atrocity Protection",
        "summary": (
            "The Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989 "
            "provides strong legal protection to Dalits and Adivasis against caste-based violence, "
            "discrimination, and humiliation."
        ),
        "details": [
            "**SC/ST Atrocities Act, 1989 (amended 2018)** – Covers offences like forced labour, social boycott, "
            "land dispossession, verbal humiliation, and physical violence based on caste.",
            "**Special Courts** – Designated Special Courts must try atrocity cases, ensuring faster justice.",
            "**No Anticipatory Bail** – Accused persons cannot easily get anticipatory bail; victims are protected.",
            "**Immediate Relief** – Victims/families are entitled to government-mandated financial relief "
            "(travel, food, medical, legal, economic rehabilitation).",
            "**Article 17** of the Constitution – Abolishes untouchability; its practice in any form is a punishable offence.",
            "**Reservation** – SC/ST persons are entitled to reservations in government jobs (15%/7.5%) and "
            "educational institutions under Articles 15(4) and 16(4).",
            "**Forest Rights Act, 2006** – Protects tribal communities' rights over forest land and resources.",
        ],
        "steps": [
            "1. File an FIR at the nearest police station; if refused, approach the **Superintendent of Police (SP)**.",
            "2. Contact the **SC/ST Commission** helpline: **14566** (National Commission for SC/ST).",
            "3. Approach the **Special Public Prosecutor** or **Special Court** for SC/ST cases in your district.",
            "4. Apply for victim relief/compensation through the **District Collector/DM** office.",
            "5. Contact **Ambedkar Foundation** or state-level Dalit/tribal welfare departments for support.",
        ],
        "law": "SC/ST (Prevention of Atrocities) Act 1989 (amended 2018); Constitution Articles 15, 16, 17, 46",
    },

    "criminal_rights": {
        "keywords": [
            "arrest", "arrested", "police", "fir", "bail", "custody", "detained",
            "detention", "lockup", "handcuff", "interrogation", "accused", "crime",
            "criminal", "charge", "chargesheet", "magistrate", "remand", "warrant",
            "गिरफ्तारी", "पुलिस", "जमानत", "एफआईआर", "हिरासत", "आरोपी",
        ],
        "title": "Rights During Arrest & Criminal Proceedings",
        "summary": (
            "Every person in India has constitutional and statutory rights during arrest, "
            "police custody, and criminal proceedings that police must respect."
        ),
        "details": [
            "**Right to Know Grounds of Arrest** – Police must inform you of the reason for arrest (Article 22(1)).",
            "**Right to a Lawyer** – You can consult and be defended by a lawyer of your choice from the time of arrest.",
            "**Right to be Produced Before Magistrate** – Within **24 hours** of arrest (excluding travel time); Article 22(2).",
            "**Right Against Self-Incrimination** – You cannot be compelled to be a witness against yourself (Article 20(3)).",
            "**Right to Bail** – For bailable offences, bail is a right. For non-bailable offences, apply to a magistrate.",
            "**No Third-Degree** – Torture, custodial violence, and degrading treatment are prohibited and constitute offences.",
            "**FIR Registration** – Police must register an FIR for cognizable offences; refusal is punishable. "
            "You can also register an FIR online in many states or via the **National Cyber Crime Reporting Portal**.",
            "**Women's Rights During Arrest** – A woman cannot be arrested after sunset or before sunrise except in exceptional cases. "
            "Female police officer must be present during the arrest of a woman.",
            "**BNSS, 2023** – The Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 has replaced the CrPC from July 2024.",
        ],
        "steps": [
            "1. If arrested, immediately ask for the **reason for arrest** and your **right to contact a lawyer**.",
            "2. Demand to be produced before a **Magistrate within 24 hours**.",
            "3. Apply for bail at the **Magistrate's Court** (Sessions Court for non-bailable offences).",
            "4. File a complaint about police misconduct/custodial violence with the **State Human Rights Commission** "
            "or **National Human Rights Commission (NHRC)**: nhrc.nic.in / helpline **14433**.",
            "5. For FIR refusal, file a complaint to the **SP/DSP** or approach the **Magistrate** under Section 156(3) BNSS.",
            "6. Get free legal aid from **DLSA** (District Legal Services Authority) helpline: **15100**.",
        ],
        "law": "Constitution Articles 20–22; Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023; Bharatiya Nyaya Sanhita (BNS) 2023",
    },

    "women_rights": {
        "keywords": [
            "woman", "women", "gender", "maternity", "pregnancy", "posh", "sexual harassment",
            "workplace harassment", "equal pay", "rape", "assault", "molest", "eve teasing",
            "stalking", "dowry death", "widows", "divorce", "maintenance", "alimony",
            "महिला", "यौन उत्पीड़न", "मातृत्व", "तलाक", "गुजारा भत्ता", "बलात्कार",
        ],
        "title": "Women's Rights",
        "summary": (
            "Indian law provides comprehensive protections for women against discrimination, "
            "workplace harassment, domestic abuse, and denial of equal rights."
        ),
        "details": [
            "**POSH Act, 2013** – Every workplace with 10+ employees must have an **Internal Complaints Committee (ICC)**. "
            "Women can report sexual harassment to the ICC or Local Complaints Committee (LCC) within **90 days**.",
            "**Maternity Benefit Act, 1961 (amended 2017)** – Women employees are entitled to **26 weeks** of paid maternity leave "
            "(12 weeks for third child). Applies to establishments with 10+ employees.",
            "**Equal Remuneration Act, 1976** – Men and women must receive equal pay for the same or similar work.",
            "**Rape & Sexual Assault** – Covered under Bharatiya Nyaya Sanhita (BNS) 2023; victim's statement recorded by "
            "female magistrate; identity protected by law.",
            "**Section 498A BNS** – Cruelty by husband or his relatives is a cognizable and non-bailable offence.",
            "**Maintenance Rights** – Women can claim maintenance under Section 125 CrPC (now BNSS) and personal laws "
            "even during judicial separation.",
            "**Dowry Death (Section 80 BNS)** – If a woman dies within 7 years of marriage under suspicious circumstances, "
            "the husband's family is presumed guilty.",
            "**Women's Reservation** – 33% reservation for women in Parliament and State Legislatures (Constitution 106th Amendment Act, 2023).",
        ],
        "steps": [
            "1. For workplace sexual harassment, file a complaint with the **ICC** or **LCC** of your district within 90 days.",
            "2. For rape/assault, file an FIR immediately; police are obligated to record it. Call **112** or **1091** (Women Helpline).",
            "3. Visit a **One Stop Centre (Sakhi)**: Call **181** for medical, legal, shelter, and police support.",
            "4. For maternity leave denial, file a complaint with the **Labour Commissioner** or **Shram Suvidha Portal**.",
            "5. For maintenance, approach the **Family Court** or **Magistrate Court** under Section 144 BNSS.",
            "6. Contact **NCW** (National Commission for Women): ncwapps.nic.in or helpline **7827170170**.",
        ],
        "law": "POSH Act 2013; Maternity Benefit Act 1961; BNS 2023 (Sections 63–99); Hindu Marriage Act 1955",
    },

    "disability_rights": {
        "keywords": [
            "disability", "disabled", "differently abled", "handicap", "blind", "deaf",
            "wheelchair", "mental illness", "autism", "cerebral palsy", "pwd", "rpwd",
            "special needs", "benchmark disability", "reservation disability", "divyang",
            "विकलांग", "दिव्यांग", "अपंग", "विकलांगता",
        ],
        "title": "Disability Rights",
        "summary": (
            "The Rights of Persons with Disabilities (RPWD) Act, 2016 guarantees equal rights, "
            "non-discrimination, and accessibility for persons with disabilities in India."
        ),
        "details": [
            "**21 Types of Disabilities** recognised including visual, hearing, locomotor, intellectual, "
            "mental illness, autism, cerebral palsy, dwarfism, acid attack victims, and Parkinson's disease.",
            "**Reservation** – **4% reservation** in government jobs for persons with benchmark disabilities "
            "(1% each for blindness/low vision, deaf/hard of hearing, locomotor disability, and multiple disabilities).",
            "**Free Education** – Children with disabilities aged 6–18 have the right to **free inclusive education** in neighbourhood schools.",
            "**Accessibility** – Public buildings, transport, and ICT must be made accessible; violations can be reported.",
            "**Unique Disability ID (UDID)** – A national disability identity card providing access to benefits and schemes.",
            "**Chief Commissioner of Disabilities** – Oversees implementation and hears complaints at national level.",
            "**State Commissioner of Disabilities** – Addresses complaints at the state level.",
            "**Anti-Discrimination** – Discrimination in employment, education, and public facilities is prohibited and punishable.",
        ],
        "steps": [
            "1. Obtain a **Disability Certificate** from a government hospital/medical board to access benefits.",
            "2. Apply for a **UDID Card** online at: **swavlambancard.gov.in**",
            "3. File a complaint about discrimination or denial of rights with the **State Commissioner for Persons with Disabilities**.",
            "4. For inaccessible government buildings/services, file a complaint with the **Chief Commissioner for Disabilities**: ccd.nic.in",
            "5. For employment discrimination, approach the **Equal Opportunity Officer** in the organisation or file with the State Commissioner.",
            "6. Access government schemes: **Assistive Devices Scheme (ADIP)**, NHFDC loans, and state disability welfare schemes.",
        ],
        "law": "Rights of Persons with Disabilities (RPWD) Act, 2016; Constitution Article 41",
    },

    "senior_citizen_rights": {
        "keywords": [
            "senior citizen", "elderly", "old age", "parents", "maintenance parents",
            "pension", "aged", "retirement", "elder abuse", "neglect parents",
            "बुजुर्ग", "वृद्ध", "वरिष्ठ नागरिक", "माता-पिता", "पेंशन", "बुढ़ापा",
        ],
        "title": "Senior Citizen Rights",
        "summary": (
            "The Maintenance and Welfare of Parents and Senior Citizens Act, 2007 ensures "
            "that senior citizens receive maintenance from children and relatives, and are "
            "protected from abandonment and abuse."
        ),
        "details": [
            "**Right to Maintenance** – Children and relatives are legally bound to provide maintenance to parents "
            "and senior citizens who cannot support themselves.",
            "**Maintenance Tribunal** – District-level tribunals hear maintenance applications; orders must be passed within **90 days**.",
            "**Maximum Maintenance** – Up to **₹10,000/month** under the central Act (states can increase this).",
            "**Property Protection** – If a senior citizen transfers property to a relative on the condition of "
            "maintenance and the relative fails, the transfer can be **declared void**.",
            "**Old Age Homes** – States must establish at least one old age home per district (capacity: 150+).",
            "**Helpline for Elders** – Dedicated elder helpline for complaints and support.",
            "**Pension Schemes** – National Social Assistance Programme (NSAP) provides pensions to destitute elderly, "
            "widows, and persons with disabilities.",
            "**Senior Citizen Savings Scheme (SCSS)** – Government-backed savings scheme with higher interest rates for those 60+.",
        ],
        "steps": [
            "1. File a maintenance application with the **Sub-Divisional Magistrate (SDM)** or the Maintenance Tribunal.",
            "2. Call the **Elder Helpline: 14567** (ELDERLINE, toll-free) for support and complaints.",
            "3. If property was transferred but maintenance denied, apply to the **Tribunal** to void the transfer.",
            "4. For physical abuse or neglect, file an FIR or approach the local police station.",
            "5. Apply for pension under **IGNOAPS** (Indira Gandhi National Old Age Pension Scheme) via your local Panchayat/municipality.",
            "6. Contact **HelpAge India**: 1800-180-1253 (toll-free) for elder care support.",
        ],
        "law": "Maintenance and Welfare of Parents and Senior Citizens Act, 2007; National Social Assistance Programme",
    },

    "cyber_crime": {
        "keywords": [
            "cyber", "cybercrime", "online fraud", "hacking", "phishing", "otp fraud",
            "upi fraud", "scam", "internet", "social media", "fake profile",
            "data theft", "identity theft", "ransomware", "sextortion", "blackmail",
            "online harassment", "it act", "digital", "bank fraud",
            "साइबर", "ऑनलाइन धोखा", "हैकिंग", "ओटीपी फ्रॉड", "साइबर अपराध",
        ],
        "title": "Cyber Crime & Digital Rights",
        "summary": (
            "The Information Technology (IT) Act, 2000 and related laws protect citizens from "
            "online fraud, hacking, harassment, and financial cyber crimes."
        ),
        "details": [
            "**IT Act, 2000 (amended 2008)** – Key offences: hacking (Section 66), identity theft (Section 66C), "
            "online cheating (Section 66D), cyber stalking/harassment (Section 67), and sending obscene material.",
            "**BNS 2023** – Cyber crimes including online fraud and harassment are also covered under the "
            "Bharatiya Nyaya Sanhita, 2023.",
            "**Online Financial Fraud** – Fraudulent UPI/bank transactions can be reported to the bank immediately "
            "to freeze the transaction, and to the cyber crime portal.",
            "**Sextortion / Blackmail** – Sharing intimate images without consent is a criminal offence under "
            "Section 67A of IT Act and Section 97 BNS.",
            "**Phishing / OTP Fraud** – Never share OTP, CVV, or banking passwords. Report immediately.",
            "**Fake Social Media Profiles** – Impersonation is punishable under Section 66D of the IT Act.",
            "**Data Privacy** – The Digital Personal Data Protection Act, 2023 (DPDP) gives citizens rights over "
            "their personal data held by companies.",
            "**Cyber Bullying** – Repeated online harassment is punishable; screenshots serve as evidence.",
        ],
        "steps": [
            "1. Report immediately at the **National Cyber Crime Reporting Portal**: **cybercrime.gov.in**",
            "2. Call the **Cyber Crime Helpline: 1930** (toll-free, 24/7) to freeze fraudulent transactions.",
            "3. For online financial fraud, **call your bank immediately** to block the card/account.",
            "4. File an FIR at the **nearest police station** or Cyber Crime Police Station in your city.",
            "5. Preserve evidence: **take screenshots**, save URLs, record transaction IDs before reporting.",
            "6. For harassment/sextortion, approach the **One Stop Centre (181)** or Women Helpline **(1091)** if the victim is a woman.",
        ],
        "law": "Information Technology Act 2000 (amended 2008); BNS 2023; Digital Personal Data Protection Act 2023",
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
    Match user query to a legal topic using NLP-enhanced keyword matching.

    Scoring combines:
    - Exact substring keyword hit: 3 pts each
    - Stemmed keyword match: 2 pts each (catches plurals, conjugations, etc.)
    - Synonym-expanded token match: 1 pt each

    Returns the best-matching topic dict or None if no match found.
    """
    if not query:
        return None

    query_lower = query.lower()
    _, expanded_tokens = preprocess_query(query)

    best_match = None
    best_score = 0

    for topic_key, topic_data in LEGAL_TOPICS.items():
        score = 0
        for kw in topic_data["keywords"]:
            kw_lower = kw.lower()
            # Exact substring match (highest weight)
            if kw_lower in query_lower:
                score += 3
            else:
                # Stemmed match (handles plurals and verb forms)
                kw_stem = stem(kw_lower)
                if kw_stem in expanded_tokens:
                    score += 2

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
