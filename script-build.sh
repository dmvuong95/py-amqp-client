rm -r dist/
python setup.py sdist bdist_wheel register -r local upload -r local