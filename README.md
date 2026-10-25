# 🎓 Student Expense Tracker

A simple, beginner-friendly, and professional personal finance tracking application designed specifically for college and university students. Built using **Python 3**, **Streamlit**, **Pandas**, and **Matplotlib**, with persistent local storage in a lightweight **CSV** file.

---

## 📖 Project Overview

College life brings multiple daily expenses — from textbooks and semester supplies to cafeteria lunches, transit passes, grocery runs, and weekend outings. Without an organized tracker, students often face month-end financial crunches.

The **Student Expense Tracker** solves this by providing:
1. Fast, single-click entry of daily expenses with categories.
2. Real-time budget monitoring with 80% caution and 100% budget-exceeded alerts.
3. Interactive visual analytics (spending breakdown pie chart and daily spending bar chart).
4. Category and date-range filters to audit spending habits before exams or holidays.
5. Zero complicated setup: no databases, no sign-ups, and no paid API keys.

---

## ✨ Features

- **➕ Add Expenses Seamlessly**: Log date, category, amount, and description.
- **🏷️ Student Categories**: Pre-configured categories: `Food`, `Travel`, `Education`, `Shopping`, `Entertainment`, `Other`.
- **💰 Dynamic Monthly Budget**: Adjust your monthly spending target at any time directly from the sidebar.
- **⚠️ Smart Budget Warnings**:
  - Green indicator when within safe spending limits.
  - Yellow warning when monthly spending crosses **80%** of your budget.
  - Red alert when monthly spending exceeds **100%** of your budget.
- **📊 Interactive Visualizations**:
  - **Category Pie Chart**: Highlights what proportion of your money goes to food vs. textbooks vs. entertainment.
  - **Daily Spending Bar Chart**: Visualizes day-to-day transaction spikes.
- **🔍 Filter & Search**: Filter transactions by custom date range and category multiselect.
- **📋 Clean Tabular Records**: Sortable history table with clean dollar formatting.
- **🗑️ Delete Record**: Safely delete misplaced or test records with instant updates.
- **💾 Local CSV Persistence**: Automatically creates and updates `expenses.csv` on your laptop without data loss between restarts.

---

## 🛠️ Technologies Used

| Technology | Purpose | Why It Was Chosen |
|---|---|---|
| **Python 3.10+** | Core Programming Language | Clean syntax, beginner-friendly, ubiquitous in engineering curricula. |
| **Streamlit** | Web Interface | Lets Python developers build reactive web applications without HTML/CSS/JS. |
| **Pandas** | Data Manipulation & Analysis | Industry-standard tabular DataFrame library for filtering, grouping, and aggregations. |
| **Matplotlib** | Data Visualization | Standard Python plotting library for generating charts cleanly. |
| **CSV (Comma-Separated Values)** | File Storage | Human-readable, portable format that can be opened in Microsoft Excel or Google Sheets. |

---

## 📥 Installation Instructions

### Prerequisites
Make sure you have Python 3.9 or higher installed on your computer. You can check your version in your terminal:
```bash
python3 --version
# or on Windows:
# python --version
```

### Step 1: Clone or Download the Project
Navigate into the project folder in your terminal:
```bash
cd student-expense-tracker
```

### Step 2: Create a Virtual Environment (Recommended)
A virtual environment isolates project dependencies from your system's global Python installation.

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Packages
Install all required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Application

Once dependencies are installed, start the Streamlit local web server:

```bash
streamlit run app.py
```

Streamlit will print the local URL in your terminal:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

Open `http://localhost:8501` in any modern web browser.

---

## 💡 Example Usage Walkthrough

1. **Set Your Target Budget**:
   - In the left sidebar under **Budget Settings**, set your monthly budget (e.g., `$450.00`).
2. **Log Your First Expense**:
   - In the sidebar under **Add New Expense**, enter:
     - Amount: `24.50`
     - Category: `Food`
     - Date: Select today's date
     - Description: `Campus cafeteria lunch & iced coffee`
   - Click **Record Expense**.
3. **Observe Automatic File Creation**:
   - Notice that `expenses.csv` is immediately created in the project folder with your entry.
4. **Inspect Metrics & Visuals**:
   - The top cards update to show `$24.50` spent, `$425.50` remaining, and `Food` as your top spending category.
   - The pie chart and daily bar chart render your transaction immediately.
5. **Test Budget Alerts**:
   - Add another expense of `$350.00` for `Education` (`Course Textbook`).
   - The spending reaches `$374.50` (83.2% of `$450.00`), triggering the **80% Budget Warning banner**.

---

## ⚠️ Project Limitations

1. **Unencrypted Local Storage**:
   - Data is stored in plain-text CSV (`expenses.csv`). Anyone with physical access to your laptop can open and read the file in a text editor or spreadsheet app.
2. **Single-User Concurrent Access**:
   - The CSV file is read from and written to synchronously. It is designed for single-student personal use on one device, not for multi-user simultaneous edits.
3. **Single Currency**:
   - Default currency is USD (`$`). Multi-currency conversion is not included to keep the code simple and beginner-accessible.
4. **Fixed Monthly Horizon**:
   - Budgeting calculations evaluate the current calendar month (from the 1st to the end of the month).

---

## 🔮 Possible Future Improvements

1. **Export Reports to PDF / Excel**: Add an export button to generate monthly PDF expense statements for parents or scholarship compliance.
2. **Recurring Expenses**: Automatically log recurring monthly bills such as campus Wi-Fi, dorm laundry subscriptions, or gym passes.
3. **Receipt Image Attachment**: Let students upload photos of paper receipts stored alongside transaction rows.
