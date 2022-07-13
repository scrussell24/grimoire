#!/bin/bash
set -e

isort -s env -c .
black grimoire/. --check


pycodestyle --max-line-length=100 --ignore=E742,W391 grimoire/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Python Lint Error"
    exit $retVal
fi

python -m mypy grimoire/ --exclude env/ --disallow-untyped-defs
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Python Type Checking Error"
    exit $retVal
fi

python -m pytest --cov=grimoire/ tests/
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Python Test Error"
    exit $retVal
fi