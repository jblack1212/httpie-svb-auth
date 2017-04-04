all: dummy

dummy:
	echo "Run 'make deploy' to deploy to PyPI."

deploy:
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*

clean:
	git clean -dxf
