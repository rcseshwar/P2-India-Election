"""
Voter registration and NVSP tools for the Voter Registration Agent.
Provides guidance on voter registration processes.
"""


def get_voter_registration_guide(action: str) -> dict:
    """Get step-by-step guide for voter registration actions on NVSP.

    Args:
        action: The registration action - 'new_registration', 'update_details',
                'check_status', 'download_voter_id', 'find_polling_booth',
                'corrections', or 'overseas_registration'

    Returns:
        Dictionary with step-by-step instructions for the requested action.
    """
    guides = {
        "new_registration": {
            "title": "New Voter Registration (Form 6)",
            "eligibility": [
                "Indian citizen",
                "Must be 18 years or older on the qualifying date (1st January of the year)",
                "Ordinarily resident in the constituency",
                "Not disqualified under any law",
            ],
            "online_steps": [
                "1. Visit https://www.nvsp.in or https://voters.eci.gov.in",
                "2. Click on 'Register as New Voter' or 'Form 6'",
                "3. Log in / Create an account (mobile OTP verification)",
                "4. Fill in personal details: Name, Date of Birth, Gender",
                "5. Enter current address (this determines your constituency)",
                "6. Upload documents: Age proof + Address proof + Passport photo",
                "7. Submit and note the Reference ID",
                "8. BLO (Booth Level Officer) will verify at your address",
                "9. Once approved, EPIC (Voter ID) will be issued",
            ],
            "documents_needed": {
                "age_proof": ["Birth Certificate", "10th Marksheet", "Aadhaar Card", "Passport", "PAN Card"],
                "address_proof": [
                    "Aadhaar Card", "Passport", "Driving License",
                    "Utility Bill (recent)", "Bank Passbook", "Rent Agreement",
                ],
                "photo": "Recent passport-size photograph",
            },
            "offline_option": "Visit your nearest ERO (Electoral Registration Officer) office with Form 6 and documents",
            "processing_time": "Typically 15-30 days after BLO verification",
        },
        "update_details": {
            "title": "Update Voter Details (Form 8)",
            "scenarios": {
                "name_correction": "Form 8 - Section for correction of entries",
                "address_change_same_constituency": "Form 8A",
                "address_change_different_constituency": "Form 6 (new registration in new constituency)",
                "photo_update": "Form 8 with new photograph",
            },
            "steps": [
                "1. Visit https://www.nvsp.in",
                "2. Select 'Correction in Voter Details' (Form 8)",
                "3. Enter your EPIC number",
                "4. Select the fields to update",
                "5. Upload supporting documents",
                "6. Submit and track with Reference ID",
            ],
        },
        "check_status": {
            "title": "Check Voter Registration Status",
            "methods": [
                {
                    "method": "Online via NVSP",
                    "steps": [
                        "Visit https://www.nvsp.in",
                        "Click 'Search in Electoral Roll'",
                        "Search by: EPIC Number OR Name + Details",
                        "View your registration status and polling booth",
                    ],
                },
                {
                    "method": "Via Voter Helpline App",
                    "steps": [
                        "Download 'Voter Helpline' app from Play Store / App Store",
                        "Search using EPIC number or personal details",
                        "View complete voter details and booth info",
                    ],
                },
                {
                    "method": "Via SMS",
                    "steps": [
                        "SMS: EPIC <space> <Your EPIC Number> to 1950",
                        "Receive status via SMS reply",
                    ],
                },
                {
                    "method": "Helpline",
                    "steps": [
                        "Call 1950 (Toll-free Voter Helpline)",
                        "Available in multiple languages",
                    ],
                },
            ],
        },
        "download_voter_id": {
            "title": "Download e-EPIC (Digital Voter ID)",
            "steps": [
                "1. Visit https://voters.eci.gov.in",
                "2. Login with your registered mobile number",
                "3. Go to 'Download e-EPIC' section",
                "4. Verify your identity via OTP",
                "5. Download the e-EPIC in PDF format",
                "6. e-EPIC is equally valid as physical EPIC card",
            ],
            "note": "e-EPIC can also be accessed through the Voter Helpline App",
        },
        "find_polling_booth": {
            "title": "Find Your Polling Booth",
            "steps": [
                "1. Visit https://www.nvsp.in → 'Search in Electoral Roll'",
                "2. Enter your EPIC number or search by name",
                "3. Your polling booth details will be shown",
                "4. Note: Booth number, Part number, and Address",
            ],
            "tip": "Check this before election day to know exactly where to go",
        },
        "corrections": {
            "title": "Corrections in Voter ID",
            "steps": [
                "1. Visit https://www.nvsp.in",
                "2. Select Form 8 for corrections",
                "3. Enter EPIC number",
                "4. Select field to correct (Name, Age, Photo, Address, etc.)",
                "5. Upload supporting documents",
                "6. Submit and track using Reference ID",
            ],
        },
        "overseas_registration": {
            "title": "Overseas/NRI Voter Registration (Form 6A)",
            "eligibility": [
                "Indian citizen residing abroad",
                "Name not in electoral roll in India",
                "Has a valid Indian passport",
            ],
            "steps": [
                "1. Visit https://www.nvsp.in",
                "2. Fill Form 6A for Overseas Voter Registration",
                "3. Register for the constituency of your passport address",
                "4. Can vote in person at the designated polling booth",
                "5. OR use Electronically Transmitted Postal Ballot System (ETPBS) if available",
            ],
        },
    }
    action_key = action.lower().strip().replace(" ", "_")
    if action_key in guides:
        return guides[action_key]
    return {
        "error": f"Unknown action '{action}'.",
        "available_actions": list(guides.keys()),
        "tip": "Try 'new_registration', 'check_status', or 'update_details'",
    }


def get_voter_eligibility_check(age: int, is_citizen: bool, has_criminal_disqualification: bool) -> dict:
    """Check if a person is eligible to vote in Indian elections.

    Args:
        age: The person's age in years
        is_citizen: Whether the person is an Indian citizen
        has_criminal_disqualification: Whether the person has any criminal disqualification

    Returns:
        Dictionary with eligibility status and explanation.
    """
    eligible = True
    reasons = []

    if age < 18:
        eligible = False
        reasons.append(f"Must be 18 or older. Current age: {age}. Can register when turning 18.")
    if not is_citizen:
        eligible = False
        reasons.append("Must be an Indian citizen.")
    if has_criminal_disqualification:
        eligible = False
        reasons.append("Persons with certain criminal convictions may be disqualified.")

    return {
        "eligible": eligible,
        "age": age,
        "reasons": reasons if not eligible else ["Meets all eligibility criteria"],
        "next_step": "Proceed to voter registration at https://www.nvsp.in" if eligible
        else "Address the above issues before applying",
    }
