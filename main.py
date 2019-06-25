#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import nest
from glob import glob
from brian2 import *
from brian2hears import *

def collectSpikes(time, neuron, collect):
    for t, n in zip(time, neuron):
        collect[n].append(round(t.item()*1000, 1))

bands = 32
DB = "ODB"
FILES = glob('Datasets/' + DB + '/sounds/*.wav')

# Brian2 neuronal parameters
eareqs = '''
dv/dt = (I-v)/(1*ms)+0.2*xi*(2/(1*ms))**.5 : 1 (unless refractory)
I : 1
'''
# center frequencies with a spacing following an ERB scale
center_frequencies = erbspace(20*Hz, 16000*Hz, bands)
# NEST neuronal parameters
edict = {"I_e": 180.0, "tau_m": 20.0, 't_ref': 15.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
idict = {"I_e": 300.0}
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha", params=idict)
nest.SetDefaults("static_synapse",{"weight": 150.0})
# Create neurons and meters
BandSpikeGen = nest.Create("spike_generator", bands)
ExcReceiveBand = nest.Create("exc_iaf_psc_alpha", int(bands/4))
LocInh = nest.Create("inh_iaf_psc_alpha", int(bands/4))
Detection = nest.Create("exc_iaf_psc_alpha", 1)
Vmeter = nest.Create("voltmeter", params={"withtime": True})
Smeter = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
# Connect neurons and meters
conn_dict = {"rule": "fixed_indegree", "indegree": 5}
nest.Connect(BandSpikeGen, ExcReceiveBand, conn_dict)
nest.Connect(ExcReceiveBand, LocInh, "one_to_one", {"weight": 180, "delay": 1.0})
nest.Connect(LocInh, ExcReceiveBand, "one_to_one", {"weight": -200, "delay": 1.0})
nest.Connect(ExcReceiveBand, Detection, {"rule": "fixed_total_number", "N": bands}, {"weight": 9, "delay": 0.1})
nest.Connect(Vmeter, Detection)
nest.Connect(Detection, Smeter)

for f in FILES:
    print("Parse: " + f)
    sound = loadsound(f)
    sound.level = 60*dB
    print("Brian2hears: Gammatone filtering...")
    gfb = Gammatone(sound, center_frequencies)
    print("Brian2: Spike generation...")
    ihc = FunctionFilterbank(gfb, lambda x: 3*clip(x, 0, Inf)**(1.0/3.0))
    cochlea = FilterbankGroup(ihc, 'I', eareqs, reset='v=0', threshold='v>1', refractory=5*ms, method='euler')
    auditoryNerve = SpikeMonitor(cochlea)
    auditoryNerve.invalidates_magic_network = False
    # Run Brian2 simulation
    run(sound.duration, report="stdout")

####--------------------------------------------------------
    print("NEST: Onset detection network...")
    nest.ResetNetwork()
    collect = [ [] for i in range(bands) ]
    collectSpikes(auditoryNerve.t, auditoryNerve.i, collect)
# debug here: print what spikegen really does
    count = 0
    for machine in BandSpikeGen:
        nest.SetStatus([machine], {"spike_times": (collect[count])})
        count = count+1

    print("Sim: " + str(round(sound.duration.item())*1000.0))
    # Run NEST simulation
    nest.Simulate(round(sound.duration.item())*1000.0)

    # Plot membrane potential and spike events of Detection neuron
    plt.figure(1)
    plt.subplot(2, 1, 1)
    dmm = nest.GetStatus(Vmeter)[0]
    print(dmm)
    Vms = dmm["events"]["V_m"]
    ts = dmm["events"]["times"]
    plt.ylabel("Membrane potential (mV)")
    plt.plot(ts, Vms)
    plt.subplot(2, 1, 2)
    dSD = nest.GetStatus(Smeter, keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.plot(ts, evs, 'k.')
    plt.show()

    # Write spike timing(onset timing) into file
    with open(f.replace('/sounds/','/predictions/').replace('.wav','.txt'), 'w') as outfile:
        for spike in dSD["times"]:
            outfile.write(str(round(spike/1000.0, 4)) + '\n')
