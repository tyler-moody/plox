while true; do ls ./* | entr -pd /usr/bin/python3 -m unittest discover -p "*_test.py"; done
