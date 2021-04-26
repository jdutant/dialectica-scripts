.PHONY: test

test: sample_completed.bib

sample_completed.bib: selfcites.py sample.bib source.bib 
	@python3 selfcites.py sample.bib --source source.bib --suffix _completed
