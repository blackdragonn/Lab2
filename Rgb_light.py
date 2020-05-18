import graphviz

def ParamCheck(*ty2):  
 
    def common(fun):
        def deal(*fun_x):
            ty=map(ToCheckFun,ty2)
            if ty:
                x_list=[a for a in fun_x]
                x_list_it=iter(x_list)
                result=[]
                for t_check in ty:
                    r=t_check(x_list_it.__next__())
                    result.append(r)
                print('param check result: ',result)
                    
            return fun(*fun_x)
        
        return deal                
    return common

def ToCheckFun(t):
    return lambda x:isinstance(x,t)

class StateMachine:
    def __init__(self): 
        self.handlers = {}        # 状态转移函数字典
        self.startState = None    # 初始状态
        self.state=[]
        self.stateAction={}       # 说明这个状态在干啥
        self.clk=0                # 时钟
        self.state_history = []   # 每个时钟时的状态历史 
        self.transition_history = []  #每次状态转移记录

    #设置起始状态
    @ParamCheck(object,str)
    def set_start(self, state):
        self.startState = state
        self.state_history.append((self.clk,state))

    # 参数name为状态名
    @ParamCheck(object,str,str)
    def add_state(self, name, action):
        self.stateAction[name]=action
        self.state.append(name)

    #设置状态转移函数
    @ParamCheck(object,str,object)
    def add_transition(self,state,function):
        self.handlers[state] = function#为每个状态设置状态转移
        return function

    @ParamCheck(object,int)
    def run(self, clk_n):

        handler = self.handlers[self.startState]
        current_state=self.startState
        all_clk=clk_n
        # 从Start状态开始进行处理
        while clk_n>0:
            self.state_history.append((all_clk-clk_n+1,current_state)) 
            (clk_new, next_state) = handler(self.clk)     # 经过状态转移函数变换到新状态
            self.clk=clk_new
            self.transition_history.append((all_clk-clk_n+1,current_state,next_state))
 #           print("current_state: %s current_state_action: %s next_state: %s" % (current_state,self.stateAction[current_state],next_state))
            handler = self.handlers[next_state]
            current_state=next_state
            clk_n-=1
    @ParamCheck(object)
    def visualize(self,clk1,clk2):
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

if __name__ == "__main__":
    clk1 = int(input('green light last:'))
    clk2 = int(input('yellow light last:'))
    m = StateMachine()
    m.set_start("s0")
    m.add_state("s0","A green,B red")
    m.add_state("s1","A yellow,B red")
    m.add_state("s2","A red,B green")
    m.add_state("s3","A red,B yellow")
    m.add_transition("s0",lambda clk: (clk+1,"s0") if clk<clk1 else (clk and 0,"s1"))
    m.add_transition("s1",lambda clk: (clk+1,"s1") if clk<clk2 else (clk and 0,"s2"))
    m.add_transition("s2",lambda clk: (clk+1,"s2") if clk<clk1 else (clk and 0,"s3"))
    m.add_transition("s3",lambda clk: (clk+1,"s3") if clk<clk2 else (clk and 0,"s0"))

    m.run(20)
    print(m.state_history)
    print(m.transition_history)

    dot=m.visualize(clk1,clk2)
    f= open('fsm.dot','w') 
    f.write(dot)
    f.close()

    with open("fsm.dot") as f:
        dot_graph = f.read()
    dot=graphviz.Source(dot_graph)
    dot.view()
