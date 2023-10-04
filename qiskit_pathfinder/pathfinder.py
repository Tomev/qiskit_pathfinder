"""
=============================================================================

    This module contains a shortest path finding utility for the qiskit-provided
    devices.

=============================================================================
"""

__author__ = "Tomasz Rybotycki"


from qiskit_ibm_provider import (
    IBMProvider,
)
from qiskit.providers import (
    BackendV1,
)
from dijkstar import (
    Graph,
    find_path,
)
from dijkstar.algorithm import (
    PathInfo,
)
from typing import (
    List,
    Optional,
)


class QiskitPathfinder:
    """
    This class is responsible for finding the shortest path between two qubits
    on a given IBMQ device.

    # TODO TR:  Add optional weights based on the 2-qubit error gates.
    """

    def __init__(
        self,
        device_name: str,
        token: Optional[str] = None,
        directed: bool = False,
    ) -> None:
        """
        Initializes the class.

        :param token: IBMQ token.
        :param device_name: Name of the device to be used.
        :param directed: If True, the graph will be directed.
        """
        self.provider: IBMProvider

        if token is None:
            self.provider = IBMProvider()
        else:
            self.provider = IBMProvider(token=token)

        device: BackendV1 = self.provider.get_backend(device_name)
        self.graph: Graph = self.to_graph_array(
            device.configuration().coupling_map,
            directed=directed,
        )

    @staticmethod
    def to_graph_array(
        coupling_map: List[List[int]],
        directed: bool = False,
    ) -> Graph:
        """
        Converts a coupling map to a graph.

        :param coupling_map: Coupling map to be converted.
        :param directed: If True, the graph will be directed.

        :return: Graph representation of the coupling map.
        """
        graph: Graph = Graph()

        for connection in coupling_map:
            graph.add_edge(
                connection[0],
                connection[1],
                1,
            )

            if not directed:
                graph.add_edge(
                    connection[1],
                    connection[0],
                    1,
                )

        return graph

    def find_path(
        self,
        source: int,
        destination: int,
    ) -> PathInfo:
        """
        Finds the shortest path between two qubits.

        :param source: Source qubit.
        :param destination: Destination qubit.

        :return: Shortest path between the two qubits.
        """
        return find_path(
            self.graph,
            source,
            destination,
        )
