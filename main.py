from code_generator.collector import collect_files
from code_generator.synth import generate_synth
from realisations.nodes.oscillators import SineOscillator
from realisations.nodes.tmp import OneSampleDelay

osc1 = SineOscillator()
osc1['frequency'] = 440

delay1 = OneSampleDelay()
delay1['input'] = osc1

osc2 = SineOscillator()
osc2['frequency'] = delay1

delay2 = OneSampleDelay()
delay2['input'] = osc2

osc3 = SineOscillator()
osc3['frequency'] = delay2

generate_synth([osc3])
collect_files()
