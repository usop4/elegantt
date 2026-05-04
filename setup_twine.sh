rm -rf dist

python3 -m pip install --upgrade build twine
python3 -m build

ls dist

echo "twine upload -r testpypi dist/*"

twine upload -r testpypi dist/*

echo "twine upload -r pypi dist/*"
