set -x
rm *.txt
echo "a test file" > a.txt
echo "line 2 of a test file" >> a.txt
echo "line 3 of a test file" >> a.txt
echo "line 4 of a test file" >> a.txt
echo "line 5 of a test file" >> a.txt
echo "exit" >> a.txt
cat a.txt | python3 ../pipes/pipe.py processor pipes.processors.passthrough.PassThrough input stream stdin output stream stdout > b.txt
diff a.txt b.txt
echo "PIPES THROUGH RABBITMQ"
python3 ../pipes/pipe.py processor pipes.processors.passthrough.PassThrough input stream file a.txt output rabbitmq localhost qtest
python3 ../pipes/pipe.py processor pipes.processors.passthrough.PassThrough input rabbitmq localhost qtest output stream stdout
echo "TEST COMPLETE"
