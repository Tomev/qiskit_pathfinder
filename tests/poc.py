"""
=============================================================================

    This module contains proof of concept for the pathfinder.

    Assumes that the account with the access to the IBMQ device is already
    configured.

=============================================================================
"""

__author__ = "Tomasz Rybotycki"

from qiskit_pathfinder.pathfinder import (
    QiskitPathfinder,
    PathInfo,
)
from dijkstar.algorithm import (
    NoPathError,
)


def main():
    # This one should work.
    try:
        pathfinder: QiskitPathfinder = QiskitPathfinder("ibm_brisbane")
        path_info: PathInfo = pathfinder.find_path(
            0,
            126,
        )
        print(path_info)
    except NoPathError as e:
        print(e)

    # This one should fail.
    try:
        pathfinder: QiskitPathfinder = QiskitPathfinder(
            "ibm_brisbane",
            directed=True,
        )
        path_info: PathInfo = pathfinder.find_path(
            0,
            126,
        )
        print(path_info)
    except NoPathError as e:
        print(e)


if __name__ == "__main__":
    main()
