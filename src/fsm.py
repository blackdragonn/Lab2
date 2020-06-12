import graphviz
from inspect import signature
from functools import wraps

 
def param_check(*type_args, **type_kwargs):
    def decorate(func):
        sig = signature(func)
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments
 
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate

class StateMachine:
    def __init__(self): 
        self.handlers = {}        # State transfer function dictionary
        self.start_state = None    # Initial state
        self.state=[]
        self.state_action={}       # Explain what this state is doing
        self.clk=0                # clock
        self.light_state_history = []   # State light logic history at each clock
        self.transition_history = []  #Each state transfer record

    #Set the starting state
    @param_check(object,str)
    def set_start(self, state):
        self.start_state = state

    #Add status
    @param_check(object,str,str)
    def add_state(self, name, action):
        self.state_action[name]=action
        self.state.append(name)

    #Set state transition function
    @param_check(object,str,object)
    def add_transition(self,state,function):
        self.handlers[state] = function  #Set state transition for each state
        return function

    #Use time to drive fsm
    @param_check(object,int)
    def run_by_time(self, clk_n):
        handler = self.handlers[self.start_state]
        current_state=self.start_state
        all_clk=clk_n
        self.light_state_history.append((self.clk,self.state_action[self.start_state]))
        # Start processing from the Start state
        while clk_n>0:
            self.light_state_history.append((all_clk-clk_n+1,self.state_action[current_state])) #Log the logic of traffic lights
            (clk_new, next_state) = handler(self.clk)     # Transform to a new state after a state transition function
            self.clk=clk_new
            self.transition_history.append((all_clk-clk_n+1,current_state,next_state)) #Log the logic of fsm transition
            handler = self.handlers[next_state]
            current_state=next_state
            clk_n-=1

    #Use events to drive fsm
    @param_check(object,list)
    def run_by_event(self, event_lst):
        handler = self.handlers[self.start_state]
        current_state=self.start_state
        t=len(event_lst)
        i=0
        # Start processing from the Start state
        while i<t:
            next_state = handler(event_lst[i])     # Transform to a new state after a state transition function
            self.transition_history.append((i+1,"Input event:"+str(event_lst[i]),current_state,next_state)) #Log the logic of fsm transition
            handler = self.handlers[next_state]
            current_state=next_state
            i+=1


    @param_check(object)
    def visualize_time(self,clk1,clk2):
        time=[clk1,clk2,clk1,clk2]
        res = []
        res.append("digraph G {")
        res.append("  rankdir=LR;")
        for v in self.state:
            res.append("  {}[];".format(v))
        for index,v in enumerate(self.state):
            for index2,q in enumerate(self.state):
                if(v==q):
                    res.append('  {} -> {}[label="clk<{}; clk++"];'.format(v, q, time[index]))
                if index2-index==1:
                    res.append('  {} -> {}[label="clk>={}; clk=0"];'.format(v, q, time[index]))
        length=len(self.state)
        res.append('  {} -> {}[label="clk>={}; clk=0"];'.format(self.state[length-1], self.state[0], clk2))
        
        res.append("}")

        return "\n".join(res)

    @param_check(object,list)
    def visualize_event(self,event_list):
        res = []
        res.append("digraph G {")
        res.append("  rankdir=LR;")
        for v in self.state:
            res.append("  {}[];".format(v))

        for q in self.state:
            handler = self.handlers[q]
            for v in event_list:
                    next_state=handler(v)
                    res.append('  {} -> {}[label="{}"];'.format(q, next_state, v))
        
        res.append("}")

        return "\n".join(res)

#Used for parameter type detection unit test
@param_check(int,str,list)
def param_check_test(a,b,c):
    pass

if __name__ == "__main__":
    clk1 = 3
    clk2 = 1
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

    m.run_by_time(18)
    print(m.light_state_history)
    print(m.transition_history)

    dot=m.visualize_time(clk1,clk2)
    f= open('fsm_rgb_light.dot','w') 
    f.write(dot)
    f.close()

    with open("fsm_rgb_light.dot") as f:
        dot_graph = f.read()
    dot=graphviz.Source(dot_graph)
    dot.view(filename='rgb_light_state_diagram')

#     # m = StateMachine()
#     # m.add_state("s0","Initial state")
#     # m.add_state("s1","Sequence 1 detected")
#     # m.add_state("s2","Sequence 11 detected")
#     # m.add_state("s3","Sequence 110 detected")
#     # m.add_state("s4","Sequence 1101 detected")
#     # m.set_start("s0")
#     # m.add_transition("s0",lambda a: "s1" if a==1 else "s0")
#     # m.add_transition("s1",lambda a: "s2" if a==1 else "s0")
#     # m.add_transition("s2",lambda a: "s3" if a==0 else "s2")
#     # m.add_transition("s3",lambda a: "s4" if a==1 else "s0")
#     # m.add_transition("s4",lambda a: "s1" if a==1 else "s0")

#     # m.run_by_event([1,0,1,0,1,1,0,1])
#     # print(m.transition_history)

#     # dot=m.visualize_event([0,1])
#     # f= open('fsm_sequence_detection.dot','w') 
#     # f.write(dot)
#     # f.close()

#     # with open("fsm_sequence_detection.dot") as f:
#     #     dot_graph = f.read()
#     # dot=graphviz.Source(dot_graph)
#     # dot.view(filename='fsm_sequence_detection_diagram')

#     # m = StateMachine()
#     # m.add_state("StateStopping","Initial state")
#     # m.add_state("StateGoingUp","Sequence 1 detected")
#     # m.add_state("StateGoingDown","Sequence 11 detected")
#     # m.add_state("StateOpened","Sequence 110 detected")
#     # m.add_state("StateWarning","Sequence 1101 detected")

#     # m.set_start("StateStopping")

#     # m.add_transition("StateStopping",lambda a: "StateOpened" if a=='EVENT_OPEN' else ('StateGoingUp' if a=='EVENT_UP' else ('StateGoingDown' if a=='EVENT_DOWN' else 'StateStopping' )))
#     # m.add_transition("StateOpened",lambda a: "StateStopping" if a=='EVENT_CLOSE' else ('StateWarning' if a=='EVENT_WARN' else 'StateOpened'))
#     # m.add_transition("StateGoingUp",lambda a: "StateStopping" if a=='EVENT_STOP' else 'StateGoingUp')
#     # m.add_transition("StateGoingDown",lambda a: "StateStopping" if a=='EVENT_STOP' else "StateGoingDown")
#     # m.add_transition("StateWarning",lambda a: "StateOpened" if a=='EVENT_DELWARN' else "StateWarning")

#     # m.run_by_event(['EVENT_OPEN','EVENT_CLOSE','EVENT_UP','EVENT_STOP','EVENT_OPEN','EVENT_WARN','EVENT_DELWARN'])
#     # print(m.transition_history)

#     # dot=m.visualize_event(['EVENT_UP','EVENT_DOWN','EVENT_STOP','EVENT_OPEN','EVENT_CLOSE','EVENT_WARN','EVENT_DELWARN'])
#     # f= open('fsm_elevator.dot','w') 
#     # f.write(dot)
#     # f.close()

#     # with open("fsm_elevator.dot") as f:
#     #     dot_graph = f.read()
#     # dot=graphviz.Source(dot_graph)
#     # dot.view(filename='fsm_elevator_diagram')