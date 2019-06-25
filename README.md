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
* Optional(for additional visualization) -- [Matplotlib](https://matplotlib.org/)
### evaluation
* [gcc compiler](https://gcc.gnu.org/)
* [tee](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/tee.html)

## Repository contents
* `SNNinMIR.pdf` is the detailed technical description file of the project.
* `run.sh` is the 1-step easy-running script.
* `main.py` is the core program for onset detection.
* `network.py` is an SNN only simulation routine without music input for network dynamics evaluation.
* `LICENSE`: the project is under MPLv2.
* `README.md` is what you are reading.
* `mir-term.odp` is the in-class presentation slides on 2019/06/18. Actually, all the contens are included in `SNNinMIR.pdf`.

## How to run the program
1. Clone or download this repository and download the ODB dataset.
2. Switch to the top level of this repository, i.e. `cd /path/to/SNN-in-MIR`.
3. Create a dirctory to put dataset in. `mkdir Datasets` and move all the file below the `ODB` and `evaluator` directories under `Datasets`. It should look like this: `SNN-in-MIR/Datasets/[ODB/evaluator]/...`.
4. Execute `run.sh` to predict all onset points and obtain the evaluation results in the ODB dataset. The results will be saved under the top-level directory. If you find that you cannot execute the script, you should try `sudo chmod +x run.sh`.

___Note: The programs are developed and tested on Arch Linux. Non-linux users may need to modify some instructions in the source codes or operate in a virtual machine.___