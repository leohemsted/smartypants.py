all: HEADER.html HEADER.hbs.html checksums

HEADER.html: HEADER.en.html
	mv $< $@

HEADER.%.html: smartypants.py
	python3 $< $* >$@

checksums:
	rm -f md5sums sha512sums
	set -e; for f in smartypants.py-*; do md5sum $$f >>md5sums; sha512sum $$f >>sha512sums; done

emit:
	bzr tags |while read tagname revno; do bzr cat -r$$revno smartypants.py >>$$tagname; done
