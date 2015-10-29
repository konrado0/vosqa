#!/bin/bash
#verify that we are called inside 
if [ ! -d "postgresconf" ]; then
    echo "Please call from inside tools directory"
fi

CURRENT_DIR=$(pwd)

MACHINE_TYPE=$(uname -m)
if [ "$MACHINE_TYPE" == 'x86_64' ]; then
	MACHINE='x86_64'
else
	MACHINE='i386'
fi

# update the local package index
sudo apt-get update

#install necessary Ubuntu packages
# postgres administration: pgadmin3 phppgadmin
sudo apt-get -y install build-essential python-dev vim mc meld openjdk-7-jdk curl postgresql libpq-dev gitg memcached libmemcached-dev libjpeg8 libjpeg8-dev zlib1g zlib1g-dev libfreetype6 libfreetype6-dev nginx pgadmin3 libpcre3 libpcre3-dev supervisor libxml2-dev libxslt1-dev yui-compressor
sudo apt-get -y install libtiff4 libtiff4-dev liblcms1 liblcms1-dev
sudo apt-get -y install google-chrome-stable

#Create links necessary for working PIL installation with pip
#if [ ! -f '/usr/lib/libz.so' ]; then
	sudo ln -s /usr/lib/$MACHINE-linux-gnu/libfreetype.so /usr/lib/
	sudo ln -s /usr/lib/$MACHINE-linux-gnu/libz.so /usr/lib/
	sudo ln -s /usr/lib/$MACHINE-linux-gnu/libjpeg.so /usr/lib/
	sudo ln -s /usr/lib/$MACHINE-linux-gnu/libtiff.so /usr/lib/
	sudo ln -s /usr/lib/$MACHINE-linux-gnu/liblcms.so /usr/lib
	#sudo ln -s /usr/include/freetype2 /usr/include/freetype
#fi

if [ "$1" = "-i" ]; then

	# Select current version of virtualenv:
	VERSION=1.11.4
	# Name your first "bootstrap" environment:
	INITIAL_ENV=py0
	# Options for your first environment:
	ENV_OPTS='--no-site-packages'
	# Set to whatever python interpreter you want for your first environment:
	PYTHON=$(which python)
	URL_BASE=https://pypi.python.org/packages/source/v/virtualenv
	CURRENT_DIR=$(pwd)

	# --- Configure postgres ----
	sudo -u postgres createuser -d -S -R dressbook 
	sudo -u postgres createdb osqa -O dressbook -E 'UTF8'
	sudo cp $CURRENT_DIR/postgresconf/* /etc/postgresql/9.1/main/ 
	sudo chown postgres:postgres /etc/postgresql/9.1/main/*
	sudo service postgresql restart

	# --- Virtualenv installation ---	
	mkdir ~/virtualenv
	cd ~/virtualenv
	echo "Downloading virtuaenv version $VERSION"
	curl -O $URL_BASE/virtualenv-$VERSION.tar.gz
	tar xzf virtualenv-$VERSION.tar.gz
	echo "Creating the first "bootstrap" environment $INITIAL_ENV."
	$PYTHON virtualenv-$VERSION/virtualenv.py $ENV_OPTS $INITIAL_ENV
	echo "Remove unnecessary files..."
	rm -rf virtualenv-$VERSION
	echo "Install virtualenv into the environment via its pip."
	$INITIAL_ENV/bin/pip install virtualenv-$VERSION.tar.gz

	# --- Create evnironment for osqa
	$INITIAL_ENV/bin/virtualenv osqa
	osqa/bin/pip install -r $CURRENT_DIR/../osqa/requirements.txt
	cd $CURRENT_DIR
else
	#update requirements
	~/virtualenv/osqa/bin/pip install --upgrade -r $CURRENT_DIR/../osqa/requirements.txt
fi
echo "Done"

