from mergemind.models.api import RunReviewRequest
from mergemind.models.domain import PBI, ChangedFile, PullRequest
from mergemind.models.review_packet import RetrievedChunk


class MockPacketBuilder:
    def build_pr(self, request: RunReviewRequest) -> PullRequest:
        return PullRequest(
            id=request.pr_number or 0,
            title="Add input validation to user registration endpoint",
            body=(
                "This PR adds validation for the registration API payload before "
                "creating a user record. It checks for missing email and password "
                "fields and returns HTTP 400 for invalid requests."
            ),
            branch="feature/registration-input-validation",
            changed_files=[
                ChangedFile(
                    path="src/api/registration.py",
                    patch=(
                        "@router.post('/register')\n"
                        "def register_user(payload: dict):\n"
                        "    email = payload.get('email')\n"
                        "    password = payload.get('password')\n"
                        "\n"
                        "    if not email or not password:\n"
                        "        raise HTTPException(status_code=400, detail='Missing fields')\n"
                        "\n"
                        "    create_user(email=email, password=password)\n"
                        "    return {'status': 'ok'}\n"
                    ),
                    status="modified",
                ),
                ChangedFile(
                    path="tests/test_registration.py",
                    patch=(
                        "def test_register_user_missing_email(client):\n"
                        "    response = client.post('/register', json={'password': 'secret'})\n"
                        "    assert response.status_code == 400\n"
                    ),
                    status="modified",
                ),
            ],
        )

    def build_pbi(self, request: RunReviewRequest) -> PBI | None:
        if not request.pbi_id:
            return None

        return PBI(
            id=request.pbi_id,
            title="Validate registration payload before persistence",
            description=(
                "As a platform engineer, I want the registration endpoint to validate "
                "incoming payloads before user creation so that invalid data is rejected "
                "early and does not reach the persistence layer."
            ),
            acceptance_criteria=[
                "Reject requests with missing email.",
                "Reject requests with missing password.",
                "Return HTTP 400 for invalid payloads.",
                "Add automated tests for validation failures.",
            ],
        )

    def build_retrieved_chunks(self) -> list[RetrievedChunk]:
        return [
            RetrievedChunk(
                source_type="doc",
                source_id="api-guidelines",
                path="docs/api_guidelines.md",
                content=(
                    "All external API inputs must be validated before any database write. "
                    "Validation failures should return HTTP 400 with a clear error message."
                ),
                score=0.95,
            ),
            RetrievedChunk(
                source_type="doc",
                source_id="testing-standards",
                path="docs/testing_standards.md",
                content=(
                    "Each validation branch must have at least one automated negative test. "
                    "Tests should cover missing required fields and malformed input."
                ),
                score=0.91,
            ),
            RetrievedChunk(
                source_type="code",
                source_id="src/api/profile.py",
                path="src/api/profile.py",
                content=(
                    "@router.post('/profile')\n"
                    "def create_profile(payload: dict):\n"
                    "    if 'name' not in payload:\n"
                    "        raise HTTPException(status_code=400, detail='Missing name')\n"
                    "    ...\n"
                ),
                score=0.82,
            ),
        ]
