There are 2 python programs attached. Also, attached is a presentation with results.

1. airline.py runs analytics on 2007 & 2008 data to solve first 3 questions from the problem statement.
2. predict_airline.py builds the predictive model

1. airline.py:
This can be run from command line or from Jupyter notebook
From command line, > python airline.py path <parm1> <parm2> <parm3>
	'path' is where the input sheets reside
	parm1/2/3 takes the value of 'y' and are optional
	parm1 solves question1, parm2 solves question2 and parm3 solves question3. Parms can be passed in any combination.
For e.g. to get answers for question 1 & 3, pass
> python airline.py path y n y

An exe was generated using pyinstaller; however, the generated package turned out to be 1 GB in space even though source program is 9.9 kb. Therefore, the package is not attached.

Note: Logic for question1 runs quickly. Question 2 takes 20-25 mins and question3 takes around 1 hour.


2. predict_airline.py:
This program is a modeler and not intended to run as a program from start to end.
This builds models using Ridge & Lasso regression. It answers questions 5 & 6.
On account of the configuration of the machine (16Gb, i7), only 100,000 rows (with 651 features/dimensions) are processed from 2007 sheet to allow Modeling within reasonable time.
