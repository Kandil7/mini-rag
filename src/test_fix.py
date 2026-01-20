"""
Test script to verify the fix for the 422 error in the process endpoint
"""
import requests
import json

def test_process_endpoint():
    """
    Test the process endpoint with proper parameters
    """
    # Base URL for the API
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Call without required file_id parameter (should return 400)
    print("Test 1: Calling /api/v1/data/process/1 without file_id parameter")
    try:
        response = requests.get(f"{base_url}/api/v1/data/process/1")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Call with required file_id parameter (should proceed further)
    print("Test 2: Calling /api/v1/data/process/1 with file_id parameter")
    try:
        params = {
            'file_id': 'test_file.txt',
            'chunk_size': 100,
            'overlap_size': 20
        }
        response = requests.get(f"{base_url}/api/v1/data/process/1", params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_process_endpoint()