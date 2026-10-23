AI-Assisted Software Testing and Literature Analysis

**Overview**

This project demonstrates Python-based analysis of software-testing research literature and an illustrative workflow for AI-assisted test generation.

**Features**
- Keyword-based coding of research abstracts.
- Frequency analysis of testing activities, techniques, and barriers.
- Publication trends by year.
- Visualization using Matplotlib.
- Prompt construction from user stories and acceptance criteria.
- Basic rule-based screening of example Playwright test code.

**Project Structure**
- literature_matrix.csv — sample literature dataset.
- literature_coding.py — literature coding and visualization.
- ai_test_generation.py — prompt construction and example test-code screening.
- requirements.txt — Python dependencies.
- outputs/ — generated charts and coded dataset, if configured.

**Requirements**
- Python 3.10 or later.
- pandas.
- matplotlib.

**Installation**
Install the dependencies:
python -m pip install -r requirements.txt

**Usage**

Run the literature analysis:

python literature_coding.py

Run the illustrative test-generation workflow:

python ai_test_generation.py

The literature script processes the CSV dataset and produces a chart and a coded dataset. The test-generation script builds a prompt and screens predefined example code.

**Current Limitations**

The test-generation script does not currently call an LLM API or execute Playwright tests. Its code screening is a basic demonstration and does not replace security analysis or human review.

The literature coding relies on keyword matching, so results should be validated before drawing research conclusions.

**Technologies**

Python, Pandas, Matplotlib, regular expressions, Playwright (TypeScript as the target testing framework), Git, and GitHub.

**Academic Use**

This repository supports an academic project on literature analysis and AI-assisted software testing. Sample data and illustrative results should not be interpreted as comprehensive research findings.

