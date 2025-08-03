#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT google_form_generator:app
