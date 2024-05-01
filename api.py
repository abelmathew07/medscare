import requests

# Define the URL of the API endpoint
url = 'http://localhost:5000/generate_opticket'  # Adjust the URL if necessary

data = {
    "hospital_name": "Sample Hospital",
    "patient_name": "John Doe",
    "address": "123 Main St, City, Country",
    "symptoms": "Body pain, cough, headache",
    "predicted_disease": "Viral Fever"
}

# Send a POST request to the API endpoint with JSON data
response = requests.post(url, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Save the PDF content to a file
    with open('opticket.pdf', 'wb') as f:
        f.write(response.content)
    print("PDF generated successfully!")
else:
    # Print the error message if the request failed
    print("Error:", response.text)
