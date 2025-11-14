#!/usr/bin/env python3
"""
Simple Docker Compose test for the bug fix.
This runs inside the Docker container.
"""

import requests
import json
import time
import uuid
import sys

API_URL = "http://api:8000/api/v1"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_step(num, text):
    print(f"\n[Step {num}] {text}")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def wait_for_api():
    """Wait for API to be ready"""
    print_step(0, "Waiting for API to be ready...")

    for i in range(30):
        try:
            response = requests.get(f"{API_URL.replace('/api/v1', '')}/health", timeout=2)
            if response.status_code == 200:
                print_success("API is ready")
                return True
        except:
            pass
        time.sleep(1)
        if i % 5 == 0:
            print(f"  Still waiting... ({i+1}/30)")

    print_error("API is not responding after 30 seconds")
    return False

def create_contract():
    """Create a test contract in the database"""
    print_step(1, "Creating test contract...")

    # For now, we'll just use a UUID since the contracts endpoint might not exist
    contract_id = str(uuid.uuid4())
    print_success(f"Using contract ID: {contract_id}")
    return contract_id

def create_analysis(contract_id):
    """Create an analysis"""
    print_step(2, "Creating analysis...")

    data = {
        "contract_id": contract_id,
        "output_language": "english"
    }

    try:
        response = requests.post(f"{API_URL}/analyses", json=data, timeout=10)

        if response.status_code != 201:
            print_error(f"Failed to create analysis: {response.status_code}")
            print(f"Response: {response.text}")
            return None

        analysis = response.json()
        analysis_id = analysis["id"]

        print_success(f"Analysis created: {analysis_id}")
        print(f"   Status: {analysis['status']}")

        return analysis_id

    except Exception as e:
        print_error(f"Error creating analysis: {e}")
        return None

def check_celery_processing(analysis_id):
    """Check if Celery picked up the task"""
    print_step(3, "Checking if Celery worker picked up the task...")

    time.sleep(3)  # Give Celery a moment to pick up the task

    try:
        response = requests.get(f"{API_URL}/analyses/{analysis_id}", timeout=10)
        if response.status_code == 200:
            analysis = response.json()
            status = analysis["status"]

            if status == "queued":
                print_error(f"Analysis still in 'queued' state after 3 seconds")
                print("   This suggests Celery worker is not processing the task")
                return False
            elif status in ["running", "completed"]:
                print_success(f"Celery worker started processing! Status: {status}")
                return True
            elif status == "failed":
                print_error(f"Analysis failed")
                if "error_message" in analysis:
                    print(f"   Error: {analysis['error_message']}")
                return False
        else:
            print_error(f"Failed to get analysis status: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error checking analysis: {e}")
        return False

def stream_events(analysis_id):
    """Stream SSE events"""
    print_step(4, "Streaming analysis events (SSE)...")

    try:
        response = requests.get(
            f"{API_URL}/analyses/{analysis_id}/stream",
            stream=True,
            timeout=30
        )

        events_received = 0
        start_time = time.time()

        for line in response.iter_lines():
            if time.time() - start_time > 30:
                print_error("Timeout after 30 seconds")
                break

            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        event_type = data.get('type') or data.get('kind')
                        message = data.get('message') or data.get('payload', {}).get('message', 'No message')

                        events_received += 1
                        print(f"📡 Event #{events_received}: {event_type} - {message}")

                        # Check if complete
                        if event_type in ['status_change', 'status'] and 'completed' in str(message).lower():
                            print_success("Analysis completed!")
                            return True

                    except json.JSONDecodeError:
                        pass

        if events_received == 0:
            print_error("No events received from SSE stream")
            print("\n💡 This indicates the BUG is present:")
            print("   - API created Analysis with ID A")
            print("   - Celery created Analysis with ID B (duplicate)")
            print("   - SSE polls for events from A, but events are for B")
            print("   - Result: No events received!")
            return False
        else:
            print_success(f"Received {events_received} events")
            return True

    except Exception as e:
        print_error(f"Error streaming events: {e}")
        return False

def verify_final_status(analysis_id):
    """Verify the final analysis status"""
    print_step(5, "Verifying final status...")

    try:
        response = requests.get(f"{API_URL}/analyses/{analysis_id}", timeout=10)

        if response.status_code == 200:
            analysis = response.json()
            status = analysis["status"]

            print(f"\n   Final status: {status}")

            if status == "completed":
                print_success("Analysis completed successfully!")
                print_success("Bug fix is working! ✅")
                return True
            elif status == "queued":
                print_error("Analysis stuck in 'queued' state")
                print("\n💡 This indicates the BUG is present:")
                print("   - Celery worker may not be running")
                print("   - Or Celery created a duplicate Analysis record")
                return False
            elif status == "running":
                print_error("Analysis still running (may need more time)")
                return False
            elif status == "failed":
                print_error("Analysis failed")
                if "error_message" in analysis:
                    print(f"   Error: {analysis['error_message']}")
                return False
        else:
            print_error(f"Failed to get analysis: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Error verifying status: {e}")
        return False

def main():
    """Run the test"""
    print_header("🧪 Docker Compose Bug Fix Test")

    # Wait for API
    if not wait_for_api():
        sys.exit(1)

    # Create contract
    contract_id = create_contract()
    if not contract_id:
        sys.exit(1)

    # Create analysis
    analysis_id = create_analysis(contract_id)
    if not analysis_id:
        sys.exit(1)

    # Check Celery processing
    celery_working = check_celery_processing(analysis_id)

    # Stream events
    events_received = stream_events(analysis_id)

    # Verify final status
    final_ok = verify_final_status(analysis_id)

    # Summary
    print_header("📊 Test Results Summary")

    print(f"✅ Analysis created: YES")
    print(f"{'✅' if celery_working else '❌'} Celery processing: {'YES' if celery_working else 'NO'}")
    print(f"{'✅' if events_received else '❌'} Events received: {'YES' if events_received else 'NO'}")
    print(f"{'✅' if final_ok else '❌'} Analysis completed: {'YES' if final_ok else 'NO'}")

    if celery_working and events_received and final_ok:
        print_header("🎉 SUCCESS! Bug fix is working!")
        sys.exit(0)
    else:
        print_header("❌ FAILED - Bug fix not working or Celery not running")

        print("\n🔧 Troubleshooting:")
        if not celery_working:
            print("  • Check Celery worker logs: docker-compose logs celery")
            print("  • Verify Redis is running: docker-compose ps redis")
        if not events_received:
            print("  • Check if duplicate Analysis records exist")
            print("  • Run diagnostic: docker-compose exec api python scripts/diagnose.py")

        sys.exit(1)

if __name__ == "__main__":
    main()
