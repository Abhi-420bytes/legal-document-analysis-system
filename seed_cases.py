"""
Seed ChromaDB with 80 Indian court case summaries (10 per class × 8 classes).
Run once:  python seed_cases.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

CASES = [
    # ── CRIMINAL ──────────────────────────────────────────────────────────────
    {
        "id": "cr_001", "case_type": "criminal",
        "title": "State of Maharashtra v. Ajay Sharma",
        "court": "Bombay High Court", "year": "2021",
        "sections": "Section 302 IPC, Section 34 IPC",
        "outcome": "Convicted. Life imprisonment awarded.",
        "text": (
            "The accused Ajay Sharma was charged under Section 302 IPC for the murder of "
            "Ramesh Gupta. FIR was registered at Andheri Police Station. The prosecution "
            "produced eyewitness testimony and forensic evidence. The court found the accused "
            "guilty beyond reasonable doubt and sentenced him to life imprisonment under "
            "Section 302 IPC read with Section 34 IPC."
        ),
    },
    {
        "id": "cr_002", "case_type": "criminal",
        "title": "Rajiv Nair v. State of Kerala",
        "court": "Kerala High Court", "year": "2020",
        "sections": "Section 376 IPC, Section 164 CrPC",
        "outcome": "Accused convicted. 10 years rigorous imprisonment.",
        "text": (
            "The accused was charged under Section 376 IPC for sexual assault. The victim "
            "recorded her statement under Section 164 CrPC before the Magistrate. Medical "
            "examination corroborated the victim's account. The court convicted the accused "
            "and sentenced him to 10 years rigorous imprisonment with fine."
        ),
    },
    {
        "id": "cr_003", "case_type": "criminal",
        "title": "CBI v. Suresh Mehta",
        "court": "Delhi High Court", "year": "2022",
        "sections": "Section 420 IPC, Section 120B IPC",
        "outcome": "Accused convicted for cheating and conspiracy.",
        "text": (
            "The accused Suresh Mehta was charged with criminal conspiracy under Section 120B "
            "and cheating under Section 420 IPC for defrauding investors of Rs. 5 crores through "
            "a fake investment scheme. The CBI filed a charge sheet after thorough investigation. "
            "The special court convicted the accused and sentenced him to 7 years imprisonment."
        ),
    },
    {
        "id": "cr_004", "case_type": "criminal",
        "title": "State of UP v. Mohan Lal",
        "court": "Allahabad High Court", "year": "2019",
        "sections": "Section 395 IPC, Section 397 IPC",
        "outcome": "Bail rejected. Charge sheet filed.",
        "text": (
            "The accused persons were arrested for committing dacoity with deadly weapons under "
            "Sections 395 and 397 IPC. The police recovered stolen property and weapons from "
            "the accused. The bail application was rejected by the Magistrate. The Sessions "
            "Court framed charges and committed the case for trial."
        ),
    },
    {
        "id": "cr_005", "case_type": "criminal",
        "title": "Pradeep Kumar v. State of Punjab",
        "court": "Punjab and Haryana High Court", "year": "2023",
        "sections": "Section 498A IPC, Section 406 IPC",
        "outcome": "FIR quashed. Matter settled.",
        "text": (
            "The petitioner sought quashing of FIR registered under Sections 498A and 406 IPC "
            "for dowry harassment and criminal breach of trust. Both parties reached an amicable "
            "settlement and the wife withdrew the complaint. The High Court quashed the FIR "
            "in exercise of its jurisdiction under Section 482 CrPC."
        ),
    },
    {
        "id": "cr_006", "case_type": "criminal",
        "title": "State of Gujarat v. Bharat Patel",
        "court": "Gujarat High Court", "year": "2021",
        "sections": "Section 307 IPC, Section 34 IPC",
        "outcome": "Convicted for attempt to murder. 7 years imprisonment.",
        "text": (
            "The accused was charged with attempt to murder under Section 307 IPC after "
            "attacking the victim with a sharp weapon causing grievous injuries. The "
            "prosecution established common intention under Section 34 IPC. The court "
            "convicted the accused and sentenced him to 7 years rigorous imprisonment."
        ),
    },
    {
        "id": "cr_007", "case_type": "criminal",
        "title": "State of Karnataka v. Ravi Shankar",
        "court": "Karnataka High Court", "year": "2022",
        "sections": "NDPS Act Section 20, Section 37",
        "outcome": "Convicted for drug trafficking. 10 years imprisonment.",
        "text": (
            "The accused was arrested for possession and trafficking of narcotics under "
            "the NDPS Act. Large quantity of contraband was recovered from his vehicle. "
            "The Special Court convicted him under Section 20 of the NDPS Act and "
            "sentenced him to 10 years rigorous imprisonment with heavy fine."
        ),
    },
    {
        "id": "cr_008", "case_type": "criminal",
        "title": "Amit Kumar v. State of Haryana",
        "court": "Punjab and Haryana High Court", "year": "2020",
        "sections": "Section 304B IPC, Section 498A IPC",
        "outcome": "Convicted for dowry death. Life imprisonment.",
        "text": (
            "The husband and in-laws were charged with dowry death under Section 304B IPC "
            "following the unnatural death of the wife within 7 years of marriage. "
            "Evidence of dowry demands and harassment established. Court convicted all "
            "accused and sentenced them to life imprisonment under Section 304B IPC."
        ),
    },
    {
        "id": "cr_009", "case_type": "criminal",
        "title": "State v. Vikram Singh",
        "court": "Rajasthan High Court", "year": "2023",
        "sections": "Section 279 IPC, Section 304A IPC",
        "outcome": "Convicted for rash driving causing death.",
        "text": (
            "The accused caused death of a pedestrian by rash and negligent driving of "
            "his vehicle at high speed. He was charged under Sections 279 and 304A IPC. "
            "The court found him guilty of causing death by negligence and sentenced him "
            "to 2 years imprisonment with suspension of driving licence."
        ),
    },
    {
        "id": "cr_010", "case_type": "criminal",
        "title": "State of Maharashtra v. Cyber Fraudster",
        "court": "Bombay High Court", "year": "2023",
        "sections": "IT Act Section 66C, Section 66D, IPC Section 420",
        "outcome": "Convicted for cyber fraud. 3 years imprisonment.",
        "text": (
            "The accused committed cyber fraud by creating fake banking websites and "
            "stealing credentials of customers causing financial losses of Rs. 2 crores. "
            "He was charged under the IT Act for identity theft and cheating under IPC "
            "Section 420. Court convicted him and sentenced to 3 years imprisonment."
        ),
    },
    # ── CIVIL ─────────────────────────────────────────────────────────────────
    {
        "id": "cv_001", "case_type": "civil",
        "title": "Anita Sharma v. Apollo Hospitals",
        "court": "Delhi High Court", "year": "2021",
        "sections": "Consumer Protection Act, Tort of Negligence",
        "outcome": "Rs. 25 lakhs compensation awarded for medical negligence.",
        "text": (
            "The plaintiff filed a suit for damages alleging medical negligence by Apollo "
            "Hospitals resulting in permanent disability. The court found that the hospital "
            "breached its duty of care by performing a wrong procedure. Compensation of "
            "Rs. 25 lakhs was awarded to the plaintiff under the law of tort for negligence."
        ),
    },
    {
        "id": "cv_002", "case_type": "civil",
        "title": "Ram Prasad v. Shyam Lal",
        "court": "Civil Court, Lucknow", "year": "2020",
        "sections": "Order 37 CPC, Negotiable Instruments Act",
        "outcome": "Decree passed for Rs. 8 lakhs.",
        "text": (
            "Plaintiff filed a summary suit under Order 37 CPC for recovery of Rs. 8 lakhs "
            "advanced as a loan to the defendant. The defendant failed to repay despite repeated "
            "demands and a dishonoured cheque. The court passed a decree in favour of the "
            "plaintiff for Rs. 8 lakhs along with interest at 12% per annum."
        ),
    },
    {
        "id": "cv_003", "case_type": "civil",
        "title": "Meera Devi v. Housing Board of Rajasthan",
        "court": "Rajasthan High Court", "year": "2022",
        "sections": "CPC Section 9, Specific Relief Act",
        "outcome": "Permanent injunction granted.",
        "text": (
            "The plaintiff sought permanent injunction restraining the Housing Board from "
            "demolishing her lawfully constructed residential premises. The court found that "
            "the plaintiff had valid title and possession. A permanent injunction was granted "
            "restraining the defendant from interfering with the plaintiff's peaceful possession."
        ),
    },
    {
        "id": "cv_004", "case_type": "civil",
        "title": "Vijay Transport v. National Insurance Co.",
        "court": "Motor Accident Claims Tribunal, Chennai", "year": "2021",
        "sections": "Motor Vehicles Act Section 166",
        "outcome": "Rs. 15 lakhs compensation to accident victim.",
        "text": (
            "The claimant filed a petition under the Motor Vehicles Act for compensation for "
            "injuries sustained in a road accident caused by the rash and negligent driving of "
            "the respondent's vehicle. The tribunal awarded Rs. 15 lakhs as compensation "
            "considering the nature of injuries, loss of income, and future medical expenses."
        ),
    },
    {
        "id": "cv_005", "case_type": "civil",
        "title": "Suresh Builders v. City Municipal Corporation",
        "court": "Bombay High Court", "year": "2023",
        "sections": "CPC Order 39, Specific Relief Act Section 38",
        "outcome": "Temporary injunction granted against demolition.",
        "text": (
            "The plaintiff builder sought a mandatory injunction directing the municipal "
            "corporation to issue completion certificate and stop demolition proceedings. "
            "The court granted interim relief and directed the municipality to maintain status "
            "quo pending final hearing of the suit for specific performance and injunction."
        ),
    },
    {
        "id": "cv_006", "case_type": "civil",
        "title": "Sunita Rao v. Builder DLF",
        "court": "NCDRC New Delhi", "year": "2022",
        "sections": "Consumer Protection Act 2019 Section 2, Section 35",
        "outcome": "Builder ordered to refund Rs. 45 lakhs with interest.",
        "text": (
            "The complainant booked an apartment with the builder but the builder failed "
            "to deliver possession within the agreed timeline. The National Consumer "
            "Disputes Redressal Commission found deficiency in service and directed the "
            "builder to refund Rs. 45 lakhs with 9 percent interest per annum."
        ),
    },
    {
        "id": "cv_007", "case_type": "civil",
        "title": "Ramesh v. Insurance Company",
        "court": "High Court of Bombay", "year": "2021",
        "sections": "Insurance Act, Consumer Protection Act",
        "outcome": "Insurance claim allowed. Rs. 20 lakhs awarded.",
        "text": (
            "The plaintiff filed suit against the insurance company for wrongful rejection "
            "of his fire insurance claim. The court found that the rejection was arbitrary "
            "and against the policy terms. The insurer was directed to pay Rs. 20 lakhs "
            "as insurance claim with interest and litigation costs."
        ),
    },
    {
        "id": "cv_008", "case_type": "civil",
        "title": "Krishnamurthy v. State Bank of India",
        "court": "Karnataka High Court", "year": "2020",
        "sections": "Banking Ombudsman Scheme, Consumer Protection Act",
        "outcome": "Bank directed to compensate Rs. 5 lakhs for deficient service.",
        "text": (
            "The plaintiff alleged deficiency in banking service after the bank wrongly "
            "debited his account and refused to reverse the erroneous transaction. The "
            "court found negligence on the part of the bank and awarded Rs. 5 lakhs as "
            "compensation for mental agony and financial loss caused."
        ),
    },
    {
        "id": "cv_009", "case_type": "civil",
        "title": "Tenant Cooperative v. Municipality",
        "court": "Delhi High Court", "year": "2023",
        "sections": "Specific Relief Act Section 39, Municipal Law",
        "outcome": "Mandatory injunction granted to restore water supply.",
        "text": (
            "The residential cooperative sought mandatory injunction to restore water "
            "supply wrongly disconnected by the municipality. The court found that "
            "disconnection without notice was illegal and granted mandatory injunction "
            "directing the municipality to restore supply within 48 hours."
        ),
    },
    {
        "id": "cv_010", "case_type": "civil",
        "title": "Doctor v. Hospital Administration",
        "court": "Madras High Court", "year": "2022",
        "sections": "CPC Section 9, Tort Law",
        "outcome": "Defamation suit decreed. Rs. 10 lakhs awarded.",
        "text": (
            "The doctor filed a civil suit for defamation against the hospital "
            "administration for publishing false statements about his professional "
            "conduct. The court found the statements to be defamatory and without "
            "basis and awarded Rs. 10 lakhs as damages for loss of reputation."
        ),
    },
    # ── CONTRACT DISPUTE ──────────────────────────────────────────────────────
    {
        "id": "co_001", "case_type": "contract_dispute",
        "title": "ABC Constructions v. XYZ Developers",
        "court": "Delhi High Court", "year": "2023",
        "sections": "Indian Contract Act Section 73, Section 74",
        "outcome": "Rs. 40 lakhs decreed with 18% interest.",
        "text": (
            "The plaintiff ABC Constructions completed interior fit-out work as per contract "
            "but the defendant XYZ Developers failed to pay two instalments totalling Rs. 40 "
            "lakhs. The court held that the defendant was in breach of contract and awarded "
            "the outstanding amount with interest at 18% per annum under Sections 73 and 74 "
            "of the Indian Contract Act, 1872."
        ),
    },
    {
        "id": "co_002", "case_type": "contract_dispute",
        "title": "Infosys Ltd. v. DataCorp Solutions",
        "court": "Bangalore Civil Court", "year": "2022",
        "sections": "Indian Contract Act Section 73, Arbitration Act",
        "outcome": "Arbitration award upheld. Rs. 1.2 crore damages.",
        "text": (
            "The dispute arose from a software development contract where the vendor failed "
            "to deliver milestones within agreed timelines. The client terminated the contract "
            "and invoked the arbitration clause. The arbitrator awarded Rs. 1.2 crores as "
            "damages for breach of contract including refund of advance and loss of profits."
        ),
    },
    {
        "id": "co_003", "case_type": "contract_dispute",
        "title": "Sharma Textiles v. Cotton Suppliers Ltd.",
        "court": "Gujarat High Court", "year": "2020",
        "sections": "Sale of Goods Act, Indian Contract Act Section 73",
        "outcome": "Supplier held liable for defective goods.",
        "text": (
            "The plaintiff purchased raw cotton from the defendant under a supply agreement. "
            "The goods delivered were of inferior quality causing losses in manufacturing. "
            "The court held the defendant in breach of the implied condition of merchantable "
            "quality under the Sale of Goods Act and awarded compensation under Section 73 "
            "of the Indian Contract Act."
        ),
    },
    {
        "id": "co_004", "case_type": "contract_dispute",
        "title": "Hotel Grand v. Event Management Co.",
        "court": "Madras High Court", "year": "2021",
        "sections": "Indian Contract Act Section 56, Section 73",
        "outcome": "Force majeure upheld. Contract discharged.",
        "text": (
            "The hotel sought to invoke the force majeure clause due to COVID-19 lockdown "
            "restrictions preventing performance of a large event contract. The court held "
            "that COVID-19 constituted a force majeure event under Section 56 of the Indian "
            "Contract Act making performance impossible and discharged both parties from "
            "their contractual obligations."
        ),
    },
    {
        "id": "co_005", "case_type": "contract_dispute",
        "title": "MNC Bank v. Reliable Industries",
        "court": "Bombay High Court", "year": "2022",
        "sections": "Indian Contract Act Section 74, Arbitration Act",
        "outcome": "Penalty clause enforced. Rs. 50 lakhs awarded.",
        "text": (
            "The bank sued for enforcement of the penalty clause in a loan agreement after "
            "the borrower defaulted on repayment. The borrower challenged the penalty as "
            "unreasonable. The court upheld the penalty clause under Section 74 of the Indian "
            "Contract Act finding it was a genuine pre-estimate of loss and awarded Rs. 50 "
            "lakhs as stipulated damages."
        ),
    },
    {
        "id": "co_006", "case_type": "contract_dispute",
        "title": "Pharma Distributor v. Medicine Manufacturer",
        "court": "Delhi High Court", "year": "2020",
        "sections": "Indian Contract Act Section 73, Distribution Agreement",
        "outcome": "Distributor awarded Rs. 30 lakhs for wrongful termination.",
        "text": (
            "The plaintiff distributor had an exclusive distribution agreement with the "
            "defendant manufacturer. The manufacturer wrongfully terminated the agreement "
            "without serving the required notice period. The court held this as breach "
            "of contract and awarded Rs. 30 lakhs as damages for lost profits."
        ),
    },
    {
        "id": "co_007", "case_type": "contract_dispute",
        "title": "Construction Company v. Government PWD",
        "court": "High Court of Rajasthan", "year": "2022",
        "sections": "Arbitration and Conciliation Act Section 34",
        "outcome": "Arbitration award of Rs. 2 crores upheld.",
        "text": (
            "The construction company filed a petition challenging the government's "
            "rejection of arbitration award in a road construction contract dispute. "
            "The contractor had claimed extra costs due to design changes by the "
            "government. The High Court upheld the arbitration award of Rs. 2 crores."
        ),
    },
    {
        "id": "co_008", "case_type": "contract_dispute",
        "title": "Franchisee v. Fast Food Chain",
        "court": "Bombay High Court", "year": "2021",
        "sections": "Indian Contract Act Section 27, Franchise Agreement",
        "outcome": "Non-compete clause declared void. Injunction refused.",
        "text": (
            "The fast food chain sought enforcement of a non-compete clause in the "
            "franchise agreement restricting the franchisee from operating any food "
            "business for 5 years after termination. The court held the clause was "
            "void under Section 27 of the Indian Contract Act as unreasonable restraint."
        ),
    },
    {
        "id": "co_009", "case_type": "contract_dispute",
        "title": "Real Estate Developer v. Land Owner",
        "court": "Karnataka High Court", "year": "2023",
        "sections": "Specific Relief Act Section 10, Indian Contract Act",
        "outcome": "Specific performance of development agreement ordered.",
        "text": (
            "The developer filed suit for specific performance of a joint development "
            "agreement after the landowner refused to hand over possession for "
            "construction. The court found valid agreement existed and ordered specific "
            "performance directing the landowner to hand over the property for development."
        ),
    },
    {
        "id": "co_010", "case_type": "contract_dispute",
        "title": "Insurance Broker v. Insurance Company",
        "court": "Delhi High Court", "year": "2022",
        "sections": "Indian Contract Act Section 73, Agency Law",
        "outcome": "Broker awarded unpaid commission of Rs. 15 lakhs.",
        "text": (
            "The insurance broker filed suit for recovery of unpaid commission from "
            "the insurance company for policies procured through his agency. The "
            "company denied the commission claiming breach of agency agreement. "
            "The court found no breach and awarded the outstanding commission of Rs. 15 lakhs."
        ),
    },
    # ── FAMILY LAW ────────────────────────────────────────────────────────────
    {
        "id": "fl_001", "case_type": "family_law",
        "title": "Priya Mehta v. Rakesh Mehta",
        "court": "Family Court, Mumbai", "year": "2022",
        "sections": "Hindu Marriage Act Section 13, Section 25",
        "outcome": "Divorce granted. Rs. 30,000/month alimony.",
        "text": (
            "The wife filed for divorce on grounds of cruelty and desertion under Section 13 "
            "of the Hindu Marriage Act. The husband had abandoned the matrimonial home for "
            "over two years without reasonable cause. The Family Court granted divorce and "
            "awarded permanent alimony of Rs. 30,000 per month under Section 25 of the Act."
        ),
    },
    {
        "id": "fl_002", "case_type": "family_law",
        "title": "Sunita Devi v. Mahesh Kumar",
        "court": "Delhi High Court", "year": "2021",
        "sections": "CrPC Section 125, Domestic Violence Act",
        "outcome": "Rs. 20,000/month maintenance ordered.",
        "text": (
            "The wife filed an application under Section 125 CrPC for maintenance after being "
            "thrown out of the matrimonial home. She also filed a complaint under the Domestic "
            "Violence Act alleging physical abuse. The court awarded Rs. 20,000 per month as "
            "interim maintenance and issued a protection order in her favour."
        ),
    },
    {
        "id": "fl_003", "case_type": "family_law",
        "title": "Arun Sharma v. Kavita Sharma",
        "court": "Family Court, Chandigarh", "year": "2023",
        "sections": "Hindu Marriage Act Section 26, Guardian Act",
        "outcome": "Joint custody awarded to both parents.",
        "text": (
            "Both parents claimed custody of their 8-year-old child after separation. The "
            "Family Court conducted a welfare assessment and interviewed the child. Considering "
            "the best interests of the child, the court awarded joint custody with the child "
            "living with the mother during school term and with the father during vacations."
        ),
    },
    {
        "id": "fl_004", "case_type": "family_law",
        "title": "Rekha v. Vinod Kumar",
        "court": "High Court of Andhra Pradesh", "year": "2020",
        "sections": "IPC Section 498A, Dowry Prohibition Act",
        "outcome": "Husband and in-laws convicted for dowry harassment.",
        "text": (
            "The wife filed complaint under Section 498A IPC and Dowry Prohibition Act against "
            "her husband and in-laws for demanding dowry and subjecting her to cruelty. The "
            "trial court convicted the accused. The High Court upheld the conviction finding "
            "sufficient evidence of harassment for dowry and cruelty to the wife."
        ),
    },
    {
        "id": "fl_005", "case_type": "family_law",
        "title": "Nirmala v. Suresh Patel",
        "court": "Gujarat Family Court", "year": "2022",
        "sections": "Hindu Adoption and Maintenance Act Section 18",
        "outcome": "Rs. 15,000/month maintenance to wife and child.",
        "text": (
            "The wife sought maintenance for herself and the minor child under the Hindu "
            "Adoptions and Maintenance Act. The husband claimed financial inability. The court "
            "examined the husband's income and assets and awarded Rs. 15,000 per month to "
            "the wife and Rs. 10,000 per month for the child's education and maintenance."
        ),
    },
    {
        "id": "fl_006", "case_type": "family_law",
        "title": "Suresh v. Asha Kumar",
        "court": "Kerala High Court", "year": "2021",
        "sections": "Hindu Marriage Act Section 13B, Section 14",
        "outcome": "Mutual consent divorce granted after cooling off period waived.",
        "text": (
            "Both parties filed a joint petition for divorce by mutual consent under "
            "Section 13B of the Hindu Marriage Act. The parties had been living "
            "separately for over 3 years. The Family Court waived the 6-month cooling "
            "off period and granted divorce on mutual consent with agreed settlement."
        ),
    },
    {
        "id": "fl_007", "case_type": "family_law",
        "title": "NRI Husband v. Wife",
        "court": "Supreme Court of India", "year": "2022",
        "sections": "Hindu Marriage Act, Private International Law",
        "outcome": "Foreign divorce decree not recognized. Indian proceedings continue.",
        "text": (
            "The NRI husband obtained a divorce decree from a US court ex-parte without "
            "serving proper notice to the wife in India. The Supreme Court refused to "
            "recognize the foreign divorce decree as it violated principles of natural "
            "justice. The Indian matrimonial proceedings were directed to continue."
        ),
    },
    {
        "id": "fl_008", "case_type": "family_law",
        "title": "Grandmother v. Parents",
        "court": "Delhi High Court", "year": "2023",
        "sections": "Guardian and Wards Act Section 17, Section 25",
        "outcome": "Visitation rights granted to grandparents.",
        "text": (
            "The paternal grandparents sought visitation rights with their grandchild "
            "after the parents separated and the mother denied access. The court held "
            "that grandparents have a right to maintain relationship with grandchildren "
            "and granted structured visitation rights twice a month."
        ),
    },
    {
        "id": "fl_009", "case_type": "family_law",
        "title": "Second Wife v. Husband",
        "court": "Allahabad High Court", "year": "2020",
        "sections": "Muslim Personal Law, CrPC Section 125",
        "outcome": "Maintenance awarded to divorced Muslim wife.",
        "text": (
            "The petitioner divorced Muslim wife filed for maintenance under Section "
            "125 CrPC after being abandoned without proper mehr and maintenance. "
            "The court following the Shah Bano principle awarded Rs. 10000 per month "
            "as maintenance during the iddat period and beyond."
        ),
    },
    {
        "id": "fl_010", "case_type": "family_law",
        "title": "Minor v. Biological Parents",
        "court": "Gujarat High Court", "year": "2022",
        "sections": "Juvenile Justice Act Section 2, Adoption Regulations",
        "outcome": "Adoption by foster parents confirmed. Biological claim rejected.",
        "text": (
            "Biological parents sought return of child given up for adoption claiming "
            "financial circumstances had improved. The court held that the adoption "
            "had been completed legally under the Juvenile Justice Act and the "
            "interests of the child demanded continuity with adoptive parents."
        ),
    },
    # ── PROPERTY ──────────────────────────────────────────────────────────────
    {
        "id": "pr_001", "case_type": "property",
        "title": "Jagdish Singh v. Harpal Singh",
        "court": "Punjab and Haryana High Court", "year": "2021",
        "sections": "Transfer of Property Act Section 54, Limitation Act",
        "outcome": "Plaintiff's title upheld. Adverse possession rejected.",
        "text": (
            "The plaintiff claimed ownership of agricultural land based on a registered sale "
            "deed of 1995. The defendant claimed adverse possession for over 20 years. The "
            "court examined the revenue records and possession evidence and upheld the "
            "plaintiff's title, rejecting the claim of adverse possession as not established "
            "by continuous, peaceful and open possession."
        ),
    },
    {
        "id": "pr_002", "case_type": "property",
        "title": "Ramesh Landlord v. Suresh Tenant",
        "court": "Rent Control Tribunal, Delhi", "year": "2022",
        "sections": "Delhi Rent Control Act, Transfer of Property Act Section 105",
        "outcome": "Eviction order passed for non-payment of rent.",
        "text": (
            "The landlord filed an eviction petition against the tenant for non-payment of "
            "rent for 15 months and creating sub-tenancy without permission. The Rent Control "
            "Tribunal found both grounds established and passed an eviction order directing "
            "the tenant to vacate within 3 months with payment of arrears."
        ),
    },
    {
        "id": "pr_003", "case_type": "property",
        "title": "Sharma Family v. State of Maharashtra",
        "court": "Bombay High Court", "year": "2020",
        "sections": "Land Acquisition Act Section 23, Section 28A",
        "outcome": "Enhanced compensation of Rs. 2.5 crores awarded.",
        "text": (
            "The petitioner challenged land acquisition by the state government claiming the "
            "compensation of Rs. 80 lakhs was grossly inadequate for prime agricultural land. "
            "The High Court examined market value evidence and comparable sales and enhanced "
            "the compensation to Rs. 2.5 crores plus solatium under the Land Acquisition Act."
        ),
    },
    {
        "id": "pr_004", "case_type": "property",
        "title": "Gopal v. Ramji Lal",
        "court": "Allahabad High Court", "year": "2021",
        "sections": "Hindu Succession Act Section 8, CPC Order 20 Rule 18",
        "outcome": "Partition decree passed. Equal shares to all legal heirs.",
        "text": (
            "The plaintiff sought partition of ancestral property comprising a house and "
            "agricultural land following the death of the father. The defendant co-heirs "
            "refused to agree on partition. The court passed a preliminary partition decree "
            "directing equal division among all four legal heirs under the Hindu Succession Act."
        ),
    },
    {
        "id": "pr_005", "case_type": "property",
        "title": "Anand v. Municipal Corporation of Hyderabad",
        "court": "Telangana High Court", "year": "2023",
        "sections": "Article 226 Constitution, Municipal Corporation Act",
        "outcome": "Demolition notice quashed. Corporation directed to regularise.",
        "text": (
            "The petitioner challenged a demolition notice issued by the municipal corporation "
            "for his residential building constructed with valid permissions. The High Court "
            "found that the notice was issued without following due procedure and quashed it, "
            "directing the corporation to decide the regularisation application within 3 months."
        ),
    },
    {
        "id": "pr_006", "case_type": "property",
        "title": "Builders Association v. RERA Authority",
        "court": "Bombay High Court", "year": "2022",
        "sections": "RERA Act Section 31, Section 40",
        "outcome": "RERA order upheld. Builder penalised Rs. 50 lakhs.",
        "text": (
            "Homebuyers filed complaint under RERA against the builder for delayed "
            "delivery of flats beyond the registered date. The RERA authority imposed "
            "a penalty of Rs. 50 lakhs and directed interest payment to buyers. "
            "The High Court upheld the RERA order finding no ground for interference."
        ),
    },
    {
        "id": "pr_007", "case_type": "property",
        "title": "Encroacher v. Municipal Board",
        "court": "Allahabad High Court", "year": "2021",
        "sections": "UP Urban Planning Act, Article 226 Constitution",
        "outcome": "Encroachment removal order upheld.",
        "text": (
            "The petitioner challenged a notice for removal of encroachment on "
            "government land claiming long possession. The court found that the "
            "petitioner had no title to the land and was an encroacher. The "
            "demolition notice was upheld and petitioner was directed to vacate."
        ),
    },
    {
        "id": "pr_008", "case_type": "property",
        "title": "Co-owner v. Co-owner",
        "court": "Madras High Court", "year": "2020",
        "sections": "Transfer of Property Act Section 44, CPC Order 20 Rule 18",
        "outcome": "Partition by metes and bounds ordered.",
        "text": (
            "Two co-owners of a commercial building disputed the use and rental income "
            "from the property. The court ordered partition of the property by metes "
            "and bounds and directed a commissioner to survey and divide the property "
            "into equal shares with an account of past rental income."
        ),
    },
    {
        "id": "pr_009", "case_type": "property",
        "title": "Mortgagor v. Bank",
        "court": "Delhi High Court", "year": "2023",
        "sections": "SARFAESI Act Section 13, Section 17",
        "outcome": "SARFAESI proceedings stayed. DRT directed to hear matter.",
        "text": (
            "The borrower challenged bank action under SARFAESI Act for taking "
            "symbolic possession of mortgaged property after loan default. The "
            "borrower claimed the outstanding amount was disputed. The court stayed "
            "the proceedings and directed the Debt Recovery Tribunal to hear the matter."
        ),
    },
    {
        "id": "pr_010", "case_type": "property",
        "title": "Temple Trust v. Land Encroacher",
        "court": "Karnataka High Court", "year": "2022",
        "sections": "Hindu Religious Endowments Act, Transfer of Property Act",
        "outcome": "Temple land recovered. Encroacher evicted.",
        "text": (
            "The temple trust filed suit to recover land belonging to the temple "
            "that had been encroached upon by the defendant for over 15 years. "
            "The court held that temple property cannot be acquired by adverse "
            "possession and directed eviction of the encroacher with payment of "
            "mesne profits."
        ),
    },
    # ── CONSTITUTIONAL ────────────────────────────────────────────────────────
    {
        "id": "cn_001", "case_type": "constitutional",
        "title": "Citizens Forum v. State of Bihar",
        "court": "Patna High Court", "year": "2022",
        "sections": "Article 14, Article 21, Article 226 Constitution",
        "outcome": "Government order quashed as arbitrary.",
        "text": (
            "The petitioner challenged a government order arbitrarily transferring public "
            "servants in violation of established transfer policy. The High Court held that "
            "the order violated Article 14 of the Constitution as it was discriminatory and "
            "without rational basis. The order was quashed and directions issued to follow "
            "the transfer policy transparently."
        ),
    },
    {
        "id": "cn_002", "case_type": "constitutional",
        "title": "Advocate Ravi v. State of Tamil Nadu",
        "court": "Madras High Court", "year": "2021",
        "sections": "Article 32, Article 22, Habeas Corpus",
        "outcome": "Detenu released. Preventive detention order quashed.",
        "text": (
            "A habeas corpus petition was filed challenging the preventive detention of the "
            "petitioner under the National Security Act. The court found that the detention "
            "order was passed without proper application of mind and the detenu was not given "
            "adequate opportunity to make a representation. The detention order was quashed "
            "and the petitioner was directed to be released immediately."
        ),
    },
    {
        "id": "cn_003", "case_type": "constitutional",
        "title": "Students Union v. University of Rajasthan",
        "court": "Rajasthan High Court", "year": "2023",
        "sections": "Article 14, Article 19, Article 226 Constitution",
        "outcome": "University circular struck down as unconstitutional.",
        "text": (
            "The students' union challenged a university circular imposing unreasonable "
            "restrictions on student elections as violative of Articles 14 and 19 of the "
            "Constitution. The High Court held that the circular was arbitrary, disproportionate "
            "and violated the right to equality. The circular was struck down and the university "
            "was directed to conduct elections as per established norms."
        ),
    },
    {
        "id": "cn_004", "case_type": "constitutional",
        "title": "Teachers Association v. State of UP",
        "court": "Allahabad High Court", "year": "2020",
        "sections": "Article 311, Article 16, Service Law",
        "outcome": "Dismissal set aside. Reinstatement with back wages.",
        "text": (
            "The petitioner challenged his dismissal from government service without following "
            "the procedure under Article 311 of the Constitution. The Inquiry Officer had not "
            "given the employee adequate opportunity to cross-examine witnesses. The court set "
            "aside the dismissal order and directed reinstatement with full back wages."
        ),
    },
    {
        "id": "cn_005", "case_type": "constitutional",
        "title": "Environmental NGO v. Union of India",
        "court": "Supreme Court of India", "year": "2022",
        "sections": "Article 21, Article 48A, Environment Protection Act",
        "outcome": "Directions issued for pollution control.",
        "text": (
            "A PIL was filed challenging industrial pollution in the Yamuna river corridor "
            "as a violation of the right to clean environment under Article 21. The Supreme "
            "Court directed the Central and State governments to take immediate steps to close "
            "polluting industries and implement the river action plan within 6 months."
        ),
    },
    {
        "id": "cn_006", "case_type": "constitutional",
        "title": "Journalist v. State of UP",
        "court": "Allahabad High Court", "year": "2023",
        "sections": "Article 19(1)(a), IPC Section 124A",
        "outcome": "Sedition FIR quashed. Article 19 upheld.",
        "text": (
            "A journalist challenged the FIR registered against him for sedition "
            "under Section 124A IPC for publishing an article critical of government "
            "policies. The High Court following the Supreme Court guidelines on sedition "
            "quashed the FIR finding no incitement to violence and upheld freedom of press."
        ),
    },
    {
        "id": "cn_007", "case_type": "constitutional",
        "title": "SC/ST Employee v. State Government",
        "court": "Supreme Court of India", "year": "2021",
        "sections": "Article 16(4), Article 335, SC/ST Reservation Policy",
        "outcome": "Reservation in promotion upheld as constitutional.",
        "text": (
            "The state government's policy of reservation in promotion for SC/ST "
            "employees was challenged as unconstitutional. The Supreme Court upheld "
            "the reservation policy finding that quantifiable data on backwardness "
            "and inadequacy of representation had been collected and the policy "
            "was constitutionally valid under Article 16(4)."
        ),
    },
    {
        "id": "cn_008", "case_type": "constitutional",
        "title": "Undertrial Prisoners v. State of Bihar",
        "court": "Patna High Court", "year": "2022",
        "sections": "Article 21, CrPC Section 436A, Prison Manual",
        "outcome": "Undertrial prisoners ordered to be released on bail.",
        "text": (
            "A PIL was filed highlighting plight of undertrial prisoners who had "
            "spent more than half the maximum sentence in jail without trial. The "
            "court found violation of Article 21 right to speedy trial and directed "
            "the state to release all eligible undertrial prisoners under Section 436A CrPC."
        ),
    },
    {
        "id": "cn_009", "case_type": "constitutional",
        "title": "Women Officers v. Union of India",
        "court": "Supreme Court of India", "year": "2020",
        "sections": "Article 14, Article 16, Army Act",
        "outcome": "Permanent commission granted to women army officers.",
        "text": (
            "Women Short Service Commission officers challenged the policy denying "
            "them permanent commission in the Army as discriminatory under Articles "
            "14 and 16. The Supreme Court held the policy was unconstitutional and "
            "directed grant of permanent commission to all eligible women officers."
        ),
    },
    {
        "id": "cn_010", "case_type": "constitutional",
        "title": "Internet Freedom Foundation v. Union of India",
        "court": "Supreme Court of India", "year": "2023",
        "sections": "Article 19(1)(a), Article 19(1)(g), Telegraph Act Section 5",
        "outcome": "Internet shutdown guidelines issued. Indefinite shutdown held illegal.",
        "text": (
            "A PIL challenged the practice of imposing indefinite internet shutdowns "
            "in Jammu and Kashmir as violating rights under Article 19. The Supreme "
            "Court held that internet access is a fundamental right and indefinite "
            "shutdowns are unconstitutional. Detailed guidelines for review of shutdown "
            "orders were issued."
        ),
    },
    # ── INTELLECTUAL PROPERTY ─────────────────────────────────────────────────
    {
        "id": "ip_001", "case_type": "intellectual_property",
        "title": "Tech Innovations v. Copy Cat Solutions",
        "court": "Delhi High Court", "year": "2022",
        "sections": "Patents Act Section 48, Section 104",
        "outcome": "Patent infringement proven. Permanent injunction granted.",
        "text": (
            "The plaintiff held a registered patent for a software algorithm. The defendant "
            "used the patented process in their commercial product without licence. The court "
            "found clear infringement of the patent rights under Section 48 of the Patents "
            "Act and granted a permanent injunction along with damages of Rs. 75 lakhs."
        ),
    },
    {
        "id": "ip_002", "case_type": "intellectual_property",
        "title": "Cafe Coffee Day v. Cafe Coffee House",
        "court": "Karnataka High Court", "year": "2021",
        "sections": "Trade Marks Act Section 29, Section 135",
        "outcome": "Passing off established. Mark cancelled.",
        "text": (
            "The plaintiff restaurant chain sought cancellation of the defendant's registered "
            "trademark which was deceptively similar to their established mark causing market "
            "confusion. The court held that passing off was established due to phonetic and "
            "visual similarity and directed cancellation of the defendant's mark along with "
            "damages of Rs. 20 lakhs."
        ),
    },
    {
        "id": "ip_003", "case_type": "intellectual_property",
        "title": "Film Producer v. OTT Platform",
        "court": "Bombay High Court", "year": "2023",
        "sections": "Copyright Act Section 51, Section 55",
        "outcome": "Copyright infringement. Rs. 1 crore damages awarded.",
        "text": (
            "The film producer sued an OTT platform for streaming their copyrighted film "
            "without obtaining a licence. The defendant failed to prove a valid licence "
            "agreement. The court awarded damages of Rs. 1 crore under Section 55 of the "
            "Copyright Act and granted a permanent injunction against further streaming."
        ),
    },
    {
        "id": "ip_004", "case_type": "intellectual_property",
        "title": "Pharma Ltd. v. Generic Drugs Co.",
        "court": "Intellectual Property Appellate Board", "year": "2020",
        "sections": "Patents Act Section 84, Section 90",
        "outcome": "Compulsory licence granted at 7% royalty.",
        "text": (
            "The respondent applied for compulsory licence for a patented cancer drug under "
            "Section 84 of the Patents Act on grounds of non-availability and unaffordable "
            "pricing. The IPAB found that the drug was not available to public at reasonably "
            "affordable price and granted a compulsory licence at 7% royalty to make the "
            "drug accessible."
        ),
    },
    {
        "id": "ip_005", "case_type": "intellectual_property",
        "title": "Author v. Publishing House",
        "court": "Delhi High Court", "year": "2021",
        "sections": "Copyright Act Section 14, Section 17, Section 57",
        "outcome": "Moral rights violation. Publisher directed to credit author.",
        "text": (
            "The author sued the publishing house for publishing a mutilated version of the "
            "novel without consent and removing the author's name. The court held that the "
            "publisher violated the author's moral rights under Section 57 of the Copyright "
            "Act. The publisher was directed to restore the original content and properly "
            "credit the author in all future editions."
        ),
    },
    {
        "id": "ip_006", "case_type": "intellectual_property",
        "title": "Software Company v. Ex-Employee",
        "court": "Delhi High Court", "year": "2022",
        "sections": "Copyright Act Section 2(o), Section 51",
        "outcome": "Source code copyright infringement established. Injunction granted.",
        "text": (
            "The plaintiff software company sued its former employee for copying "
            "proprietary source code and using it to build a competing product. "
            "The court found that software source code is protected as literary work "
            "under the Copyright Act and granted permanent injunction against "
            "the defendant's competing product."
        ),
    },
    {
        "id": "ip_007", "case_type": "intellectual_property",
        "title": "Music Composer v. Film Producer",
        "court": "Bombay High Court", "year": "2021",
        "sections": "Copyright Act Section 13, Section 57, Performer Rights",
        "outcome": "Royalties awarded to music composer. Rs. 50 lakhs damages.",
        "text": (
            "The music composer sued the film producer for using his compositions "
            "in a film sequel without consent and without paying royalties. The "
            "court held that composer retains copyright in musical works and "
            "awarded Rs. 50 lakhs as damages along with future royalty rights."
        ),
    },
    {
        "id": "ip_008", "case_type": "intellectual_property",
        "title": "Seed Company v. Farmer",
        "court": "High Court of Andhra Pradesh", "year": "2020",
        "sections": "Protection of Plant Varieties and Farmers Rights Act 2001",
        "outcome": "Farmer exemption upheld. Seed company suit dismissed.",
        "text": (
            "A seed company sued a farmer for saving and resowing patented hybrid "
            "seeds claiming infringement of plant variety rights. The court upheld "
            "the farmer exemption under the Protection of Plant Varieties Act which "
            "permits farmers to save seeds for personal use and dismissed the suit."
        ),
    },
    {
        "id": "ip_009", "case_type": "intellectual_property",
        "title": "Luxury Brand v. Street Vendor",
        "court": "Delhi High Court", "year": "2023",
        "sections": "Trade Marks Act Section 29, Section 102",
        "outcome": "Counterfeiting established. Goods seized and destroyed.",
        "text": (
            "The luxury brand filed an anti-counterfeiting suit against vendors "
            "selling fake goods bearing its trademark at street markets. The court "
            "found clear trademark counterfeiting under Section 102 and directed "
            "seizure and destruction of all counterfeit goods and imposed damages."
        ),
    },
    {
        "id": "ip_010", "case_type": "intellectual_property",
        "title": "Pharmaceutical Company v. IPAB",
        "court": "Madras High Court", "year": "2022",
        "sections": "Patents Act Section 3(d), Section 25",
        "outcome": "Patent refused under Section 3(d). Evergreening rejected.",
        "text": (
            "A pharmaceutical company challenged the rejection of its patent "
            "application for a modified form of a known drug. The court upheld "
            "rejection under Section 3(d) of the Patents Act finding that the "
            "modified form did not show significant enhancement in efficacy "
            "preventing evergreening of pharmaceutical patents."
        ),
    },
    # ── LABOUR ────────────────────────────────────────────────────────────────
    {
        "id": "lb_001", "case_type": "labour",
        "title": "Ram Kishore v. Steel Authority of India",
        "court": "Labour Court, Delhi", "year": "2021",
        "sections": "Industrial Disputes Act Section 25F, Section 11A",
        "outcome": "Wrongful dismissal. Reinstatement with back wages.",
        "text": (
            "The workman was dismissed from service without proper domestic enquiry. The "
            "Labour Court found that the dismissal was in violation of the principles of "
            "natural justice as the worker was not given adequate opportunity to present his "
            "defence. The court ordered reinstatement with full back wages under Section 11A "
            "of the Industrial Disputes Act."
        ),
    },
    {
        "id": "lb_002", "case_type": "labour",
        "title": "Workers Union v. Textile Mills Ltd.",
        "court": "Industrial Tribunal, Ahmedabad", "year": "2022",
        "sections": "Industrial Disputes Act Section 9A, Section 25N",
        "outcome": "Retrenchment declared illegal. Workers reinstated.",
        "text": (
            "The trade union challenged the retrenchment of 300 workers by the textile mill "
            "claiming it violated Section 25N of the Industrial Disputes Act which requires "
            "prior government permission for establishments with over 100 workers. The "
            "tribunal found the retrenchment illegal and ordered reinstatement with continuity "
            "of service and back wages."
        ),
    },
    {
        "id": "lb_003", "case_type": "labour",
        "title": "Contract Workers v. BHEL",
        "court": "High Court of Telangana", "year": "2020",
        "sections": "Contract Labour Act Section 10, Section 21",
        "outcome": "Principal employer directed to absorb contract workers.",
        "text": (
            "The contract workers filed a writ petition seeking regularisation of their "
            "services after working continuously for over 10 years through a contractor. "
            "The court found that the work was perennial and the contract arrangement was "
            "sham. BHEL as principal employer was directed to absorb the workers as regular "
            "employees with all applicable service benefits."
        ),
    },
    {
        "id": "lb_004", "case_type": "labour",
        "title": "Employees Association v. IT Company",
        "court": "Labour Court, Bangalore", "year": "2023",
        "sections": "Payment of Wages Act Section 7, Section 15",
        "outcome": "Illegal deductions recovered. Penalty imposed.",
        "text": (
            "The employees association filed a complaint under the Payment of Wages Act "
            "alleging that the employer made illegal deductions from salaries including "
            "deductions towards bond amount and training costs in violation of Section 7. "
            "The authority ordered recovery of all deductions and imposed a penalty of "
            "Rs. 50,000 on the employer."
        ),
    },
    {
        "id": "lb_005", "case_type": "labour",
        "title": "Security Guards Union v. Mall Management",
        "court": "Minimum Wages Authority, Mumbai", "year": "2022",
        "sections": "Minimum Wages Act Section 12, Section 20",
        "outcome": "Underpayment proven. Rs. 12 lakhs recovered.",
        "text": (
            "Security guards filed a claim under the Minimum Wages Act alleging wages below "
            "the notified statutory minimum. The employer paid Rs. 8,000 per month against "
            "the notified minimum of Rs. 12,500. The authority found underpayment proven "
            "and ordered recovery of Rs. 12 lakhs in wage arrears for 50 workers."
        ),
    },
    {
        "id": "lb_006", "case_type": "labour",
        "title": "Domestic Workers Union v. Employer",
        "court": "Delhi High Court", "year": "2022",
        "sections": "Unorganised Workers Social Security Act 2008",
        "outcome": "Domestic workers entitled to social security benefits.",
        "text": (
            "The union filed a writ petition seeking social security benefits for "
            "domestic workers under the Unorganised Workers Social Security Act. "
            "The court held that domestic workers are entitled to registration and "
            "social security benefits and directed the state to implement the scheme "
            "within 3 months."
        ),
    },
    {
        "id": "lb_007", "case_type": "labour",
        "title": "Gig Worker v. Food Delivery Platform",
        "court": "Bombay High Court", "year": "2023",
        "sections": "Industrial Disputes Act Section 2(s), Contract Labour Act",
        "outcome": "Gig workers declared workmen. Platform directed to provide benefits.",
        "text": (
            "Delivery partners of a food aggregator platform filed a writ claiming "
            "they are workmen under the Industrial Disputes Act and entitled to "
            "employment benefits. The court held that the control exercised by the "
            "platform established employer-employee relationship and directed it to "
            "provide ESI and PF benefits to all delivery partners."
        ),
    },
    {
        "id": "lb_008", "case_type": "labour",
        "title": "Terminated Manager v. MNC",
        "court": "Karnataka High Court", "year": "2021",
        "sections": "Industrial Employment Standing Orders Act, Natural Justice",
        "outcome": "Termination set aside for non-compliance with standing orders.",
        "text": (
            "A senior manager was terminated from an MNC for alleged performance "
            "issues without following the domestic enquiry procedure prescribed "
            "under the Industrial Employment Standing Orders Act. The court set "
            "aside the termination order as it violated principles of natural justice "
            "and the certified standing orders of the establishment."
        ),
    },
    {
        "id": "lb_009", "case_type": "labour",
        "title": "Coal Miners Union v. Coal India",
        "court": "Jharkhand High Court", "year": "2022",
        "sections": "Mines Act 1952, Industrial Disputes Act",
        "outcome": "Safety violations found. Mine closed temporarily.",
        "text": (
            "The trade union filed a petition highlighting safety violations in "
            "the coal mine leading to accidents and worker deaths. The court found "
            "multiple violations of the Mines Act 1952 and directed immediate closure "
            "of the mine pending safety audit and directed payment of compensation "
            "to families of deceased workers."
        ),
    },
    {
        "id": "lb_010", "case_type": "labour",
        "title": "Pension Fund Members v. EPFO",
        "court": "Supreme Court of India", "year": "2022",
        "sections": "Employees Provident Fund Act Section 6A, Pension Scheme",
        "outcome": "Higher pension on actual salary allowed for pre-2014 employees.",
        "text": (
            "Employees who had opted for higher pension contribution on actual "
            "salary challenged EPFO rejection of their pension revision applications. "
            "The Supreme Court upheld their right to higher pension and directed EPFO "
            "to allow employees who had made joint options before 2014 to receive "
            "pension calculated on actual salary."
        ),
    },
]


def main():
    from backend.pipeline.case_retriever import CaseRetriever

    retriever = CaseRetriever(db_path="./case_database")

    # Build documents in the format CaseRetriever expects
    docs = []
    for c in CASES:
        full_text = (
            f"{c['title']} | {c['court']} {c['year']} | "
            f"Sections: {c['sections']} | Outcome: {c['outcome']} | {c['text']}"
        )
        docs.append({
            "id":        c["id"],
            "text":      full_text,
            "case_type": c["case_type"],
            "title":     c["title"],
            "court":     c["court"],
            "year":      c["year"],
            "sections":  c["sections"],
            "outcome":   c["outcome"],
        })

    retriever.index_cases(docs)
    print(f"✅ Indexed {len(docs)} cases into ChromaDB")
    print(f"   (10 per class × 8 classes = {len(docs)} total)\n")

    # Quick test
    test = "accused charged under Section 302 IPC for murder FIR filed"
    results = retriever.find_similar(test, n=3)
    print("Test query: murder / Section 302 IPC")
    print("Top 3 similar cases:")
    for r in results:
        print(f"  [{r.get('case_type','?')}] {r.get('title','?')} — {r.get('court','?')} {r.get('year','?')}")


if __name__ == "__main__":
    main()
