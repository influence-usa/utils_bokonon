export PYTHONPATH=$PYTHONPATH:bokonon/
python -m unittest discover -v -s tests -p 'test_*.py'
