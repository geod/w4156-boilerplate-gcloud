#!/bin/bash

touch tmp_test.json
echo -n "{\"id\": \"1\", \"text\": \"" >> tmp_test.json
cat textrank_input.txt >> tmp_test.json
echo "\"}" >> tmp_test.json

python3 stage1.py tmp_test.json > out1.json
python3 stage2.py out1.json > out2.json

mv out2.json result.json
rm out1.json
rm graph.dot

rm tmp_test.json

python3 stage3.py

rm result.json
