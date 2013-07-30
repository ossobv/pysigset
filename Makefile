.PHONY: clean default
.PHONY: dist doc

SOURCES = pysigset.py setup.py
OBJECTS = $(patsubst %.py,%.pyc,$(SOURCES)) $(patsubst %.py,%.pyo,$(SOURCES))

default: dist

clean:
	$(RM) -r MANIFEST README.txt README.rst dist $(OBJECTS)

dist: README.rst $(SOURCES) MANIFEST.in
	# sdist likes a reStructuredText README.txt 
	cp -n README.rst README.txt
	# do the sdist
	python setup.py sdist
	##python setup.py register # only needed once
	#python setup.py sdist upload

doc: README.rst
README.rst: README.md

%.rst: %.md
	# pandoc does its tricks nicely. But we need to tweak it a little bit.
	sh -c 'pandoc $< -t rst > $@'
	# PyPI does not like warnings/errors
	sh -c 'rst2html $@ --no-raw --halt=warning >/dev/null || ( rm -f $@; false )'
