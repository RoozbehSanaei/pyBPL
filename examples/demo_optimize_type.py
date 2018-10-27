"""
Sample a character type and then optimize its parameters to maximize the
likelihood of the type under the prior
"""
from __future__ import print_function, division
import argparse
import matplotlib.pyplot as plt

from pybpl.library import Library
from pybpl.ctd import CharacterTypeDist
from pybpl.concept import Character
from pybpl.inference import optimize_type

parser = argparse.ArgumentParser()
parser.add_argument(
        '--ns', help="number of strokes", required=False, type=int
)
parser.add_argument(
    '--lr', help='learning rate', default=1e-3, type=float
)
parser.add_argument(
    '--eps', help='tolerance for constrained optimization', default=1e-4,
    type=float
)
parser.add_argument(
    '--nb_iter', help='number of optimization iterations', default=1000,
    type=int
)
parser.add_argument(
    '--proj_grad_ascent', dest='proj_grad_ascent', action='store_true',
    help='use projected gradient ascent for constrained optimization'
)
parser.add_argument(
    '--no-proj_grad_ascent', dest='proj_grad_ascent', action='store_false'
)
parser.set_defaults(proj_grad_ascent=True)
args = parser.parse_args()



def main():
    # load the library
    lib = Library(lib_dir='./lib_data')
    # initialize the character type distribution
    type_dist = CharacterTypeDist(lib)
    # sample a character type from the distribution
    c = type_dist.sample_type(k=args.ns)
    print('num strokes: %i' % c.k)
    print('num sub-strokes: ', [p.nsub.item() for p in c.P])
    # optimize the character type that we sampled
    score_list = optimize_type(
        c, type_dist, args.lr, args.nb_iter, args.eps, args.proj_grad_ascent
    )
    # plot log-likelihood vs. iteration
    plt.figure()
    plt.plot(score_list)
    plt.ylabel('log-likelihood')
    plt.xlabel('iteration')
    plt.show()


if __name__ == "__main__":
    main()