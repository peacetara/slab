build: test
	python3 setup.py build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
test:
	-sloccount --wide --details . >sloccount.sc
.PHONY: build test