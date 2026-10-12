# Pandas Practice Workbook

**Master Pandas through practice, problem-solving, and real-world challenges.**

A hands-on Pandas workbook designed to help you move beyond watching tutorials and start solving problems independently.

This workbook contains **75 challenges** organized into a guided Learning Phase, an independent Testing Phase, and a final customer analytics challenge.

## What's Inside?

### Phase 1: Learning

**Tasks 1–44**

Build your Pandas skills step by step through guided exercises and practical datasets.

Topics include:

- Series and DataFrames
- Data inspection and selection
- Data cleaning and missing values
- Filtering and sorting
- String operations and data types
- GroupBy and aggregations
- Transformations and pivot tables
- Combining datasets with `merge()`, `join()`, and `concat()`
- Date and time operations
- Performance and best practices
- End-to-end data analysis

Use hints and complete solutions with explanations when you need help.

### Phase 2: Testing

**Tasks 45–74**

Put your knowledge to the test with problems that encourage independent thinking.

Challenges include:

- Data cleaning and transformation
- Customer and order analysis
- Grouped calculations
- Merge auditing and debugging
- Performance optimization
- Memory-efficient data processing
- Interview-style questions
- Multi-step analytical problems

The goal is to solve problems without being told exactly which Pandas function to use.

### Final Challenge: Customer Value & Retention Report

**Task 75**

Apply your skills in an end-to-end customer analytics challenge involving customer information, completed orders, revenue, recency, frequency, monetary value, and customer segmentation.

## Features

- 75 hands-on challenges
- Guided learning and independent testing
- Realistic datasets
- Interactive hints
- Complete solutions and explanations
- Debugging and optimization exercises
- Interview-style questions
- A final customer analytics challenge

## Project Structure

```text
pandas-practice-workbook/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── student_performance.csv
├── pandas_practice.ipynb
├── practice_system.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vikasthamke/pandas-practice-workbook.git
cd pandas-practice-workbook
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook pandas_practice.ipynb
```

Run the notebook cells in order and follow the instructions for each task.

## Using the Hint and Solution System

The `practice_system.py` file provides functions to access hints, complete solutions, and task information.

Import the functions in a notebook cell:

```python
from practice_system import hint, answer, list_tasks
```

**Get a hint:**

```python
hint(12)
```

**Get a more detailed hint:**

```python
hint(12, level=2)
```

**Reveal the complete solution:**

```python
answer(12)
```

**List tasks:**

```python
list_tasks()
```

Consult the helper functions whenever you need guidance, but try solving each problem independently first.

## Recommended Learning Approach

1. Attempt the exercise before looking at the solution.
2. Use a hint if you get stuck.
3. Write and test your own code.
4. Review the solution and explanation.
5. Try solving the problem again without assistance.
6. Complete the Testing Phase without relying on hints unnecessarily.
7. Finish the final customer analytics challenge.

**Learn → Practice → Solve → Test → Build**

## Who Is This For?

- Python learners who want to practice Pandas
- Aspiring Data Analysts and Data Scientists
- Machine Learning and AI Engineering learners
- Developers preparing for technical interviews
- Anyone who wants to improve practical data manipulation skills

## Requirements

- Python 3
- Pandas
- NumPy
- Jupyter Notebook

Install the packages listed in `requirements.txt` to get started.

## License

Released under the [MIT License](LICENSE). You may use, copy, modify and share this workbook, including commercially, as long as the copyright and license notice stay with it.

---

Created by **Vikas Thamke**

**SkillPilot — Navigate Your Skills. Build Your Future.**