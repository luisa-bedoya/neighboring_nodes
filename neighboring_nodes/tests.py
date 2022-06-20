from django.test import TestCase
from neighboring_nodes.views import *


class NeighborNodesTests(TestCase):

    # Preparing the general case to test
    global neighboring_nodes
    neighboring_nodes = NeighboringNodes(5, False)
    
    # tests will be done on the entire diagonal 
    # starting at position 0.0 to 4.4
    # being (index (x coordinate, y coordinate)):
    #  0 (0,0) |  1 (1,0) |  2 (2,0) |  3 (3,0) |  4 (4,0) |  
    #  5 (0,1) |  6 (1,1) |  7 (2,1) |  8 (3,1) |  9 (4,1) | 
    # 10 (0,2) | 11 (1,2) | 12 (2,2) | 13 (3,2) | 14 (4,2) | 
    # 15 (0,3) | 16 (1,3) | 17 (2,3) | 18 (3,3) | 19 (4,3) |
    # 20 (0,4) | 21 (1,4) | 22 (2,4) | 23 (3,4) | 24 (4,4) |

    
    def test_create_neighborhood(self):
        """
        Ensure what we created is an expected neighborhood,
        ensure it be built by Node's instances
        """

        global neighboring_nodes

        node_0 = Node(0, 0, 0)
        node_6 = Node(6, 1, 1)
        node_12 = Node(12, 2, 2)
        node_18 = Node(18, 3, 3)
        node_24 = Node(24, 4, 4)

        assert type(neighboring_nodes.grid[0][0]) == type(node_0)
        assert str(neighboring_nodes.grid[0][0]) == str(node_0)
        assert type(neighboring_nodes.grid[1][1]) == type(node_6)
        assert str(neighboring_nodes.grid[1][1]) == str(node_6)
        assert type(neighboring_nodes.grid[2][2]) == type(node_12)
        assert str(neighboring_nodes.grid[2][2]) == str(node_12)
        assert type(neighboring_nodes.grid[3][3]) == type(node_18)
        assert str(neighboring_nodes.grid[3][3]) == str(node_18)
        assert type(neighboring_nodes.grid[4][4]) == type(node_24)
        assert str(neighboring_nodes.grid[4][4]) == str(node_24)
   
    
    def test_get_node_coordinates(self):
        """
        Node coordinates function return what is expected
        Tested by all the nodes in the diagonal.
        """

        global neighboring_nodes

        x, y = neighboring_nodes.get_node_coordinates(0)
        assert x == 0
        assert y == 0

        x, y = neighboring_nodes.get_node_coordinates(6)
        assert x == 1
        assert y == 1

        x, y = neighboring_nodes.get_node_coordinates(12)
        assert x == 2
        assert y == 2

        x, y = neighboring_nodes.get_node_coordinates(18)
        assert x == 3
        assert y == 3

        x, y = neighboring_nodes.get_node_coordinates(24)
        assert x == 4
        assert y == 4


    def test_finding_neighbors(self):
        """
        Ensure exception cases (radius too big, etc),
        output for each type of neighbor is expected
        """

        global neighboring_nodes

        output, indexes = neighboring_nodes.finding_neighbors(1, "INVALID-TYPE", 6)
        assert output == "Neighborhood type not valid"

        output, indexes = neighboring_nodes.finding_neighbors(4, "SQUARE", 6)
        assert output == "Neighborhood radius not valid"

        output, indexes = neighboring_nodes.finding_neighbors(2, "SQUARE", 0, 0)
        assert output == "The radius is too big to draw the neighbor type in that position"
        
        # Testing with radius = 1
        output, indexes = neighboring_nodes.finding_neighbors(1, "SQUARE", 6)
        expected_output =  ["x: 0, y: 1, index: 5",
                            "x: 0, y: 2, index: 10",
                            "x: 1, y: 2, index: 11",
                            "x: 2, y: 2, index: 12",
                            "x: 2, y: 1, index: 7",
                            "x: 2, y: 0, index: 2",
                            "x: 1, y: 0, index: 1",
                            "x: 0, y: 0, index: 0", 
                            ""]

        output_array = output.split("\n")
        
        for i, value in enumerate(output_array):
            assert expected_output[i] == value.strip()
        
        output, indexes = neighboring_nodes.finding_neighbors(1, "CROSS", 1, 1)
        expected_output =  ["x: 1, y: 2, index: 11",
                            "x: 2, y: 1, index: 7",
                            "x: 1, y: 0, index: 1",
                            "x: 0, y: 1, index: 5",
                            ""]

        output_array = output.split("\n")
        
        for i, value in enumerate(output_array):
            assert expected_output[i] == value.strip()

        output, indexes = neighboring_nodes.finding_neighbors(1, "DIAMOND", 1, 1)
        expected_output =  ["x: 0, y: 1, index: 5",
                            "x: 1, y: 2, index: 11",
                            "x: 2, y: 1, index: 7",
                            "x: 1, y: 0, index: 1",                            
                            ""]

        output_array = output.split("\n")
        
        for i, value in enumerate(output_array):
            assert expected_output[i] == value.strip()

        # Testing with radius = 2

        output, indexes = neighboring_nodes.finding_neighbors(2, "SQUARE", 12)
        expected_output =  ["x: 1, y: 2, index: 11",
                            "x: 1, y: 3, index: 16",
                            "x: 2, y: 3, index: 17",
                            "x: 3, y: 3, index: 18",
                            "x: 3, y: 2, index: 13",
                            "x: 3, y: 1, index: 8",
                            "x: 2, y: 1, index: 7",
                            "x: 1, y: 1, index: 6", 
                            "x: 0, y: 1, index: 5",
                            "x: 0, y: 2, index: 10",
                            "x: 0, y: 3, index: 15",
                            "x: 0, y: 4, index: 20",
                            "x: 1, y: 4, index: 21",
                            "x: 2, y: 4, index: 22",
                            "x: 3, y: 4, index: 23",
                            "x: 4, y: 4, index: 24",
                            "x: 4, y: 3, index: 19", 
                            "x: 4, y: 2, index: 14",
                            "x: 4, y: 1, index: 9",
                            "x: 4, y: 0, index: 4",
                            "x: 3, y: 0, index: 3",
                            "x: 2, y: 0, index: 2",
                            "x: 1, y: 0, index: 1",
                            "x: 0, y: 0, index: 0",
                            ""]

        output_array = output.split("\n")

        for i, value in enumerate(output_array):
            assert expected_output[i] == value.strip()

        output, indexes = neighboring_nodes.finding_neighbors(2, "CROSS", 12)
        expected_output =  ["x: 2, y: 3, index: 17",
                            "x: 3, y: 2, index: 13",
                            "x: 2, y: 1, index: 7",
                            "x: 1, y: 2, index: 11", 
                            "x: 2, y: 4, index: 22",
                            "x: 4, y: 2, index: 14",
                            "x: 2, y: 0, index: 2",
                            "x: 0, y: 2, index: 10",                            
                            ""]

        output_array = output.split("\n")
        
        for i, value in enumerate(output_array):
            assert expected_output[i] == value.strip()

        output, indexes = neighboring_nodes.finding_neighbors(2, "DIAMOND", 12)
        expected_output =  ["x: 1, y: 2, index: 11", 
                            "x: 2, y: 3, index: 17",
                            "x: 3, y: 2, index: 13",
                            "x: 2, y: 1, index: 7",
                            "x: 1, y: 1, index: 6", 
                            "x: 0, y: 2, index: 10",
                            "x: 1, y: 3, index: 16",
                            "x: 2, y: 4, index: 22",
                            "x: 3, y: 3, index: 18", 
                            "x: 4, y: 2, index: 14",
                            "x: 3, y: 1, index: 8",
                            "x: 2, y: 0, index: 2",                   
                            ""]

        output_array = output.split("\n")
        
        for i, value in enumerate(output_array):
            assert expected_output[i] == value.strip()
