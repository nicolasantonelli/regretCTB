Regretful Now, Impatient Later

An oTree experiment for the master’s thesis “Regretful Now, Impatient Later: An Experimental Exploration of Emotional Carryover in Intertemporal Decisions.”
The experiment explores how emotional experiences, particularly regret, influence subsequent intertemporal decision-making.

Overview

This oTree app contains two main tasks:
	1.	Regret Induction Task (Lottery Wheel):
Participants choose between lotteries and observe outcomes via a spinning arrow. In the treatment group, they also see how much the unchosen lottery would have paid.
	2.	Intertemporal Choice Task (CTB):
Participants allocate a fixed budget between an earlier and a later payoff option. This measures impatience and time discounting.

The experiment ends with:
	•	Regret/Maximization/Future attitudes questionnaire
	•	Demographic questions

Folder Structure

my_experiment/
├── my_experiment/
│   ├── init.py
│   ├── models.py
│   ├── pages.py
│   ├── utils.py
│   ├── static/
│   └── templates/
├── tests/
│   └── test_spin_arrow.py
├── requirements.txt
├── Procfile

Running the Experiment
	1.	Create a virtual environment and install dependencies:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
	2.	Run the local oTree server:
otree devserver

Then open your browser and go to http://localhost:8000

Running Tests

Unit tests are included to check lottery spin outcome logic. To run them:
pytest

Deployment

Ready to deploy via:
	•	oTree Hub
	•	Heroku (using Procfile and Git)

License

This project is for academic, non-commercial use. Contact the author for other uses.

Author: Nicolas Antonelli (MSc in Behavioral and Applied Economics, University of Trento)
Thesis Supervisors: doc. Austėja Kažemekaitytė and prof. Matteo Ploner
