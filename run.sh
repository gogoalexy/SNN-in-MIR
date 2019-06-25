#!/bin/bash

mkdir -p Datasets/ODB/predictions

for SoundClip in Datasets/ODB/sounds/*.wav; do
	echo "Parse: ${SoundClip}"
	python main.py ${SoundClip}
done

cd Datasets/evaluator
if test ! -e eval.out
then
	g++ -o eval.out evaluator_onsets.cpp
fi

if test -e ../../results.txt
then
	rm ../../results.txt
fi
for gtfile in ../ODB/ground-truth/*.txt; do
	prfile="${gtfile/ground-truth/predictions}"
	echo "File: ${prfile}"
	echo "File: ${prfile}" >> ../../results.txt
	./eval.out "$gtfile" "$prfile" 2>&1 | tee -a ../../results.txt
done
