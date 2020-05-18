import unittest
from Rgb_light import *

class FsmTest(unittest.TestCase):
    def test_rgbLight(self):
        m = StateMachine()
        m.set_start("s0")
        m.add_state("s0","A green,B red")
        m.add_state("s1","A yellow,B red")
        m.add_state("s2","A red,B green")
        m.add_state("s3","A red,B yellow")

        m.add_transition("s0",lambda clk: (clk+1,"s0") if clk<4 else (clk and 0,"s1"))
        m.add_transition("s1",lambda clk: (clk+1,"s1") if clk<2 else (clk and 0,"s2"))
        m.add_transition("s2",lambda clk: (clk+1,"s2") if clk<4 else (clk and 0,"s3"))
        m.add_transition("s3",lambda clk: (clk+1,"s3") if clk<2 else (clk and 0,"s0"))

        m.run(15)

        self.assertEqual(m.state_history, [
                (0, 's0'), 
                (1, 's0'), 
                (2, 's0'), 
                (3, 's0'), 
                (4, 's0'), 
                (5, 's0'), 
                (6, 's1'), 
                (7, 's1'), 
                (8, 's1'), 
                (9, 's2'), 
                (10, 's2'), 
                (11, 's2'), 
                (12, 's2'), 
                (13, 's2'), 
                (14, 's3'), 
                (15, 's3')
        ])
        self.assertListEqual(m.transition_history, [
                (1, 's0', 's0'), 
                (2, 's0', 's0'), 
                (3, 's0', 's0'), 
                (4, 's0', 's0'), 
                (5, 's0', 's1'), 
                (6, 's1', 's1'), 
                (7, 's1', 's1'), 
                (8, 's1', 's2'), 
                (9, 's2', 's2'), 
                (10, 's2', 's2'), 
                (11, 's2', 's2'), 
                (12, 's2', 's2'), 
                (13, 's2', 's3'), 
                (14, 's3', 's3'), 
                (15, 's3', 's3')
        ])

if __name__ == '__main__':
    unittest.main()