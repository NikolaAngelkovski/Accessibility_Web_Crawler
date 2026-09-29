# Accessibility Web Crawler

A Python-based web accessibility crawler that automatically crawls web pages, extracts HTML content, evaluates common accessibility requirements, calculates accessibility scores, stores results in SQLite, and visualizes the results through a Streamlit dashboard.

## Project Overview

Web accessibility is important for ensuring that websites can be used by people with different abilities and assistive technologies.

Manually checking large websites for accessibility issues can be time-consuming. This project provides an automated solution that crawls a website and evaluates several basic accessibility characteristics.

The system follows this pipeline:

```text
Starting URL
     ↓
Web Crawler
     ↓
URL Manager
     ↓
HTML Parser
     ↓
Accessibility Engine
     ↓
Accessibility Scoring
     ↓
SQLite Database
     ↓
Analytics
     ↓
Dashboard

To run the project, run the following commands:
- pip install -r requirements.txt
- python -m pytest
- python main.py
- python -m streamlit run dashboard/app.py
