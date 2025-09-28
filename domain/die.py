class Die:
    MAX_DICE = 100
    MAX_SIDES = 1000

    def __init__(self, count: int, sides: int, modifier: int = 0):
        if count <= 0:
            raise ValueError(f"Dice count must be positive, got {count}")
        if sides <= 0:
            raise ValueError(f"Dice sides must be positive, got {sides}")
        if count > self.MAX_DICE:
            raise ValueError(f"Too many dice: {count} (max {self.MAX_DICE})")
        if sides > self.MAX_SIDES:
            raise ValueError(f"Too many sides: {sides} (max {self.MAX_SIDES})")

        self.count = count
        self.sides = sides
        self.modifier = modifier
        self.rolls = []

    def roll(self, rng=None) -> int:
        import random
        rng = rng or random.randint
        self.rolls = [rng(1, self.sides) for _ in range(self.count)]
        return sum(self.rolls) + self.modifier

    @property
    def subtotal(self):
        return sum(self.rolls) + self.modifier

    def __repr__(self):
        return f"Die(count={self.count}, sides={self.sides}, modifier={self.modifier}, rolls={self.rolls})"
