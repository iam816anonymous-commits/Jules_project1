import unittest
from unittest.mock import MagicMock, patch
from jarvis.world_model.world_state import WorldState
from jarvis.world_model.action_validator import ActionValidator

class TestChaosV1(unittest.TestCase):
    def setUp(self):
        self.validator = ActionValidator()
        self.world_state = WorldState()

    def test_missing_window_grounding(self):
        # Planner wants to click in 'Chrome', but WorldState is empty
        action = {"action": "mouse_click", "params": {"window_title": "Chrome"}}
        self.world_state.open_windows = [] # Window is missing

        valid, msg = self.validator.validate(action, self.world_state)
        self.assertFalse(valid)
        self.assertIn("not found", msg)

    def test_wrong_focus_denial(self):
        # Interactive action with no focused element in WorldState
        action = {"action": "type", "params": {"text": "hello"}}
        self.world_state.focused_element = None

        valid, msg = self.validator.validate(action, self.world_state)
        self.assertFalse(valid)

    def test_hallucination_correction(self):
        # Simulate belief update from Vision that corrects a hallucinated state
        self.world_state.confidence = 0.5 # Low confidence due to conflicting signals
        action = {"action": "mouse_click", "params": {}}

        valid, msg = self.validator.validate(action, self.world_state)
        self.assertFalse(valid)
        self.assertIn("below threshold", msg)

if __name__ == '__main__':
    unittest.main()
