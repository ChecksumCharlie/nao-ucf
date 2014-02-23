'''
Created on Nov 9, 2013

@author: Astrid
'''

class StateMachine(object):
    '''
    classdocs
    '''
    states = {};
    transitions = {};
    events = [];


    def __init__(self, initialState):
        self.states[initialState['name']] = initialState['handle'];
        self.transitions[initialState['name']] = {};
        
        self.initialState = initialState['name'];
        self.currentState = self.initialState;
        self.previousState = None;
        self.nextState = None;
            
        
    def addState(self, newState):
        self.states[newState['name']] = newState['handle'];
        self.transitions[newState['name']] = {};
        
    def addTransition(self, fromState, event, toState):
        assert(fromState in self.states), 'Unknown state %s' % fromState;
        assert(toState in self.states), 'Unknown state %s' % toState
        try:
            self.transitions[fromState]
        except NameError:
            self.transitions[fromState] = {};
        self.transitions[fromState][event] = toState;
        
    def addEvent(self, event):
        assert(event in self.transition(self.currentState)), 'Unknown event for state %s: %s' % (self.currentState, event);
        self.events.append(event);
    
    
    def transition(self):
        state = self.states[self.currentState];
        state.exit();
        self.previousState = self.currentState;
        self.currentState = self.nextState;
        self.nextState = None;
        self.states[self.currentState].enter();
        
        
    def enter(self):
        state = self.states[self.currentState];
        return state.enter();
    
    def update(self):
        state = self.states[self.currentState];
        
        if (self.nextState == None):
            event = state.update();
            if (event != None):
                assert(event in self.transitions[self.currentState]), 'Event not defined for state %s: %s' % (event, self.currentState);
                self.events.append(event);
        
        # process events
        for e in self.events:
            if (self.transitions[self.currentState][e]):
                self.nextState = self.transitions[self.currentState][e];
                break;
        self.events = [];
        
        # check and enter next state
        if (self.nextState != None):
            self.transition();
        
    def exit(self):
        state = self.states[self.currentState];
        state.exit();
        self.currentState = self.initialState;