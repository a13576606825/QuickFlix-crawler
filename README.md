Development Environment Setup
===

install Python 2
$ cd ProjectFolder
Follow this link to create an isolated python virtual evnviroment. Note the folder name is same as venv.
On OS X and Linux: $ . venv/bin/activate.
ON Windows: $ venv\scripts\activate.
Before proceed to next step, make sure you will see (ENV) in your shell
$ pip install -r requirements.txt to install all required packages.
Dependency
===

Enviroment Isolator: Virtualenv
Framework: Flask 0.10.1
Database: MongoDB
Others:
PyYaml 3.11

Coding Convention
===

JUST BE CONSISTENT!
#####Comments

inline & block comment: start with # Number Sign.
docstrings: surround by ''' ''' or """ """.
#####Naming

function_name and variable_Name: lowercase, with words separated by underscores.
CONSTANT_NAME: all capital letters with words underscores separated by underscores.
