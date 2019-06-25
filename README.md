# Spiking Neural Network in Music Information Retrieval
This project is a demo of how modern bio-inspired spiking neural network(SNN) can be integrated into music information retrieval(MIR) applications. The project incorporates two popular SNN simulator: Brian2 and NEST to demonstrate SNN can detect onsets of notes in a music clip. The author is Alex Huang-Yu Yao, please contact <cktfg18nthu@gapp.nthu.edu.tw>.

## Prerequisites
### onset predictions
* [Python3](https://www.python.org/)
* [Numpy](https://www.numpy.org/)
* [Brian2](https://brian2.readthedocs.io/en/stable/)
* [Brian2hears](https://brian2hears.readthedocs.io/en/stable/)
* [NEST](https://nest-simulator.readthedocs.io/en/latest/index.html)
* [ODB dataset](https://grfia.dlsi.ua.es/cm/worklines/pertusa/onset/)
* Optional -- [Matplotlib](https://matplotlib.org/)
### evaluation
* [gcc compiler](https://gcc.gnu.org/)
* [tee](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/tee.html)

## Repository contents
* `SNNinMIR.pdf` is the detailed technical description file of the project.
* `main.py` is the core program for onset detection.
* `network.py` is an SNN only simulation routine without music input for network dynamics evaluation.
* `evaluation.sh` is a bash script to execute the evaluation tool in ODB dataset.
* `LICENSE`: the project is under MPLv2.
* `README.md` is what you are reading.

## How to run the program
1. Clone or download this repository and download the ODB dataset.
2. Switch to the top level to this repository, i.e. `cd /path/to/SNN-in-MIR`.
3. Create a dirctory to put dataset in. `mkdir Datasets` and move all the file below the ODB and evaluator directories under `Datasets`. It should look like this: `SNN-in-MIR/Datasets/[ODB/evaluator]/`.
4. Execute `python main.py` to predict all onset points in the ODB dataset.
5. Run `./evaluation.sh` to obtain the evaluation results to the predictions. The results will be saved under the evaluator directory.
___Note: The programs are developed and tested on Arch Linux. Users of other OS may need to modify some instructions in the files.___