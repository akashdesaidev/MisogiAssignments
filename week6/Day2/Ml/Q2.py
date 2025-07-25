import random

def simulate_dice_rolls(n=10000):
    sum_7 = 0
    sum_2 = 0
    sum_gt_10 = 0

    for _ in range(n):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2

        if total == 7:
            sum_7 += 1
        if total == 2:
            sum_2 += 1
        if total > 10:
            sum_gt_10 += 1

    print(f"P(Sum = 7): {sum_7 / n:.4f}")
    print(f"P(Sum = 2): {sum_2 / n:.4f}")
    print(f"P(Sum > 10): {sum_gt_10 / n:.4f}")

# Run the simulation
simulate_dice_rolls()
