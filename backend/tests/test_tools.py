"""
Tests for ADK agents and tools.
Validates tool functions return correct data structures.
"""

import pytest
from tools.election_data import (
    get_election_structure,
    get_election_timeline,
    compare_lok_sabha_rajya_sabha,
    get_important_documents_for_voting,
    get_election_commission_info,
)
from tools.voter_tools import get_voter_registration_guide, get_voter_eligibility_check
from tools.candidate_tools import (
    get_candidate_disclosure_info,
    get_candidate_check_guide,
    get_voting_day_checklist,
)


# ── Election Data Tools ─────────────────────────────────────────────────

class TestElectionStructure:
    """Tests for get_election_structure tool."""

    def test_national_level(self):
        result = get_election_structure("national")
        assert result["level"] == "National (Central Government)"
        assert len(result["houses"]) == 2
        assert result["conducting_body"] == "Election Commission of India (ECI)"

    def test_state_level(self):
        result = get_election_structure("state")
        assert result["level"] == "State Government"
        assert "Vidhan Sabha" in result["houses"][0]["name"]

    def test_local_level(self):
        result = get_election_structure("local")
        assert "rural" in result
        assert "urban" in result
        assert len(result["rural"]["tiers"]) == 3

    def test_invalid_level(self):
        result = get_election_structure("invalid")
        assert "error" in result
        assert "available_levels" in result

    def test_case_insensitive(self):
        result = get_election_structure("NATIONAL")
        assert "level" in result


class TestElectionTimeline:
    """Tests for get_election_timeline tool."""

    def test_general_timeline(self):
        result = get_election_timeline("general")
        assert result["election_type"] == "General Election (Lok Sabha)"
        assert len(result["phases"]) == 8

    def test_state_timeline(self):
        result = get_election_timeline("state")
        assert "phases" in result

    def test_local_timeline(self):
        result = get_election_timeline("local")
        assert "general_process" in result

    def test_invalid_type(self):
        result = get_election_timeline("invalid")
        assert "error" in result


class TestParliamentComparison:
    """Tests for compare_lok_sabha_rajya_sabha tool."""

    def test_returns_comparison(self):
        result = compare_lok_sabha_rajya_sabha()
        assert "comparison" in result
        assert "key_insight" in result
        assert len(result["comparison"]) >= 10

    def test_comparison_has_both_houses(self):
        result = compare_lok_sabha_rajya_sabha()
        for item in result["comparison"]:
            assert "lok_sabha" in item
            assert "rajya_sabha" in item
            assert "aspect" in item


class TestVotingDocuments:
    """Tests for get_important_documents_for_voting tool."""

    def test_returns_documents(self):
        result = get_important_documents_for_voting()
        assert "primary_id" in result
        assert "alternative_ids" in result
        assert len(result["alternative_ids"]) > 5


class TestECIInfo:
    """Tests for get_election_commission_info tool."""

    def test_returns_eci_data(self):
        result = get_election_commission_info()
        assert result["name"] == "Election Commission of India (ECI)"
        assert "key_functions" in result
        assert "sveep" in result


# ── Voter Tools ──────────────────────────────────────────────────────────

class TestVoterRegistration:
    """Tests for voter registration tools."""

    def test_new_registration_guide(self):
        result = get_voter_registration_guide("new_registration")
        assert "title" in result
        assert "eligibility" in result
        assert "online_steps" in result
        assert "documents_needed" in result

    def test_check_status_guide(self):
        result = get_voter_registration_guide("check_status")
        assert "methods" in result
        assert len(result["methods"]) >= 3

    def test_invalid_action(self):
        result = get_voter_registration_guide("invalid")
        assert "error" in result
        assert "available_actions" in result


class TestVoterEligibility:
    """Tests for voter eligibility check."""

    def test_eligible_voter(self):
        result = get_voter_eligibility_check(age=25, is_citizen=True, has_criminal_disqualification=False)
        assert result["eligible"] is True

    def test_underage_voter(self):
        result = get_voter_eligibility_check(age=16, is_citizen=True, has_criminal_disqualification=False)
        assert result["eligible"] is False

    def test_non_citizen(self):
        result = get_voter_eligibility_check(age=25, is_citizen=False, has_criminal_disqualification=False)
        assert result["eligible"] is False

    def test_disqualified(self):
        result = get_voter_eligibility_check(age=25, is_citizen=True, has_criminal_disqualification=True)
        assert result["eligible"] is False


# ── Candidate Tools ──────────────────────────────────────────────────────

class TestCandidateDisclosure:
    """Tests for candidate disclosure tools."""

    def test_disclosure_info(self):
        result = get_candidate_disclosure_info()
        assert "mandatory_disclosures" in result
        assert "where_to_find" in result
        assert len(result["mandatory_disclosures"]) >= 4

    def test_criminal_record_check(self):
        result = get_candidate_check_guide("criminal_record")
        assert "steps" in result
        assert "red_flags" in result

    def test_assets_check(self):
        result = get_candidate_check_guide("assets")
        assert "steps" in result

    def test_invalid_check(self):
        result = get_candidate_check_guide("invalid")
        assert "error" in result


class TestVotingDayChecklist:
    """Tests for voting day checklist."""

    def test_checklist_structure(self):
        result = get_voting_day_checklist()
        assert "before_voting_day" in result
        assert "what_to_carry" in result
        assert "what_not_to_carry" in result
        assert "at_the_polling_booth" in result
        assert "evm_guide" in result
        assert "special_provisions" in result
        assert "complaints" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
