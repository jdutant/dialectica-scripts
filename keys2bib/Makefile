PHONY: test

test: output.bib

output.bib: keys2bib.py source.bib keyfile.txt 
	@python3 keys2bib.py --keys keyfile.txt --source source.bib --output output.bib
