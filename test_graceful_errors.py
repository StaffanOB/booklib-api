#!/usr/bin/env python3
"""
Test script to verify graceful database error handling
"""
import requests
import json

API_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n" + "="*50)
    print("Testing Health Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        data = response.json()
        if data.get('database', {}).get('connected'):
            print("✅ Database is connected")
        else:
            print("⚠️  Database is NOT connected (API still running!)")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def test_books_endpoint():
    """Test the books endpoint"""
    print("\n" + "="*50)
    print("Testing Books Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_URL}/books", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            books = response.json()
            print(f"✅ Success! Found {len(books)} books")
            if books:
                print(f"First book: {json.dumps(books[0], indent=2)}")
        elif response.status_code == 503:
            error = response.json()
            print("⚠️  Service Degraded (expected when DB is down):")
            print(f"   {json.dumps(error, indent=2)}")
            print("✅ API handled database error gracefully!")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def main():
    print("\n" + "="*50)
    print("BookLib API - Graceful Error Handling Test")
    print("="*50)
    print(f"Testing API at: {API_URL}")
    
    test_health_endpoint()
    test_books_endpoint()
    
    print("\n" + "="*50)
    print("Test Complete!")
    print("="*50)
    print("\nTo test with database down:")
    print("1. docker-compose stop postgres")
    print("2. Run this script again")
    print("3. docker-compose start postgres")
    print()

if __name__ == "__main__":
    main()
