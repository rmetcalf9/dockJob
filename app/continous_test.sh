until ack -f --python | entr -d nosetests --rednose ./test; do sleep 1; done
