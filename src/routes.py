from flask import request, jsonify, make_response
from models import db, ContactFormSubmission


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def get_health():
    if request.method == "GET":
        return _corsify_actual_response(jsonify({"message": "Health OK"}))


def store_contact():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    elif request.method == "POST":
        try:
            data = request.get_json()
            name = data.get("name", "")
            email = data.get("email", "")
            subject = data.get("subject", "")
            message = data.get("message", "")

            # Create a new contact form submission
            new_submission = ContactFormSubmission(
                name=name, email=email, subject=subject, message=message
            )
            db.session.add(new_submission)
            db.session.commit()

            return _corsify_actual_response(
                jsonify({"message": "Form submitted successfully"})
            )
        except Exception as e:
            return _corsify_actual_response(
                jsonify({"message": "Error processing request", "error": str(e)})
            )
