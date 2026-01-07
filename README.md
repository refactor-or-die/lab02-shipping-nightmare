# Lab 02: Shipping Nightmare

## Did you know...
The average programmer spends 73% of their time debugging if-statements in legacy code? (source: there is no source, go to church)

## Your task
You've received an e-commerce shipping cost calculator code. The previous developer ran away to the Bieszczady mountains and left behind a method with **over 200 lines of if-statements**.

Your boss yells: "We need to add hot air balloon shipping!"
You look at the code and think: "Where am I supposed to squeeze this in?"

**Solution:** Strategy Pattern!

## What's in the repository
- `shipping_calculator.py` - every programmer's nightmare
- `test_shipping_calculator.py` - tests (DON'T TOUCH!)
- This README
- Some other stuff

## Instructions
1. Clone the repo and create a branch `lab2_lastname1_lastname2`
2. Run the tests: `pytest` (they should pass)
3. Refactor the code using the Strategy pattern
4. Run the tests again (they MUST pass)
5. Commit + push to your branch
6. Prepare for presentation

## Hints
- Each shipping type (`standard`, `express`, etc.) should be a separate strategy
- Don't change the `calculate_shipping()` method API - tests must work!
- Remember edge cases (e.g., drones don't fly in bad weather)
- There should be at most a few if-statements in the new code (not 200!)

## What you'll gain
- Code you can read without crying
- Easy addition of new delivery types
- Ability to test each strategy separately
- Respect from your teammates

## Grading criteria
- Tests pass
- Strategy pattern is used
- Code is readable
- Easy to add new shipping type
- Presentation was clear

## FAQ
**Q: Can I use Java?**

A: No.

**Q: Can I use external libraries?**

A: You don't need to. Python has everything (ABC, type hints).

**Q: What about the randomness in drone?**

A: Leave it. Drones don't like rain.

**Q: Is 200 lines a lot?**

A: I've seen a method with 2000 lines. It had 47 levels of nested if-statements. The programmer who wrote it now raises alpacas (seriously).

**Q: Seriously, can't I use Java?**

A: No.

**Q: Python sucks!**

A: Be my guest and try JavaScript, Perl or PHP (but not in class).

**Q: So maybe I'll try Java???**

A: No.

**Q: But the instructor is stupid, makes us use Python but doesn't know it himself?**

A: I don't need to pretend to be all-knowing. Besides - "nobody's holding anyone at gunpoint here" :)

---

*"Good code is code you can understand at 3 AM after 4 beers"* - Wise Senior Developer (looks like a guinea pig)

Good luck!
