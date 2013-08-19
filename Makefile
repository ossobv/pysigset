.PHONY: clean default
.PHONY: dist doc

SOURCES = pysigset.py setup.py
OBJECTS = $(patsubst %.py,%.pyc,$(SOURCES)) $(patsubst %.py,%.pyo,$(SOURCES))

default: dist

clean:
	$(RM) -r MANIFEST README.txt dist $(OBJECTS)

dist: README.rst $(SOURCES) MANIFEST.in
	# sdist likes a reStructuredText README.txt 
	cp README.rst README.txt
	# do the sdist
	python setup.py sdist
	##python setup.py register # only needed once
	#python setup.py sdist upload
	# remove the README.txt again
	$(RM) README.txt

doc: README.rst
README.rst: Makefile README.md

%.rst: %.md
	# pandoc does its tricks nicely. But we need to tweak it a little bit.
	pandoc $< -t rst > $@
	# PyPI does not like warnings/errors
	sh -c 'rst2html $@ --no-raw --halt=warning >/dev/null || ( rm -f $@; false )'
