rm -r dist/
cp .pypirc ~/.pypirc
python setup.py sdist bdist_wheel register -r local upload -r local