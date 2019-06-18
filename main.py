#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import nest
from glob import glob
from brian2 import *
from brian2hears import *

nbr_center_frequencies = 32

eareqs = '''
dv/dt = (I-v)/(1*ms)+0.2*xi*(2/(1*ms))**.5 : 1 (unless refractory)
I : 1
'''
edict = {"I_e": 180.0, "tau_m": 20.0, 't_ref': 15.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
idict = {"I_e": 300.0}
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha", params=idict)
nest.SetDefaults("static_synapse",{"weight": 150.0})

def collectSpikes(time, neuron, collect):
    for t, n in zip(time, neuron):
        collect[n].append(round(t.item()*1000, 1))

DB = "ODB"
FILES = glob('Datasets/' + DB + '/sounds/*.wav')

ExcReceiveBand = nest.Create("exc_iaf_psc_alpha", int(nbr_center_frequencies/4))
LocInh = nest.Create("inh_iaf_psc_alpha", int(nbr_center_frequencies/4))
Detection = nest.Create("exc_iaf_psc_alpha", 1)
BandToPoisson = nest.Create("spike_generator", nbr_center_frequencies)
meter = nest.Create("voltmeter", 1)
conn_dict = {'rule': 'fixed_indegree', 'indegree': 5}
nest.Connect(BandToPoisson, ExcReceiveBand, conn_dict)
nest.Connect(ExcReceiveBand, LocInh, "one_to_one", {'weight': 180, 'delay': 1.0})
nest.Connect(LocInh, ExcReceiveBand, "one_to_one", {'weight': -200, 'delay': 1.0})
nest.Connect(ExcReceiveBand, Detection, {'rule': 'fixed_total_number', 'N': 8}, {'weight': 9, 'delay': 0.1})
nest.Connect(meter, Detection)

for f in FILES:
    print("Parse: " + f)
    sound = loadsound(f)
    sound.level = 60*dB

    #center frequencies with a spacing following an ERB scale
    center_frequencies = erbspace(20*Hz, 16000*Hz, nbr_center_frequencies)
    gfb = Gammatone(sound, center_frequencies)

    ihc = FunctionFilterbank(gfb, lambda x: 3*clip(x, 0, Inf)**(1.0/3.0))

    cochlea = FilterbankGroup(ihc, 'I', eareqs, reset='v=0', threshold='v>1', refractory=5*ms, method='euler')
    M = SpikeMonitor(cochlea)

    run(sound.duration, report="stdout")

#-------------------------------------
    nest.ResetNetwork()
    collect = [ [] for i in range(nbr_center_frequencies) ]
    collectSpikes(M.t, M.i, collect)
    print(collect)

    count = 0
    for machine in BandToPoisson:
        nest.SetStatus([machine], {"spike_times": (collect[count])})
        count = count+1

    nest.SetStatus(meter, {"withtime":True})
    print("Sim: " + str(round(sound.duration.item())*1000.0))
    nest.Simulate(round(sound.duration.item())*1000.0)

    dmm0 = nest.GetStatus(meter)[0]
    Vms0 = dmm0["events"]["V_m"]
    ts0 = dmm0["events"]["times"]
    plt.figure(0)
    plt.plot(ts0, Vms0)
    '''
    dmm1 = nest.GetStatus(meter)[1]
    Vms1 = dmm1["events"]["V_m"]
    ts1 = dmm1["events"]["times"]
    plt.figure(1)
    plt.plot(ts1, Vms1)
    dmm2 = nest.GetStatus(meter)[2]
    Vms2 = dmm2["events"]["V_m"]
    ts2 = dmm2["events"]["times"]
    plt.figure(2)
    plt.plot(ts2, Vms2)
    dmm3 = nest.GetStatus(meter)[3]
    Vms3 = dmm3["events"]["V_m"]
    ts3 = dmm3["events"]["times"]
    plt.figure(3)
    plt.plot(ts3, Vms3)
    dmm4 = nest.GetStatus(meter)[4]
    Vms4 = dmm4["events"]["V_m"]
    ts4 = dmm4["events"]["times"]
    plt.figure(4)
    plt.plot(ts4, Vms4)
    dmm5 = nest.GetStatus(meter)[5]
    Vms5 = dmm5["events"]["V_m"]
    ts5 = dmm5["events"]["times"]
    plt.figure(5)
    plt.plot(ts5, Vms5)
    dmm6 = nest.GetStatus(meter)[6]
    Vms6 = dmm6["events"]["V_m"]
    ts6 = dmm6["events"]["times"]
    plt.figure(6)
    plt.plot(ts6, Vms6)
    dmm7 = nest.GetStatus(meter)[7]
    Vms7 = dmm7["events"]["V_m"]
    ts7 = dmm7["events"]["times"]
    plt.figure(7)
    plt.plot(ts7, Vms7)
    '''
    plt.show()
#with open(f.replace('/sounds/','/predictions/').replace('.wav','.txt'), 'a') as outfile:
#    outfile.write('Hello\n')
