from ann.ANN import *
from beer.BeerAgent import BeerAgent
test = {'s0': {'tau': 1.988571454601034, 'bias': -2.244161235601923, 'g': 3.932027195588722}, 's3': {'tau': 1.0, 'bias': -1.408723751838008, 'g': 3.5308372949290234}, 's2': {'tau': 1.6605502064934443, 'bias': -8.934511197452917, 'g': 3.8778827896795027}, 's1': {'tau': 1.0, 'bias': -9.846381308105592, 'g': 2.6061419297570434}, 'h1': {'tau': 1.015627935615344, 'g': 2.5177744441694285, 's3': -2.811366359852115, 's2': -6.206259491762082, 's1': -6.934009945638012, 's0': 1.9828191104209667, 's4': -8.301339775602505, 'bias': 0, 'h0': 10.0}, 's4': {'tau': 1.909040717433604, 'bias': -10.0, 'g': 4.968817524481219}, 'h0': {'tau': 1.4454516705298184, 's0': 4.261323462408344, 'g': 4.908992798324103, 's3': -2.0944636572891295, 's2': -5.798317857548165, 's1': 0.8815238974979644, 'h1': -10.0, 's4': 10, 'bias': -4.825933337282132}, 'o1': {'tau': 1.0015347955427532, 'g': 4.196254969962199, 'h0': 3.370449644215906, 'h1': 6.044221206140363, 'bias': -0.7321309369955775, 'o0': 3.1099483929105958}, 'o0': {'tau': 1.4416210697131109, 'g': 1.6147841850004412, 'h0': -4.648085840785148, 'h1': 6.9369105907578605, 'bias': -8.250303667519583, 'o1': -8.973884682275566}}

ann = ANN(BeerAgent.source)
for neuron in BeerAgent.source_appends:
    for key, weight in neuron["weights"].items():
        ann.add_input(neuron["name"], key, weight, True)


for key, node in test.items():
    for t,n in node.items():
        neu = ann.neurons[key]
        if t == 'tau':
            neu.tau = n
        elif t == 'bias':
            neu.bias = n
        elif t == 'g':
            neu.g = n
        else:
            neu.inputs[t].weight = n


for i in xrange(5):
    ann.neurons['s'+str(i)].output = 1

print ann.neurons['o0'].update(0), ann.neurons['o1'].update(0)