class AgentStateMachine:
    def __init__(self):
        self.state = "IDLE"
    def transition(self, next_state: str):
        self.state = next_state
