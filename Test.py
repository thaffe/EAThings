from ann.ANN import *
from beer.BeerAgent import BeerAgent

def test_ann(shadows, step):
    global ann
    for i in xrange(5):
        n = ann.neurons["s" + str(i)]
        n.output = shadows[i]
        n.step_counter = step

    right = ann.neurons["o0"].update(step)
    left = ann.neurons["o1"].update(step)

    return left, right
test = {'s0': {'tau': 1.592686147215389, 'bias': -2.615998446020173, 'g': 4.064259823298805}, 's3': {'tau': 2.0, 'bias': -9.596911713770295, 'g': 2.699219833009929}, 's2': {'tau': 2.0, 'bias': -7.9381838205981925, 'g': 1.196180415897641}, 's1': {'tau': 1.7131650362733641, 'bias': -9.800554266312117, 'g': 5}, 'h1': {'tau': 1.4759850492782784, 'g': 4.169964788304448, 's3': 10, 's2': -7.597575378784047, 's1': -7.30851842034613, 's0': -5.515947610513402, 's4': 10, 'bias': 0, 'h0': -9.161215598682354}, 's4': {'tau': 1.719469269868766, 'bias': -10, 'g': 1.5148042062097178}, 'h0': {'tau': 1.9805457921140477, 's0': 3.8498836747822374, 'g': 1.1918849794755142, 's3': 0.19606976014775368, 's2': 1.2234104157931345, 's1': -3.9816290689941063, 'h1': -1.752762947517268, 's4': 7.843733074806298, 'bias': -6.082985820301836}, 'o1': {'tau': 1.1177444179110503, 'g': 4.156539205282791, 'h0': 0.5183605142731278, 'h1': 9.884145727513904, 'bias': -3.094239221093069, 'o0': -10}, 'o0': {'tau': 1.5704922925516338, 'g': 4.8005459803723385, 'h0': 10.0, 'h1': -5.936363488987634, 'bias': -2.338789992756717, 'o1': -5.317834057912171}}

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



print ann.neurons['o0'].update(0), ann.neurons['o1'].update(1)


ann.reset()
shadows = [True, True, True, True, True]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

print ""
ann.reset()
shadows = [True, True, True, True, False]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [True, True, True, False, False]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [True, True, False, False, False]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [True, False, False, False, False]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [False, False, False, False, False]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

print ""
ann.reset()
shadows = [False, False, False, False, True]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [False, False, False, True, True]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [False, False, True, True, True]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

ann.reset()
shadows = [False, True, True, True, True]
left, right = test_ann(shadows, 1)
print "shadows:", shadows, "o1:", left, "o2:", right

print ""

print ""
ann.reset()
for i in xrange(5):
    test_ann([False, False, False, False, False], i)
test_ann([True, True, False, False, False], 5)
print "event:", "sudden shadow left", "o1:", left, "o2:", right

print ""
ann.reset()
for i in xrange(5):
    test_ann([False, False, False, False, False], i)
left, right = test_ann([False, False, False, True, True], 5)
print "event:", "sudden shadow right", "o1:", left, "o2:", right

print ""
ann.reset()
for i in xrange(5):
    test_ann([False, False, False, False, False], i)
left, right = test_ann([False, True, True, True, False], 5)
print "event:", "sudden shadow middle", "o1:", left, "o2:", right