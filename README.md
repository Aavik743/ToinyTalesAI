# Toiny Tales AI

This application leverages the power of AI to generate short, engaging stories for children.  It provides a simple and interactive interface where users can input keywords or themes, and the AI will craft a unique tale based on their input.  The stories are designed to be imaginative and educational, fostering creativity and a love of reading and listening in young minds.

A Python-based web application with static assets.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
uvicorn main:app --reload
```

## Project Structure
```
.
├── main.py              - Main application entry point
├── requirements.txt     - Python dependencies
└── static/              - Web assets
    ├── index.html       - Main page
    ├── style.css        - Stylesheet
    └── script.js        - Client-side scripting
