rm -r dist

python3 setup.py sdist

python3 setup.py bdist_wheel

ls dist

echo "twine upload -r testpypi dist/*"

twine upload -r testpypi dist/*

echo "twine upload -r pypi dist/*"
