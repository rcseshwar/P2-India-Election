"""
Election data tools providing structured information about India's election system.
These tools are used by ADK agents to provide accurate, factual responses.
"""


def get_election_structure(level: str) -> dict:
    """Get the structure of India's election system at a specific level.

    Args:
        level: The government level - 'national', 'state', or 'local'

    Returns:
        Dictionary containing election structure details for the specified level.
    """
    structures = {
        "national": {
            "level": "National (Central Government)",
            "legislature": "Parliament of India (Sansad)",
            "houses": [
                {
                    "name": "Lok Sabha (House of the People)",
                    "total_seats": 543,
                    "election_type": "Direct election by citizens",
                    "term": "5 years",
                    "eligibility": "Indian citizen, 25+ years old",
                    "voting_method": "First-Past-The-Post (FPTP)",
                    "constituencies": "Single-member constituencies based on population",
                },
                {
                    "name": "Rajya Sabha (Council of States)",
                    "total_seats": 245,
                    "election_type": "Indirect election by state legislators",
                    "term": "6 years (1/3 retire every 2 years)",
                    "eligibility": "Indian citizen, 30+ years old",
                    "voting_method": "Single Transferable Vote (STV)",
                    "nominated": "12 members nominated by President",
                },
            ],
            "head_of_state": "President (elected by Electoral College)",
            "head_of_government": "Prime Minister (leader of majority in Lok Sabha)",
            "conducting_body": "Election Commission of India (ECI)",
        },
        "state": {
            "level": "State Government",
            "legislature": "State Legislature (Vidhan Sabha / Vidhan Parishad)",
            "houses": [
                {
                    "name": "Vidhan Sabha (Legislative Assembly)",
                    "election_type": "Direct election by citizens",
                    "term": "5 years",
                    "seats": "Varies by state (60 to 403)",
                    "voting_method": "First-Past-The-Post (FPTP)",
                },
                {
                    "name": "Vidhan Parishad (Legislative Council)",
                    "status": "Only 6 states have this upper house",
                    "states_with_council": [
                        "Andhra Pradesh", "Bihar", "Karnataka",
                        "Maharashtra", "Telangana", "Uttar Pradesh",
                    ],
                    "election_type": "Mixed (MLAs, local bodies, graduates, teachers, Governor nominees)",
                },
            ],
            "head": "Chief Minister (leader of majority in Vidhan Sabha)",
            "governor": "Appointed by President on advice of Central Government",
            "conducting_body": "State Election Commission (for local body elections)",
        },
        "local": {
            "level": "Local Self-Government (Panchayati Raj / Urban Bodies)",
            "rural": {
                "name": "Panchayati Raj (3-tier system)",
                "tiers": [
                    {
                        "name": "Gram Panchayat (Village Level)",
                        "head": "Sarpanch / Gram Pradhan",
                        "election": "Direct election by village residents",
                    },
                    {
                        "name": "Panchayat Samiti / Block Panchayat (Block Level)",
                        "head": "Chairperson",
                        "election": "Direct/Indirect depending on state",
                    },
                    {
                        "name": "Zilla Parishad (District Level)",
                        "head": "President / Chairperson",
                        "election": "Indirect election",
                    },
                ],
                "constitutional_basis": "73rd Amendment (1992)",
                "reservation": "1/3 seats reserved for women, SC/ST reservations apply",
            },
            "urban": {
                "name": "Urban Local Bodies",
                "types": [
                    {"name": "Municipal Corporation (Nagar Nigam)", "for": "Large cities (10 lakh+)"},
                    {"name": "Municipal Council (Nagar Palika)", "for": "Smaller cities"},
                    {"name": "Nagar Panchayat / Town Area Committee", "for": "Transitional areas"},
                ],
                "constitutional_basis": "74th Amendment (1992)",
                "head": "Mayor (Corporation) / Chairperson (Council)",
            },
            "conducting_body": "State Election Commission",
        },
    }
    level_key = level.lower().strip()
    if level_key in structures:
        return structures[level_key]
    return {
        "error": f"Unknown level '{level}'. Use 'national', 'state', or 'local'.",
        "available_levels": list(structures.keys()),
    }


def get_election_timeline(election_type: str) -> dict:
    """Get the typical timeline and phases of an Indian election.

    Args:
        election_type: Type of election - 'general', 'state', or 'local'

    Returns:
        Dictionary containing the election timeline phases and key dates.
    """
    timelines = {
        "general": {
            "election_type": "General Election (Lok Sabha)",
            "frequency": "Every 5 years",
            "last_held": "April-June 2024 (18th Lok Sabha)",
            "phases": [
                {
                    "phase": "1. Announcement",
                    "description": "ECI announces election dates, Model Code of Conduct (MCC) comes into effect",
                    "timing": "~45 days before first polling date",
                    "key_actions": ["MCC enforced", "Government cannot announce new policies", "Transfer of officials"],
                },
                {
                    "phase": "2. Nomination",
                    "description": "Candidates file nomination papers",
                    "timing": "~30 days before polling",
                    "key_actions": [
                        "File nomination with Returning Officer",
                        "Security deposit: ₹25,000 (₹12,500 for SC/ST)",
                        "Affidavit with criminal, financial, educational details",
                    ],
                },
                {
                    "phase": "3. Scrutiny",
                    "description": "Returning Officer examines nominations",
                    "timing": "1 day after last nomination date",
                    "key_actions": ["Verify eligibility", "Check documentation", "Accept/reject nominations"],
                },
                {
                    "phase": "4. Withdrawal",
                    "description": "Candidates may withdraw their nominations",
                    "timing": "2 days after scrutiny",
                    "key_actions": ["Final candidate list published", "Ballot order decided by draw of lots"],
                },
                {
                    "phase": "5. Campaigning",
                    "description": "Political campaigning period",
                    "timing": "Until 48 hours before polling",
                    "key_actions": [
                        "Rallies, advertisements, door-to-door",
                        "Campaign silence period: 48 hours before voting",
                        "Expenditure limits enforced",
                    ],
                },
                {
                    "phase": "6. Polling",
                    "description": "Voting day(s) - may be conducted in multiple phases",
                    "timing": "Phased over several weeks for large elections",
                    "key_actions": [
                        "EVM (Electronic Voting Machine) used",
                        "VVPAT (Voter Verified Paper Audit Trail) mandatory",
                        "Indelible ink mark on finger",
                        "Polling hours: typically 7 AM to 6 PM",
                    ],
                },
                {
                    "phase": "7. Counting",
                    "description": "Votes are counted and results declared",
                    "timing": "Usually a single day, after all phases complete",
                    "key_actions": [
                        "EVMs opened at counting centers",
                        "VVPAT verification of random 5 machines per constituency",
                        "Results declared constituency by constituency",
                    ],
                },
                {
                    "phase": "8. Government Formation",
                    "description": "Winning party/coalition forms government",
                    "timing": "Within days of result",
                    "key_actions": [
                        "Majority mark: 272 seats",
                        "President invites largest party/coalition",
                        "PM takes oath, Council of Ministers formed",
                    ],
                },
            ],
        },
        "state": {
            "election_type": "State Assembly Election (Vidhan Sabha)",
            "frequency": "Every 5 years per state",
            "note": "Multiple states may have elections at different times",
            "phases": [
                {"phase": "Announcement", "description": "Similar to general election, MCC applies to state"},
                {"phase": "Nomination & Scrutiny", "description": "Same process, state-level constituencies"},
                {"phase": "Campaigning", "description": "State-specific issues, 48-hour silence period"},
                {"phase": "Polling", "description": "Usually 1-3 phases for most states"},
                {"phase": "Counting & Result", "description": "Chief Minister sworn in by Governor"},
            ],
        },
        "local": {
            "election_type": "Local Body Elections",
            "frequency": "Every 5 years",
            "conducted_by": "State Election Commission (not ECI)",
            "note": "Rules vary significantly by state",
            "general_process": [
                "Delimitation of wards",
                "Reservation of seats (women, SC/ST, OBC)",
                "Nomination and scrutiny",
                "Campaigning (usually shorter period)",
                "Polling (usually single day)",
                "Counting and result declaration",
            ],
        },
    }
    type_key = election_type.lower().strip()
    if type_key in timelines:
        return timelines[type_key]
    return {
        "error": f"Unknown type '{election_type}'. Use 'general', 'state', or 'local'.",
        "available_types": list(timelines.keys()),
    }


def compare_lok_sabha_rajya_sabha() -> dict:
    """Compare Lok Sabha and Rajya Sabha in detail.

    Returns:
        Dictionary with a detailed comparison of both houses of Parliament.
    """
    return {
        "comparison": [
            {
                "aspect": "Full Name",
                "lok_sabha": "House of the People",
                "rajya_sabha": "Council of States",
            },
            {
                "aspect": "Total Members",
                "lok_sabha": "543 elected + 2 nominated (Anglo-Indian, abolished in 2020)",
                "rajya_sabha": "233 elected + 12 nominated by President",
            },
            {
                "aspect": "Election Method",
                "lok_sabha": "Direct election by citizens (FPTP)",
                "rajya_sabha": "Indirect election by state MLAs (STV)",
            },
            {
                "aspect": "Term",
                "lok_sabha": "5 years (can be dissolved earlier)",
                "rajya_sabha": "Permanent body; members serve 6 years, 1/3 retire every 2 years",
            },
            {
                "aspect": "Minimum Age",
                "lok_sabha": "25 years",
                "rajya_sabha": "30 years",
            },
            {
                "aspect": "Presiding Officer",
                "lok_sabha": "Speaker",
                "rajya_sabha": "Vice President of India (ex-officio Chairman)",
            },
            {
                "aspect": "Money Bills",
                "lok_sabha": "Can introduce and pass; Rajya Sabha can only suggest amendments within 14 days",
                "rajya_sabha": "Cannot introduce; can only recommend changes",
            },
            {
                "aspect": "No-Confidence Motion",
                "lok_sabha": "Can pass no-confidence motion against government",
                "rajya_sabha": "Cannot pass no-confidence motion",
            },
            {
                "aspect": "Special Powers",
                "lok_sabha": "Money Bills, Budget approval, No-confidence motion",
                "rajya_sabha": "Can create new All-India Services (Art 312), Shift subjects from State to Concurrent list (Art 249)",
            },
            {
                "aspect": "Can be Dissolved?",
                "lok_sabha": "Yes, by President on PM's advice",
                "rajya_sabha": "No, it is a permanent/continuing body",
            },
        ],
        "key_insight": "Lok Sabha is more powerful in financial matters and government formation, while Rajya Sabha represents states and provides legislative review.",
    }


def get_important_documents_for_voting() -> dict:
    """Get the list of acceptable documents for voter identification at polling booths.

    Returns:
        Dictionary containing acceptable ID documents and their details.
    """
    return {
        "primary_id": {
            "name": "EPIC (Electors Photo Identity Card)",
            "also_known_as": "Voter ID Card",
            "issued_by": "Election Commission of India",
            "how_to_get": "Apply online at NVSP portal or through BLO (Booth Level Officer)",
        },
        "alternative_ids": [
            "Aadhaar Card",
            "MNREGA Job Card",
            "Passbook with photo (issued by Bank/Post Office)",
            "Health Insurance Smart Card (under Ministry of Labour)",
            "Driving License",
            "PAN Card",
            "Smart Card issued by RGI under NPR",
            "Indian Passport",
            "Pension document with photo",
            "Service Identity Card issued by Central/State Govt / PSU / Public Ltd Companies",
            "Official identity card issued to MPs / MLAs / MLCs",
        ],
        "note": "If EPIC is not available, any of the alternative photo IDs listed above can be used. The Presiding Officer at the polling booth has the final say.",
    }


def get_election_commission_info() -> dict:
    """Get information about the Election Commission of India.

    Returns:
        Dictionary containing ECI structure, powers, and key functions.
    """
    return {
        "name": "Election Commission of India (ECI)",
        "established": "25 January 1950",
        "constitutional_basis": "Article 324 of the Constitution",
        "headquarters": "Nirvachan Sadan, New Delhi",
        "website": "https://eci.gov.in",
        "composition": {
            "chief_election_commissioner": "Appointed by President",
            "election_commissioners": "Up to 2 additional commissioners",
            "tenure": "6 years or until age 65, whichever is earlier",
            "removal": "CEC can only be removed through impeachment (like Supreme Court judge)",
        },
        "key_functions": [
            "Conduct free and fair elections at national and state levels",
            "Prepare and update electoral rolls",
            "Register political parties and allot symbols",
            "Enforce Model Code of Conduct",
            "Decide election disputes and disqualifications",
            "Implement voter education programs (SVEEP)",
            "Supervise EVMs and VVPAT machines",
        ],
        "sveep": {
            "full_form": "Systematic Voters' Education and Electoral Participation",
            "goal": "Increase voter awareness and participation",
            "activities": ["Campus ambassadors", "Voter awareness forums", "Social media campaigns"],
        },
    }
