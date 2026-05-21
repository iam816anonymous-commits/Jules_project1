import unittest
from jarvis.world_model.world_state import WorldState
from jarvis.world_model.action_validator import ActionValidator

class TestWorldModel(unittest.TestCase):
    def test_action_validator(self):
        state = WorldState()
        state.current_task_id = "123"
        state.open_windows = [{"title": "Browser"}]
        state.confidence = 0.9

        validator = ActionValidator()

        # Valid action
        action = {"type": "click", "params": {"window_title": "Browser"}}
        valid, msg = validator.validate(action, state)
        self.assertTrue(valid)

        # Invalid action (window missing)
        action2 = {"type": "click", "params": {"window_title": "VSCode"}}
        valid2, msg2 = validator.validate(action2, state)
        self.assertFalse(valid2)

if __name__ == '__main__':
    unittest.main()
