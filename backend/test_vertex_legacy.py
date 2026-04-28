import os
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

def test_vertex_legacy():
    project = "p2-india-election"
    location = "us-central1"
    
    vertexai.init(project=project, location=location)
    model = GenerativeModel("gemini-1.5-flash-001")
    
    try:
        response = model.generate_content("Hi")
        print(f"Success: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vertex_legacy()
