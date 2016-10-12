## Purpose
>#### Web crawler to crawler web content relating movie comments.

### Development Environment Setup
===
0. install Python 2
1. `$ cd ProjectFolder`
2. Follow this [link](http://flask.pocoo.org/docs/0.10/installation/#virtualenv) to create an isolated python virtual evnviroment. note the folder should be `venv`.
3. * On OS X and Linux: `$ . venv/bin/activate`.
   * ON Windows: `$ v-env\scripts\activate`.
4. Before proceed to next step, make sure you will see `(ENV)` in your shell
5. `$ pip install -r requirements.txt` to install all required packages.


### Database Setup
===
0. Download [MongoDB community server](https://www.mongodb.com/download-center?jmp=nav#community)
1. Follow this [guide](https://docs.mongodb.com/v3.2/administration/install-community/) to setup & run mongoDb locally


### Dependency
===
* **Enviroment Isolator**: Virtualenv
* **Framework**: Flask==0.10.1
* **Database**: MongoDB
* **Others**:
  * pymongo==3.0.1
	* PyYaml==3.11
  * Requests==2.9.1


### Coding Convention
===
>#### JUST BE CONSISTENT!

#####Comments
1. **inline & block comment**: start with # Number Sign.
2. **docstrings**: surround by ''' ''' or """ """.

#####Naming
1. **function_name and variable_Name**: lowercase, with words separated by underscores.
2. **CONSTANT_NAME**: all capital letters with words underscores separated by underscores.
