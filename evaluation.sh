#!/bin/bash

cd Datasets/ODB/evaluator
if test ! -e eval.out
then
	g++ -o eval.out evaluator_onsets.cpp
fi

for gtfile in ../ground-truth/*.txt; do
	prfile="${gtfile/ground-truth/predictions}"
	./eval.out "$gtfile" "$prefile" 2>&1 | tee results.txt
done
