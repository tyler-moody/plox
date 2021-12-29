while true; do ls ./* | entr -pd python3 -m unittest discover -p "*_test.py"; done
