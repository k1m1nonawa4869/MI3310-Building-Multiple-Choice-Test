#  MI3310-Multiple-Test-Managing

Project aims to create a simple Multiple Choice Test software that can help students & teachers in: creating and managing question banks, creating exams based on requirements, and score the exam from file. 

## Prerequisites:

- **Python 3.7+** (no external packages required; uses the standard library)  
- **Git CLI** (optional, for version control and branch operations)  
  - VS Code’s Source Control panel requires a system‐installed Git  

## What to do:

- First Clone this project to your local device. Use `Main` branch, select `Code -> Download ZIP` or use with your Github Desktop.
- Then run `cli.py` and enjoy the software.
- JSON file can be manually created if you are lazy to create through GUI. Following the syntax:
    - `[{"username":, "password":, "name":, "admin":, "verified"]` for Users.json
	- `originId,type,destId,amount,origBal,destBal,timestamp` for transactions.txt

## What you can do:
- **User Management**  
   - Registration & plain-text password storage (temporary)  
   - Admin approval workflow (only verified users may log in)  
   - Admin vs. Student roles  

- **Question Bank Management**  
   - Add new multiple-choice questions (ID, question text, 4 options, correct answer, difficulty)  
   - Edit existing questions  
   - Remove questions  

- **Exam Generation**  
   - Specify how many questions to pull from each difficulty level  
   - Random selection (no duplicates)  
   - Produces a `.txt` file (e.g. `EXAMID.txt`) with numbered questions and answer choices  
   - Records correct answer list in `exam.json`  

- **Student Testing & Scoring**  
   - Students “take” an exam by specifying an exam ID, viewing a text file, and entering answers in `“<number>.<letter>”` format  
   - Answers are saved to `answers.json` with `score = null` initially  
   - Admin can “Grade Exams”: compares student answers to the exam’s `rightanswer` list, calculates a raw score (0–10), rounds (0.5 rounds up), and stores an integer score in `answers.json`  

- **Reporting**  
   - Admin can generate a report per exam ID showing:  
     - Highest, lowest, average, variance  
     - Histogram of scores (0–10)  

- **Student Score Viewing**  
   - After grading, students can view their past exam(s) and see either “Not yet graded” or “X/10”

##  Program Structure:

├── README.md
├── cli.py
├── models.py
├── user_manager.py
├── question_manager.py
├── exam_manager.py
├── utils.py
├── User.json
├── questions.json
├── exam.json
└── answers.json

- **README.md**: Describes the project overview, setup instructions, and usage.

- **cli.py**: The main entry point. Presents menus for registration, login, and logout, and routes to the appropriate admin or student workflows.

- **models.py** : Defines the `User` and `Question` classes with methods to convert between Python objects and the JSON structure.

- **user_manager.py**: Handles user registration, login, and admin approval (CRUD for user accounts stored in `User.json`).

- **question_manager.py**: Manages the question bank: adding, editing, and removing questions (CRUD for `questions.json`).

- **exam_manager.py**: Implements exam creation (random selection by difficulty), student answer submission, grading, report generation, and student‐score viewing (all JSON I/O for `exam.json` and `answers.json`).

- **utils.py**: Provides helper functions for safe JSON loading/saving, parsing student answer strings, rounding scores, and building histograms.

- **User.json**: Stores registered user accounts.

- **questions.json**: Stores all multiple‐choice questions.

- **exam.json**: Stores each generated exam’s metadata.

- **answers.json**: Records student submissions and scores.

## Testing
We are documenting, stay tuned...

## Roadmap

What we wants to implement if having more time:

- Automated test suite
- GUI window
- Integration with a real database
- Support varies subject
- Online?

##  Credits:

Special thanks to @QuangDuong2005 (initial structures and code) for the project.


##  Contributions:

Please open an issue or submit a pull request.

Feel free to suggest new features or report bugs!

## License:
I dont't know
