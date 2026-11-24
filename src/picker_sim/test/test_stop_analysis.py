from picker_sim.stop_test import analyse


def test_analyse():
    # slows, stops at t=0.10, stays: 3 cm travelled
    s = [(0.05, 0.02, 0, 0.1), (0.10, 0.03, 0, 0.0), (0.20, 0.03, 0, 0.0)]
    t, d, stays = analyse(s, 0.0, (0.0, 0.0))
    assert abs(t - 0.10) < 1e-9 and abs(d - 0.03) < 1e-9 and stays
    # never stops
    t, _, stays = analyse([(0.1, 0.1, 0, 0.2)], 0.0, (0.0, 0.0))
    assert t is None and not stays
    # stops, moves again, stops: rest is the last still stretch
    s = [(0.1, 0, 0, 0.0), (0.2, 0.1, 0, 0.2), (0.3, 0.1, 0, 0.0)]
    t, _, stays = analyse(s, 0.0, (0.0, 0.0))
    assert abs(t - 0.3) < 1e-9 and stays
