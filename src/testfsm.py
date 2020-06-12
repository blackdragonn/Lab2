import unittest
from fsm import *


class FsmTest(unittest.TestCase):
    def test_get_start(self):
        m = StateMachine()
        m.set_start("s0")
        self.assertEqual(m.start_state, 's0')

    def test_add_state(self):
        m = StateMachine()
        m.add_state("s0", "Junction A green,Junction B red")
        m.add_state("s1", "Junction A yellow,Junction B red")
        m.add_state("s2", "Junction A red,Junction B green")
        m.add_state("s3", "Junction A red,Junction B yellow")
        m.set_start("s0")
        self.assertEqual(m.state_action,{"s0":"Junction A green,Junction B red",
                                            "s1":"Junction A yellow,Junction B red",
                                            "s2": "Junction A red,Junction B green",
                                            "s3": "Junction A red,Junction B yellow"})

    def test_add_transition(self):
        clk1 = 4
        clk2 = 2
        m = StateMachine()
        m.add_state("s0", "Junction A green,Junction B red")
        m.add_state("s1", "Junction A yellow,Junction B red")
        m.add_state("s2", "Junction A red,Junction B green")
        m.add_state("s3", "Junction A red,Junction B yellow")
        m.set_start("s0")
        transition_function_1=lambda clk: (clk + 1, "s0") if clk < clk1 else (0, "s1")
        transition_function_2=lambda clk: (clk + 1, "s1") if clk < clk2 else (0, "s2")
        transition_function_3=lambda clk: (clk + 1, "s2") if clk < clk1 else (0, "s3")
        transition_function_4=lambda clk: (clk + 1, "s3") if clk < clk2 else (0, "s0")
        m.add_transition("s0", transition_function_1)
        m.add_transition("s1", transition_function_2)
        m.add_transition("s2", transition_function_3)
        m.add_transition("s3", transition_function_4)
        print(m.handlers)
        self.assertEqual(m.handlers['s0'],transition_function_1)
        self.assertEqual(m.handlers['s1'],transition_function_2)
        self.assertEqual(m.handlers['s2'],transition_function_3)
        self.assertEqual(m.handlers['s3'],transition_function_4)

    #Test traffic lights, green light time is 4 seconds, yellow light time is 2 seconds, red light time is 6 seconds,clk 15
    def test_rbg_right_fsm_run_1(self):
        clk1 = 4
        clk2 = 2
        m = StateMachine()
        m.add_state("s0","Junction A green,Junction B red")
        m.add_state("s1","Junction A yellow,Junction B red")
        m.add_state("s2","Junction A red,Junction B green")
        m.add_state("s3","Junction A red,Junction B yellow")
        m.set_start("s0")
        m.add_transition("s0",lambda clk: (clk+1,"s0") if clk<clk1 else (0,"s1"))
        m.add_transition("s1",lambda clk: (clk+1,"s1") if clk<clk2 else (0,"s2"))
        m.add_transition("s2",lambda clk: (clk+1,"s2") if clk<clk1 else (0,"s3"))
        m.add_transition("s3",lambda clk: (clk+1,"s3") if clk<clk2 else (0,"s0"))

        m.run_by_time(15)

        self.assertEqual(m.light_state_history, [
                (0, 'Junction A green,Junction B red'), 
                (1, 'Junction A green,Junction B red'), 
                (2, 'Junction A green,Junction B red'), 
                (3, 'Junction A green,Junction B red'), 
                (4, 'Junction A green,Junction B red'), 
                (5, 'Junction A green,Junction B red'), 
                (6, 'Junction A yellow,Junction B red'), 
                (7, 'Junction A yellow,Junction B red'), 
                (8, 'Junction A yellow,Junction B red'), 
                (9, 'Junction A red,Junction B green'), 
                (10, 'Junction A red,Junction B green'), 
                (11, 'Junction A red,Junction B green'), 
                (12, 'Junction A red,Junction B green'), 
                (13, 'Junction A red,Junction B green'), 
                (14, 'Junction A red,Junction B yellow'),
                (15, 'Junction A red,Junction B yellow')
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

    #Test traffic lights, green light time is 8 seconds, yellow light time is 3 seconds, red light time is 11 seconds,clk 25
    def test_rbg_right_fsm_run_2(self):
        clk1 = 8
        clk2 = 3
        m = StateMachine()
        m.add_state("s0","Junction A green,Junction B red")
        m.add_state("s1","Junction A yellow,Junction B red")
        m.add_state("s2","Junction A red,Junction B green")
        m.add_state("s3","Junction A red,Junction B yellow")
        m.set_start("s0")
        m.add_transition("s0",lambda clk: (clk+1,"s0") if clk<clk1 else (0,"s1"))
        m.add_transition("s1",lambda clk: (clk+1,"s1") if clk<clk2 else (0,"s2"))
        m.add_transition("s2",lambda clk: (clk+1,"s2") if clk<clk1 else (0,"s3"))
        m.add_transition("s3",lambda clk: (clk+1,"s3") if clk<clk2 else (0,"s0"))

        m.run_by_time(25)

        self.assertEqual(m.light_state_history, [
                (0, 'Junction A green,Junction B red'), 
                (1, 'Junction A green,Junction B red'), 
                (2, 'Junction A green,Junction B red'), 
                (3, 'Junction A green,Junction B red'), 
                (4, 'Junction A green,Junction B red'), 
                (5, 'Junction A green,Junction B red'), 
                (6, 'Junction A green,Junction B red'), 
                (7, 'Junction A green,Junction B red'), 
                (8, 'Junction A green,Junction B red'), 
                (9, 'Junction A green,Junction B red'), 
                (10, 'Junction A yellow,Junction B red'), 
                (11, 'Junction A yellow,Junction B red'), 
                (12, 'Junction A yellow,Junction B red'), 
                (13, 'Junction A yellow,Junction B red'), 
                (14, 'Junction A red,Junction B green'), 
                (15, 'Junction A red,Junction B green'), 
                (16, 'Junction A red,Junction B green'), 
                (17, 'Junction A red,Junction B green'), 
                (18, 'Junction A red,Junction B green'), 
                (19, 'Junction A red,Junction B green'), 
                (20, 'Junction A red,Junction B green'), 
                (21, 'Junction A red,Junction B green'), 
                (22, 'Junction A red,Junction B green'), 
                (23, 'Junction A red,Junction B yellow'), 
                (24, 'Junction A red,Junction B yellow'), 
                (25, 'Junction A red,Junction B yellow')
        ])

        self.assertListEqual(m.transition_history, [
                (1, 's0', 's0'), 
                (2, 's0', 's0'), 
                (3, 's0', 's0'), 
                (4, 's0', 's0'), 
                (5, 's0', 's0'), 
                (6, 's0', 's0'), 
                (7, 's0', 's0'), 
                (8, 's0', 's0'), 
                (9, 's0', 's1'), 
                (10, 's1', 's1'), 
                (11, 's1', 's1'), 
                (12, 's1', 's1'), 
                (13, 's1', 's2'), 
                (14, 's2', 's2'), 
                (15, 's2', 's2'), 
                (16, 's2', 's2'), 
                (17, 's2', 's2'), 
                (18, 's2', 's2'), 
                (19, 's2', 's2'), 
                (20, 's2', 's2'), 
                (21, 's2', 's2'), 
                (22, 's2', 's3'), 
                (23, 's3', 's3'), 
                (24, 's3', 's3'), 
                (25, 's3', 's3')
        ])


    #Test Sequence "1101" detection
    def test_sequence_detection(self):
        m = StateMachine()
        m.add_state("s0","Initial state")
        m.add_state("s1","Sequence 1 detected")
        m.add_state("s2","Sequence 11 detected")
        m.add_state("s3","Sequence 110 detected")
        m.add_state("s4","Sequence 1101 detected")
        m.set_start("s0")
        m.add_transition("s0",lambda a: "s1" if a==1 else "s0")
        m.add_transition("s1",lambda a: "s2" if a==1 else "s0")
        m.add_transition("s2",lambda a: "s3" if a==0 else "s2")
        m.add_transition("s3",lambda a: "s4" if a==1 else "s0")
        m.add_transition("s4",lambda a: "s1" if a==1 else "s0")

        m.run_by_event([1,0,1,0,1,1,0,1])
        self.assertListEqual(m.transition_history,[
        (1, 'Input event:1', 's0', 's1'), 
        (2, 'Input event:0', 's1', 's0'), 
        (3, 'Input event:1', 's0', 's1'), 
        (4, 'Input event:0', 's1', 's0'), 
        (5, 'Input event:1', 's0', 's1'), 
        (6, 'Input event:1', 's1', 's2'), 
        (7, 'Input event:0', 's2', 's3'), 
        (8, 'Input event:1', 's3', 's4')]
        )


    #Test elevator fsm
    def test_elevator(self):
        m = StateMachine()
        m.add_state("StateStopping","Stopped state, the door is closed")
        m.add_state("StateGoingUp","The Elevator is rising")
        m.add_state("StateGoingDown","The elevator is descending")
        m.add_state("StateOpened","Elevator opens the door")
        m.add_state("StateWarning","Overload alarm status")

        m.set_start("StateStopping")

        m.add_transition("StateStopping",lambda a: "StateOpened" if a=='EVENT_OPEN' else ('StateGoingUp' if a=='EVENT_UP' else ('StateGoingDown' if a=='EVENT_DOWN' else 'StateStopping' )))
        m.add_transition("StateOpened",lambda a: "StateStopping" if a=='EVENT_CLOSE' else ('StateWarning' if a=='EVENT_WARN' else 'StateOpened'))
        m.add_transition("StateGoingUp",lambda a: "StateStopping" if a=='EVENT_STOP' else 'StateGoingUp')
        m.add_transition("StateGoingDown",lambda a: "StateStopping" if a=='EVENT_STOP' else "StateGoingDown")
        m.add_transition("StateWarning",lambda a: "StateOpened" if a=='EVENT_DELWARN' else "StateWarning")

        m.run_by_event(['EVENT_OPEN','EVENT_CLOSE','EVENT_UP','EVENT_STOP','EVENT_OPEN','EVENT_WARN','EVENT_DELWARN'])
        self.assertListEqual(m.transition_history,[
            (1, 'Input event:EVENT_OPEN', 'StateStopping', 'StateOpened'), 
            (2, 'Input event:EVENT_CLOSE', 'StateOpened', 'StateStopping'), 
            (3, 'Input event:EVENT_UP', 'StateStopping', 'StateGoingUp'), 
            (4, 'Input event:EVENT_STOP', 'StateGoingUp', 'StateStopping'), 
            (5, 'Input event:EVENT_OPEN', 'StateStopping', 'StateOpened'), 
            (6, 'Input event:EVENT_WARN', 'StateOpened', 'StateWarning'), 
            (7, 'Input event:EVENT_DELWARN', 'StateWarning', 'StateOpened')
        ])

    #The parameters type of param_check_test(a,b,c) should be (int,str,list)
    def test_param_check(self):
        m = StateMachine()
        self.assertRaises(TypeError,m.add_state,1,"test")
        self.assertRaises(TypeError,m.set_start,1)
        self.assertRaises(TypeError,param_check_test,1,"test",1)

if __name__ == '__main__':
    unittest.main()
