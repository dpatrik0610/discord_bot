import re
from .die import Die

class DiceRoller:
    _dice_pattern = re.compile(r'^(\d*)d(\d+)', re.IGNORECASE)
    _modifier_pattern = re.compile(r'^([+-]\d+)(?!d)')

    def roll(self, notation: str, debug: bool = False) -> dict:
        s = notation.replace(" ", "")
        if not s:
            raise ValueError("Empty dice notation")

        if debug:
            print(f"[DEBUG] Original notation: {notation}")
            print(f"[DEBUG] Stripped notation: {s}")

        dice_entries = []
        step = 0

        while s:
            if s.startswith('+'):
                # Leading '+' or '-' indicates a modifier without a die, which is invalid
                s = s[1:]  # remove leading '+' or '-'
            if s.startswith('-'):
                raise ValueError(f"Dice count must be positive")     
                   
            step += 1
            if debug:
                print(f"\n[DEBUG][Step {step}] Remaining string: '{s}'")

            # Step 1: match a die
            dice_match = self._dice_pattern.match(s)
            if not dice_match:
                raise ValueError(f"Expected dice at: {s}")
            count_str, sides_str = dice_match.groups()
            count = int(count_str) if count_str else 1
            sides = int(sides_str)
            if debug:
                print(f"[DEBUG][Step {step}] Matched die: {count}d{sides}")

            s = s[dice_match.end():]  # remove the die part
            if debug:
                print(f"[DEBUG][Step {step}] Remaining string after removing die: '{s}'")

            # Step 2: optional modifier
            mod = 0
            mod_match = self._modifier_pattern.match(s)
            if mod_match:
                mod = int(mod_match.group(1))
                s = s[mod_match.end():]  # remove the modifier part

                if debug:
                    print(f"[DEBUG][Step {step}] Matched modifier: {mod}")
                    print(f"[DEBUG][Step {step}] Remaining string after removing modifier (and optional '+'): '{s}'")
            else:
                if debug:
                    print(f"[DEBUG][Step {step}] No modifier found, default to 0")

            # Step 3: create Die object
            die = Die(count=count, sides=sides, modifier=mod)
            dice_entries.append(die)
            if debug:
                print(f"[DEBUG][Step {step}] Created Die object: {die}")

        # Step 4: sanity check for leftover modifiers
        remaining_mods = re.findall(r'[+-]\d+', s)
        if remaining_mods:
            raise ValueError(f"Extra modifiers without a dice: {remaining_mods}")
        if debug:
            print(f"\n[DEBUG] Finished parsing dice. Total dice entries: {len(dice_entries)}")

        # Step 5: roll all dice and calculate total
        total = 0
        for idx, die in enumerate(dice_entries, start=1):
            die.roll()
            total += die.subtotal
            if debug:
                print(f"[DEBUG] Rolled Die {idx}: {die.count}d{die.sides} + {die.modifier} => rolls: {die.rolls}, subtotal: {die.subtotal}")

        if debug:
            print(f"[DEBUG] Final total: {total}")
            print(f"[DEBUG] ----------------------------")
        return {"total": total, "details": dice_entries}
