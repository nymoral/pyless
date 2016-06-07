#! /bin/bash

back_up=".backup/`date +"%Y_%m_%d_%H_%M_%S"`/"

mkdir -p "$back_up"
mv pyless "$back_up"

tar -xvf p_pyless.tgz

if [ -f "settings.py" ]; then
	rm -f pyless/pyless/pyless/settings.py
	ln settings.py pyless/pyless/pyless/settings.py
fi

source env/bin/activate
pip install --upgrade -r pyless/requirements.txt
(cd pyless/pyless ; python manage.py migrate ; python manage.py collectstatic ; python manage.py test)
deactivate

sudo systemctl restart gunicorn.service
