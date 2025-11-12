"""
API Testing Script
Test the complete backend flow
"""

import requests
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"


def test_health():
    """Test health check"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Health check passed: {data}")
    return data


def test_register():
    """Test user registration"""
    print("\nTesting user registration...")
    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/auth/register",
        json={
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    print(f"✓ Registration successful")
    print(f"  User ID: {data['user']['id']}")
    print(f"  Tier: {data['user']['tier']}")
    print(f"  Analyses remaining: {data['user']['analyses_remaining']}")
    return data["access_token"]


def test_login(email: str, password: str):
    """Test user login"""
    print("\nTesting login...")
    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Login successful")
    return data["access_token"]


def test_get_me(token: str):
    """Test get current user"""
    print("\nTesting get current user...")
    response = requests.get(
        f"{BASE_URL}{API_PREFIX}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Get user successful")
    print(f"  Email: {data['email']}")
    print(f"  Tier: {data['tier']}")
    return data


def test_upload_contract(token: str, file_path: str):
    """Test contract upload"""
    print("\nTesting contract upload...")
    with open(file_path, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/contracts/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (Path(file_path).name, f, "application/pdf")}
        )
    assert response.status_code == 201
    data = response.json()
    print(f"✓ Upload successful")
    print(f"  Contract ID: {data['contract_id']}")
    print(f"  Filename: {data['filename']}")
    return data["contract_id"]


def test_list_contracts(token: str):
    """Test contract listing"""
    print("\nTesting contract listing...")
    response = requests.get(
        f"{BASE_URL}{API_PREFIX}/contracts",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Listing successful")
    print(f"  Total contracts: {data['total']}")
    return data


def test_get_contract(token: str, contract_id: str):
    """Test get contract"""
    print("\nTesting get contract...")
    response = requests.get(
        f"{BASE_URL}{API_PREFIX}/contracts/{contract_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Get contract successful")
    print(f"  Status: {data['status']}")
    return data


def test_create_analysis(token: str, contract_id: str):
    """Test create analysis"""
    print("\nTesting create analysis...")
    response = requests.post(
        f"{BASE_URL}{API_PREFIX}/analyses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "contract_id": contract_id,
            "output_language": "english"
        }
    )
    assert response.status_code == 201
    data = response.json()
    print(f"✓ Analysis created")
    print(f"  Analysis ID: {data['id']}")
    print(f"  Status: {data['status']}")
    return data["id"]


def test_get_analysis(token: str, analysis_id: str):
    """Test get analysis"""
    print("\nTesting get analysis...")
    max_retries = 60  # Wait up to 60 seconds
    for i in range(max_retries):
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/analyses/{analysis_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()

        if data['status'] in ['succeeded', 'failed']:
            print(f"✓ Analysis completed")
            print(f"  Status: {data['status']}")
            if data.get('confidence_score'):
                print(f"  Confidence: {data['confidence_score']}")
            if data.get('formatted_output'):
                print(f"  Has output: Yes")
            return data

        print(f"  Waiting... (attempt {i+1}/{max_retries}, status: {data['status']})")
        time.sleep(1)

    raise Exception("Analysis timed out")


def main():
    """Run all tests"""
    print("=" * 60)
    print("LEGALLY AI - API TESTING")
    print("=" * 60)

    try:
        # Test health
        test_health()

        # Test authentication
        token = test_register()

        # Test user endpoints
        user = test_get_me(token)

        # Test contract upload (you need to provide a test file)
        # For now, skip if no test file exists
        test_file = Path(__file__).parent / "test_contract.pdf"
        if test_file.exists():
            # Test contract endpoints
            contract_id = test_upload_contract(token, str(test_file))
            test_list_contracts(token)
            test_get_contract(token, contract_id)

            # Test analysis
            analysis_id = test_create_analysis(token, contract_id)
            test_get_analysis(token, analysis_id)
        else:
            print(f"\n⚠ Skipping contract tests (test file not found: {test_file})")

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
