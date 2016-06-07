#! /bin/bash

rm -rf ./tmp/

echo "Making copy of a package"
mkdir -p tmp/pyless/
cp requirements.txt tmp/pyless/
cp -r pyless/ tmp/pyless/

echo "Running tests"
(source env/bin/activate ; cd tmp/pyless/pyless ; python manage.py test)
if [ $? != 0 ]; then
	echo "Tests failed"
	exit 1
fi

echo "Removing undesirables"
find ./tmp/pyless/pyless/ -type f -path '*/__pycache__/*' -delete
find ./tmp/pyless/pyless/ -type d -name "*__pycache__" -delete
find ./tmp/pyless/pyless/ -type f -name "*.sqlite3" -delete

echo "Building package"
rm -f p_pyless.tgz
(cd tmp ; tar -cvzf ../p_pyless.tgz pyless/)
