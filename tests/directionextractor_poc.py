"""
=============================================================================

    This module contains proof of concept for the DirectionExtractor.

    Assumes that the account with the access to the IBMQ device is already
    configured.

=============================================================================
"""

__author__ = "Tomasz Rybotycki"

from qiskit_pathfinder.directionextractor import DirectionExtractor


def main():
    # This one should work and save the results to the file.
    extractor: DirectionExtractor = DirectionExtractor("ibm_brisbane")
    extractor.extract_directions(save_to_file=True)
    print("Test 1 done.\n\n")

    # This should work and save the results to the file and variables.
    names, directions = extractor.extract_directions(save_to_file=True)
    print(names)
    print(directions)
    print("Test 2 done.\n\n")
    print("\n")
    print("\n")

    # And this should work without saving results to the file.
    names2, directions2 = extractor.extract_directions()
    print(names2)
    print(directions2)
    print("Test 3 done.\n\n")
    print("Tests finished.")


if __name__ == "__main__":
    main()
