from scripts.families.dravidian import Dravidian
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
    family = Uralic()
    print_clock_rate(family, 5.685e-2)
    print_burst(family, 8.328e-3, mean=True)
