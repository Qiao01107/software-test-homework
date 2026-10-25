from fastapi.testclient import TestClient

from .test_api_contract import create_todo


def test_update_with_null_title_should_not_produce_internal_server_error(
    client: TestClient,
) -> None:
    """The request schema accepts nullable title, but the response schema does not."""
    created = create_todo(client, title="Non-null title")

    response = client.put(f"/todos/{created['id']}", json={"title": None})

    # This is intentionally a defect probe. The current implementation returns 500.
    assert response.status_code in {200, 422}, (
        f"observed status={response.status_code}, body={response.text!r}"
    )
