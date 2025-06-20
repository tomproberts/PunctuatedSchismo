from scripts.families.indo_european import IndoEuropean
from scripts.families.uralic import Uralic


def transform(family, value, percentage=True):
    transformed = 0.5 * value * family.n_sites / family.n_concepts
    if percentage:
        transformed *= 100
    return transformed


def print_clock_rate(family, clockrate):
    print(f'{family.name} clockrate c_μ = {clockrate} → {transform(family, clockrate):.1f} % / Kya')


def print_burst(family, burst, mean=False):
    print(f'{family.name} burst {'b_μ' if mean else 'b_i'} = {burst} → {transform(family, burst):.1f} %')


if __name__ == '__main__':
    family = IndoEuropean()
    print('--Douglas--')
    print_clock_rate(family, 9.485e-3)
    print_burst(family, 1.183e-3)

    family = Uralic()
    print('\n--Prior (long root)--')
    print_clock_rate(family, 9.66e-4)
    print_burst(family, 1.04e-2, mean=True)
    print('--Posterior (long root)--')
    print_clock_rate(family, 1.083e-3)
    print_burst(family, 2.127e-2, mean=True)
    print('\n--Prior (constrained)--')
    print_clock_rate(family, 4.952e-2)
    print_burst(family, 1.032e-2, mean=True)
    print('--Posterior (constrained)--')
    print_clock_rate(family, 3.612e-2)
    print_burst(family, 0.106, mean=True)
