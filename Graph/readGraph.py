import json
import networkx as nx

from Graph.node import NodeGraph


class Decision:
    __instance = None

    @staticmethod
    def getInstance():

        if Decision.__instance is None:
            Decision()
        return Decision.__instance

    def __init__(self):
        if Decision.__instance is not None:
            raise Exception("This class is a singleton!")

        else:
            Decision.__instance = self
            self.graph = nx.DiGraph()
            self.nodes = {}

    def readJson(self):
        # Opening JSON file
        json_file = open('decision.json')

        # returns JSON object as
        # a dictionary
        data = json.load(json_file)

        # Iterating through the json
        # list
        for node in data['nodes']:
            # def __init__(self, num, question, left_name, left_next_step, right_name, right_next_step):
            node_graph = NodeGraph(
                node['num'],
                node['question'],
                node['left']['name'],
                node['left']['next_step'],
                node['right']['name'],
                node['right']['next_step'],
            )

            print("*******************")
            print(node_graph)
            self.graph.add_node(node_graph.num, node=node_graph)

        print(list(Decision.getInstance().graph.nodes))

        for node_graph in list(self.graph.nodes):
            node = self.graph.nodes[node_graph]['node']
            self.graph.add_edge(node_graph, node.get_left_next_step())
            self.graph.add_edge(node_graph, node.get_right_next_step())

        # Closing file
        json_file.close()

    def getFirstNode(self):
        return self.graph.nodes[0]
