all: HEADER.html HEADER.hbs.html

HEADER.html: HEADER.en.html
	mv $< $@

HEADER.%.html: smartypants.py
	python $< $* >$@
