# Run with: `python -m unittest discover`

import unittest

from ruleset import RuleSet, Pkgs


class Test(unittest.TestCase):
    def test_depends_aa(self):
        rs = RuleSet()

        rs.addDep("a", "a")

        self.assertTrue(rs.isCoherent(), "rs.isCoherent failed")

    def test_depends_ab_ba(self):
        rs = RuleSet()

        rs.addDep("a", "b")
        rs.addDep("b", "a")

        self.assertTrue(rs.isCoherent(), "rs.isCoherent failed")

    def test_exclusive_ab(self):
        rs = RuleSet()

        rs.addDep("a", "b")
        rs.addConflict("a", "b")

        self.assertFalse(rs.isCoherent(), "rs.isCoherent failed")

    def test_exclusive_ab_bc(self):
        rs = RuleSet()

        rs.addDep("a", "b")
        rs.addDep("b", "c")
        rs.addConflict("a", "c")

        self.assertFalse(rs.isCoherent(), "rs.isCoherent failed")

    def test_deep_deps(self):
        rs = RuleSet()

        rs.addDep("a", "b")
        rs.addDep("b", "c")
        rs.addDep("c", "d")
        rs.addDep("d", "e")
        rs.addDep("a", "f")
        rs.addConflict("e", "f")

        self.assertFalse(rs.isCoherent(), "rs.isCoherent failed")

    def test_exclusive_ab_bc_ca_de(self):
        rs = RuleSet()
        rs.addDep("a", "b")
        rs.addDep("b", "c")
        rs.addDep("c", "a")
        rs.addDep("d", "e")
        rs.addConflict("c", "e")

        self.assertTrue(rs.isCoherent(), "rs.isCoherent failed")

        pkgs = Pkgs(rs)

        pkgs.toggle("a")
        self.assertSetEqual(
            pkgs.selection(),
            set(["a", "c", "b"]),
            "toggle expected (a, c, b) got %s" % pkgs.selection(),
        )

        rs.addDep("f", "f")
        pkgs.toggle("f")
        self.assertSetEqual(
            pkgs.selection(),
            set(["a", "c", "b", "f"]),
            "toggle expected (a, c, b, f) got %s" % pkgs.selection(),
        )

        pkgs.toggle("e")
        self.assertSetEqual(
            pkgs.selection(),
            set(["e", "f"]),
            "toggle expected (e, f) got %s" % pkgs.selection(),
        )

        pkgs.toggle("b")
        self.assertSetEqual(
            pkgs.selection(),
            set(["a", "c", "b", "f"]),
            "toggle expected (a, c, b, f) got %s" % pkgs.selection(),
        )

        rs.addDep("b", "g")
        pkgs.toggle("g")
        pkgs.toggle("b")
        # pkgs.toggle("e")
        self.assertSetEqual(
            pkgs.selection(),
            set(["g", "f"]),
            "toggle expected (g, f) got %s" % pkgs.selection(),
        )

    def test_ab_bc_toggle(self):
        rs = RuleSet()

        rs.addDep("a", "b")
        rs.addDep("b", "c")
        pkgs = Pkgs(rs)
        pkgs.toggle("c")

        self.assertSetEqual(
            pkgs.selection(),
            set(["c"]),
            "toggle expected (c) got %s" % pkgs.selection(),
        )

    # Multiple dependencies and exclusions.
    def test_ab_ac(self):
        rs = RuleSet()

        rs.addDep("a", "b")
        rs.addDep("a", "c")
        rs.addConflict("b", "d")
        rs.addConflict("b", "e")

        self.assertTrue(rs.isCoherent(), "rs.isCoherent failed")

        pkgs = Pkgs(rs)
        pkgs.toggle("d")
        pkgs.toggle("e")
        pkgs.toggle("a")
        self.assertSetEqual(
            pkgs.selection(),
            set(["a", "c", "b"]),
            "toggle expected (a, c, b) got %s" % pkgs.selection(),
        )