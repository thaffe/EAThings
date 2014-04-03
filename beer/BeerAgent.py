from core.AnnIndividual import AnnIndividual
from core.GeneFloat import GeneFloatSource


class BeerAgent(AnnIndividual):

    source = [
        {"name": "s0"},
        {"name": "s1"},
        {"name": "s2"},
        {"name": "s3"},
        {"name": "s4"},
        {"name": "h0", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0}},
        {"name": "h1", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0, "h0": 0}},
        # {"name": "h2", "weights": {"s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0, "h0": 0, "h1": 0}},
        {"name": "o0", "weights": {"h0": 0, "h1": 0}}, #, "h2": 0}},
        {"name": "o1", "weights": {"h0": 0, "h1": 0, "o0": 0}} #"h1": 0, "h2": 0, "o0": 0}}
    ]

    source_appends = [
        {"name": "h0", "weights": {"h1": 0}}, #"h2": 0}},
        # {"name": "h1", "weights": {"h2": 0}},
        {"name": "o0", "weights": {"o1": 0}}
    ]

    tau_source = GeneFloatSource(1, 2, True)
    g_source = GeneFloatSource(1, 5, False)
    bias_source = GeneFloatSource(-10, 10, False)
    weight_source = GeneFloatSource(-5, 5, False)


    def calculate_fitness(self):
        pass

    def phenotype_str(self):
        return "I'm a BeerAgent!"

    def getmove(self, shadows, step):
        for i in xrange(5):
            n = self.ann.neurons["s" + str(i)]
            n.output = shadows[i]
            n.step_counter = step

        right = self.ann.neurons["o0"].update(step)
        left = self.ann.neurons["o1"].update(step)
        return max(-4, min(4, int(round(left-right)*10)))

    def test_ann(self, shadows, step):
        for i in xrange(5):
            n = self.ann.neurons["s" + str(i)]
            n.output = shadows[i]
            n.step_counter = step

        right = self.ann.neurons["o0"].update(step)
        left = self.ann.neurons["o1"].update(step)

        return left, right

    def do_tests_on_ann(self):

        self.ann.reset()
        shadows = [True, True, True, True, True]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        print ""
        self.ann.reset()
        shadows = [True, True, True, True, False]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [True, True, True, False, False]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [True, True, False, False, False]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [True, False, False, False, False]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [False, False, False, False, False]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        print ""
        self.ann.reset()
        shadows = [False, False, False, False, True]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [False, False, False, True, True]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [False, False, True, True, True]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        self.ann.reset()
        shadows = [False, True, True, True, True]
        left, right = self.test_ann(shadows, 1)
        print "shadows:", shadows, "o1:", left, "o2:", right

        print ""

        print ""
        self.ann.reset()
        for i in xrange(5):
            self.test_ann([False, False, False, False, False], i)
        self.test_ann([True, True, False, False, False], 5)
        print "event:", "sudden shadow left", "o1:", left, "o2:", right

        print ""
        self.ann.reset()
        for i in xrange(5):
            self.test_ann([False, False, False, False, False], i)
        left, right = self.test_ann([False, False, False, True, True], 5)
        print "event:", "sudden shadow right", "o1:", left, "o2:", right

        print ""
        self.ann.reset()
        for i in xrange(5):
            self.test_ann([False, False, False, False, False], i)
        left, right = self.test_ann([False, True, True, True, False], 5)
        print "event:", "sudden shadow middle", "o1:", left, "o2:", right