import os
from google.genai import Client

def test_vertex():
    project = "p2-india-election"
    location = "us-east1"
    
    # Use ADC
    client = Client(project=project, location=location, vertexai=True)
    
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hi"
        )
        print(f"Success: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vertex()
