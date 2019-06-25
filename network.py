# This file is for network behavior observation.
# Author: Huang-Yu Yao
import nest
import numpy as np
import matplotlib.pylab as plt
# Number of input Gammatone bands
bands = 32
# Neuronal parameters
edict = {"I_e": 100.0, "tau_m": 20.0}
nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha", params=edict)
idict = {"I_e": 0.0}
nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha", params=idict)
nest.SetDefaults("static_synapse",{"weight": 150.0})
# Create neurons and meters
BandSpikeGen = nest.Create("poisson_generator", bands)
nest.SetStatus(BandSpikeGen, {"rate": 50.0})
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
# Start simulation (ms)
nest.Simulate(5000.0)
# Plot membrane potential and spike events of Detection neuron
plt.figure(1)
plt.subplot(2, 1, 1)
dmm = nest.GetStatus(Vmeter)[0]
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
