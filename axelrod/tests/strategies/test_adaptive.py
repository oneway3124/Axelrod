"""Tests for the Adaptive strategy."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestAdaptive(TestPlayer):

    name = "Adaptive"
    player = axelrod.Adaptive
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(["game"]),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C)] * 6 + [(D, C)] * 8
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D)] * 6 + [(D, D)] * 8
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        actions = [(C, C), (C, D)] * 3 + [(D, C), (D, D)] * 4
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C)] * 6 + [(D, C)] + [(D, D)] * 4 + [(C, D), (C, C)]
        self.versus_test(axelrod.TitForTat(), expected_actions=actions)

    def test_scoring(self):
        player = axelrod.Adaptive()
        opponent = axelrod.Cooperator()
        match = axelrod.Match((player, opponent), turns=2, seed=9)
        match.play()
        self.assertEqual(3, player.scores[C])
        match = axelrod.Match((player, opponent), turns=1, reset=True, seed=9,
                              game=axelrod.Game(-3, 10, 10, 10))
        match.play()
        self.assertEqual(0, player.scores[C])
