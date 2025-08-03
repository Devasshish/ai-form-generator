from flask import Flask, request, jsonify, render_template
import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

app = Flask(__name__)

# Load credentials and initialize Google Forms API
def get_forms_service():
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/forms.body']
    )
    service = build('forms', 'v1', credentials=creds)
    return service

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-form', methods=['POST'])
def create_form():
    data = request.json
    title = data.get('title', 'Untitled Form')
    questions = data.get('questions', [])

    try:
        service = get_forms_service()

        # Create the form
        NEW_FORM = {
            "info": {
                "title": title
            }
        }
        result = service.forms().create(body=NEW_FORM).execute()
        form_id = result["formId"]

        # Add questions
        requests = []
        for question in questions:
            requests.append({
                "createItem": {
                    "item": {
                        "title": question["question"],
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": opt} for opt in question["options"]],
                                    "shuffle": False
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 0
                    }
                }
            })

        # Batch update the form
        service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()

        return jsonify({"formUrl": f"https://docs.google.com/forms/d/{form_id}/edit", "formId": form_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
