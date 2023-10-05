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
    Tuple,
    Optional,
    Dict,
    List,
    Any
)


class QiskitPathfinder:
    """
    This class is responsible for finding the shortest path between two qubits
    on a given IBMQ device.

    # TODO TR:  Add local-gates induced errors when computing undirected graph.
    """

    def __init__(
        self,
        device_name: str,
        token: Optional[str] = None,
        directed: bool = False,
        weighted: bool = False,
    ) -> None:
        """
        Initializes the class.

        :param token: IBMQ token.
        :param device_name: Name of the device to be used.
        :param directed: If True, the graph will be directed.
        :param weighted: If True, the graph will be weighted.
        """
        self.provider: IBMProvider

        if token is None:
            self.provider = IBMProvider()
        else:
            self.provider = IBMProvider(token=token)

        device: BackendV1 = self.provider.get_backend(device_name)
        self.graph: Graph = self.to_graph_array(
            device,
            directed=directed,
            weighted=weighted
        )

    @staticmethod
    def to_graph_array(
        backend: BackendV1,
        directed: bool = False,
        weighted: bool = False,
    ) -> Graph:
        """
        Converts a coupling map to a graph.

        :param backend: Backend to be used.
        :param directed: If True, the graph will be directed.
        :param weighted: If True, the graph will be weighted.

        :return: Graph representation of the coupling map.
        """
        graph: Graph = Graph()
        edges: Dict[Tuple[int, int], float] = QiskitPathfinder.get_graph_edges(backend)

        for edge in edges:

            weight: float = 1 if not weighted else edges[edge]

            graph.add_edge(
                edge[0],
                edge[1],
                weight,
            )

            if not directed:
                graph.add_edge(
                    edge[1],
                    edge[0],
                    weight,
                )

        return graph

    @staticmethod
    def get_graph_edges(backend: BackendV1) -> Dict[Tuple[int, int], float]:
        """
        Returns the edges of the graph.

        :param backend: Backend to be used.

        :return: Edges of the graph.
        """
        edges: Dict[Tuple[int, int], float] = {}

        # Get multi-qubit gates.
        gates: List[str, Dict[str, Any]] = backend.properties().to_dict()["gates"]
        gates = [gate for gate in gates if len(gate["qubits"]) > 1]

        for gate in gates:
            edges[tuple(gate["qubits"])] = gate["parameters"][0]["value"]

        return edges

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
