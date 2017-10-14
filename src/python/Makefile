build: test
	rm dist/*
	python3 setup.py build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	# build sha file
	/usr/bin/shasum -a 256 dist/* >dist/shasum.256
	# check sha file
	/usr/bin/shasum -c dist/shasum.256
test:
	-sloccount --wide --details . >sloccount.sc
.PHONY: build test