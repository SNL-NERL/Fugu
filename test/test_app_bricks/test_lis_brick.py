#THIS WORKS!~ Ran 4 tests in 1.003s  OK


import unittest
import numpy as np

import os
import sys
import unittest

# from Fugu.test.test_stochastic_bricks.test_threshold_brick import ThresholdBrickTests

parentdir = os.path.abspath('../../')
sys.path.append(parentdir)

import Fugu.fugu.bricks as BRICKS
from Fugu.fugu.backends import snn_Backend
from Fugu.fugu.scaffold import Scaffold
from Fugu.test.base import BrickTest



class LISBrickTests(BrickTest):
    # Base class functions
    def build_scaffold(self, input_values):
        scaffold = Scaffold()

        spike_sequence = self.convert_input(input_values)
        input_brick = BRICKS.Vector_Input(spike_sequence, coding='Raster', name='LISInput', time_dimension=True)
        lis_brick = BRICKS.LIS(len(input_values), name='LIS')

        scaffold.add_brick(input_brick, 'input')
        scaffold.add_brick(lis_brick, input_nodes=[(0, 0)], output=True)

        scaffold.lay_bricks()

        return scaffold

    def calculate_max_timesteps(self, input_values):
        return max(input_values) * len(input_values)

    def check_spike_output(self, spikes, expected, scaffold):
        graph_names = list(scaffold.graph.nodes.data('name'))
        answer = 0
        for row in spikes.itertuples():
            neuron_name = graph_names[int(row.neuron_number)][0]
            if "Main" in neuron_name:
                level = int(neuron_name.split("_")[1])
                if level > answer:
                    answer = level

        self.assertEqual(expected, answer)

    def convert_input(self, sequence):
        num_in_sequence = len(sequence)
        max_time = max(sequence)
        spike_times = [[0] * (max_time + 1) for i in range(num_in_sequence)]
        for i, time in enumerate(sequence):
            spike_times[i][time] = 1
        return spike_times

    # Tests
    def test_lis_strictly_increasing(self):
        sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.basic_test(sequence, 10)

    def test_lis_strictly_decreasing(self):
        sequence = [10, 10, 5, 5, 1]
        self.basic_test(sequence, 1)

    def test_lis_general_short_sequence(self):
        sequence = [5, 10, 2, 3, 4]
        self.basic_test(sequence, 3)

    def test_lis_long_sequence(self):
        sequence = [1, 4, 8, 6, 2, 7, 19, 13, 14]
        self.basic_test(sequence, 6)


class SnnLISTests(LISBrickTests, unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.backend = snn_Backend()


# class DsLISTests(LISBrickTests, unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.backend = ds_Backend()

#
# class PynnSpinnakerLISTests(LISBrickTests, unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.backend = pynn_Backend()
#         self.backend_args['backend'] = 'spinnaker'
#
#
# class PynnBrianLISTests(LISBrickTests, unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.backend = pynn_Backend()
#         self.backend_args['backend'] = 'brian'
