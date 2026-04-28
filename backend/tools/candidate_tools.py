"""
Candidate information tools providing data about candidate disclosures and background checks.
"""


def get_candidate_disclosure_info() -> dict:
    """Get information about mandatory candidate disclosures in Indian elections.

    Returns:
        Dictionary with details about what candidates must disclose.
    """
    return {
        "legal_basis": "Section 33A of Representation of the People Act, 1951 + Supreme Court directives",
        "mandatory_disclosures": [
            {
                "category": "Criminal Records",
                "details": [
                    "All pending criminal cases (FIRs, charge sheets)",
                    "Past convictions including imprisonment",
                    "Cases of cognizable offenses",
                ],
                "where_to_check": "Affidavit filed with nomination papers, available on ECI website",
            },
            {
                "category": "Financial Assets",
                "details": [
                    "Movable assets (cash, bank deposits, investments, vehicles, jewelry)",
                    "Immovable assets (land, buildings, property)",
                    "Assets of spouse and dependents",
                    "Liabilities and outstanding dues",
                ],
                "where_to_check": "Affidavit on ECI website and MyNeta.info",
            },
            {
                "category": "Educational Qualifications",
                "details": ["Highest educational qualification attained"],
                "where_to_check": "Nomination affidavit",
            },
            {
                "category": "Income Tax Returns",
                "details": ["Last 5 years of income tax returns"],
                "where_to_check": "Affidavit filed with nomination",
            },
        ],
        "where_to_find": [
            {
                "source": "Election Commission of India",
                "url": "https://eci.gov.in → Candidate Affidavits",
                "description": "Official source for all nomination affidavits",
            },
            {
                "source": "Association for Democratic Reforms (ADR)",
                "url": "https://myneta.info",
                "description": "Comprehensive database of candidate records, criminal cases, assets",
            },
            {
                "source": "National Election Watch",
                "url": "https://www.myneta.info/new",
                "description": "Analysis reports on candidates and parties",
            },
        ],
        "right_to_know": "Supreme Court (2002) ruled that voters have a fundamental right to know the background of candidates.",
    }


def get_candidate_check_guide(check_type: str) -> dict:
    """Guide users on how to check specific candidate information.

    Args:
        check_type: Type of check - 'criminal_record', 'assets', 'performance', or 'party_history'

    Returns:
        Dictionary with steps to check the specified information.
    """
    guides = {
        "criminal_record": {
            "title": "How to Check a Candidate's Criminal Record",
            "steps": [
                "1. Visit https://myneta.info",
                "2. Search by candidate name, constituency, or party",
                "3. View 'Criminal Cases' section in the candidate profile",
                "4. Check the official affidavit on ECI website for details",
                "5. IPC sections and case status will be listed",
            ],
            "important_note": "Candidates with criminal charges must publish this information in newspapers and on TV within the constituency (Supreme Court order, 2020).",
            "red_flags": [
                "Cases involving serious charges (IPC 302, 376, 420, etc.)",
                "Multiple pending cases",
                "Cases under PMLA, UAPA, or other special laws",
            ],
        },
        "assets": {
            "title": "How to Check a Candidate's Assets",
            "steps": [
                "1. Visit https://myneta.info",
                "2. Search the candidate",
                "3. View 'Assets & Liabilities' section",
                "4. Compare with previous election declarations to see growth",
                "5. Check if asset growth is proportional to declared income",
            ],
            "what_to_look_for": [
                "Total declared assets vs. declared income",
                "Percentage increase in assets since last election",
                "Any undeclared properties",
                "Liabilities and loans",
            ],
        },
        "performance": {
            "title": "How to Check an Incumbent's Performance",
            "resources": [
                {
                    "name": "PRS Legislative Research",
                    "url": "https://prsindia.org",
                    "tracks": ["Questions raised", "Bills introduced", "Attendance", "Debates participated"],
                },
                {
                    "name": "Lok Sabha / Rajya Sabha websites",
                    "url": "https://sansad.in",
                    "tracks": ["Session-wise participation", "Committee memberships"],
                },
                {
                    "name": "MPLADS (MP Local Area Development Scheme)",
                    "url": "https://www.mplads.gov.in",
                    "tracks": ["Funds allocated and utilized for constituency development"],
                },
            ],
        },
        "party_history": {
            "title": "How to Check Party-Hopping History",
            "steps": [
                "1. Visit https://myneta.info → search candidate",
                "2. Check 'Election History' section",
                "3. See which parties the candidate has contested from",
                "4. Anti-Defection Law (52nd Amendment) penalizes switching after election",
            ],
        },
    }
    key = check_type.lower().strip().replace(" ", "_")
    if key in guides:
        return guides[key]
    return {
        "error": f"Unknown check type '{check_type}'.",
        "available_types": list(guides.keys()),
    }


def get_voting_day_checklist() -> dict:
    """Get a comprehensive voting day checklist and guide.

    Returns:
        Dictionary with everything a voter needs to know on polling day.
    """
    return {
        "before_voting_day": [
            "✅ Check your name in the electoral roll at https://www.nvsp.in",
            "✅ Note your polling booth number and address",
            "✅ Keep your Voter ID (EPIC) or alternative photo ID ready",
            "✅ Check polling time (usually 7 AM - 6 PM, varies by region)",
            "✅ Check if your employer has given you paid leave (mandatory under S.135B of RP Act)",
        ],
        "what_to_carry": [
            "Voter ID Card (EPIC) or any approved alternative photo ID",
            "Voter slip (if received from BLO, helpful but not mandatory)",
        ],
        "what_not_to_carry": [
            "❌ Mobile phones (not allowed inside polling booth)",
            "❌ Cameras or recording devices",
            "❌ Any items showing party symbols or colors",
            "❌ Weapons of any kind",
        ],
        "at_the_polling_booth": [
            "1. Join the queue at your designated booth",
            "2. Show your ID to the Polling Officer",
            "3. Your name is checked in the electoral roll",
            "4. Indelible ink is applied on your left index finger",
            "5. You receive a ballot slip from the Presiding Officer",
            "6. Enter the voting compartment (alone and in secrecy)",
            "7. Press the button on the EVM next to your chosen candidate's name and symbol",
            "8. Check the VVPAT slip (visible for 7 seconds) to confirm your vote",
            "9. Exit the booth",
        ],
        "evm_guide": {
            "what_is_evm": "Electronic Voting Machine - used in India since 2004 nationwide",
            "how_it_works": [
                "Two units: Control Unit (with Presiding Officer) and Ballot Unit (in voting compartment)",
                "Candidate names, party names, and symbols are displayed",
                "Press the blue button next to your preferred candidate",
                "A beep sound and light confirm your vote",
                "VVPAT prints a paper slip visible through a glass window for 7 seconds",
            ],
            "nota_option": "NOTA (None of the Above) button is available at the end of the candidate list",
        },
        "special_provisions": [
            "Persons with disabilities can bring a companion to assist",
            "Braille-enabled EVMs available for visually impaired voters",
            "Wheelchairs and ramps provided at polling booths",
            "Pregnant women and elderly can request priority in queue",
            "Postal ballot available for certain categories (service voters, absentee voters)",
        ],
        "complaints": {
            "booth_issues": "Report to the Presiding Officer",
            "helpline": "Call 1950",
            "app": "Use cVIGIL app to report violations with photos/videos",
            "online": "https://eci.gov.in → Grievance Portal",
        },
    }
