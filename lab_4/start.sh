# Get the directory the script resides it can be called from other directories
CURRENT_DIRECTORY=$(dirname $0)

python $CURRENT_DIRECTORY/server/server.py
find . -name '*.pyc' -delete
