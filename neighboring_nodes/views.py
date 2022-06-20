from django.shortcuts import render


def controller(request):
    """
    Function in charge of connecting the template with the logic based on 
    forms that add parameters and define the operation of the logic.
    Arguments:
        request: request object
    Returns:
        request object
        parameters dict 
    """
    if request.method == "POST":
        data = request.POST
        size = data.get('size')
        debug = data.get('debug')
        index_node_coordinates = data.get('get_by_index')
        index = data.get('index')
        radius = data.get('radius')
        type_neighbor = data.get('type_neighbor')
        x_coordinate = data.get('x_coordinate')
        y_coordinate = data.get('y_coordinate')

        if size:
            neighboring_nodes = NeighboringNodes(int(size), False)
            node_coordinates = None
            output_neighbor = None
            grid = None
            indexes = []

            if index_node_coordinates:
                x, y = neighboring_nodes.get_node_coordinates(int(index_node_coordinates))
                node_coordinates = f"x: {x}, y: {y}"

            if index and type_neighbor and radius:
                output_neighbor, indexes = neighboring_nodes.finding_neighbors(int(radius), type_neighbor, int(index), None)
                grid = [[ (i + int(size) * j, (1 if (i + int(size) * j) in indexes else 0 )) for i in range(0, int(size))] 
                            for j in range(0, int(size))
                        ]

            elif x_coordinate and y_coordinate and type_neighbor and radius:
                output_neighbor, indexes = neighboring_nodes.finding_neighbors(int(radius), type_neighbor, int(x_coordinate), int(y_coordinate))
                grid = [[ (i + int(size) * j, (1 if (i + int(size) * j) in indexes else 0 )) for i in range(0, int(size))] 
                            for j in range(0, int(size))
                        ]
            
            return render(request, "template.html", {"size": size, "debug": debug, 
                                    "matrix": neighboring_nodes.print_matrix, 
                                    "node_coordinates":node_coordinates, 
                                    "index_node_coordinates":index_node_coordinates, 
                                    "output_neighbor":output_neighbor,
                                    "radius" : radius,
                                    "index" : index,
                                    "type_neighbor" : type_neighbor,
                                    "x_coordinate" : x_coordinate,
                                    "y_coordinate" : y_coordinate,
                                    "grid" : grid,
                                    "indexes" : 0 if len(indexes) == 0 else 1
                                    })
        
    return render(request, "template.html", {})


class Node:
    def __init__(self, index, x_coordinate, y_coordinate):
        self.index = index
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def __str__(self):
        return f" x: {self.x_coordinate}, y: {self.y_coordinate}, index: {self.index}"


class NeighboringNodes:
    def __init__(self, size, debug):
        self.size = size
        self.debug = debug
        self.grid = [
                        [ Node(i + size * j, i, j) for i in range(0, size)] 
                            for j in range(0, size)
                    ]
        self.print_matrix = '\n'.join(['   ||   '.join([str(node) for node in row]) 
                    for row in self.grid])

        if self.debug:
            print(self.print_matrix)
            

    def get_node_coordinates(self, index):
        """
        Arguments:
            index: an integer
        Returns:
            The coordinates of a node based on their index
        """
        y_coordinate = index // self.size 
        x_coordinate = index - self.size * y_coordinate 
        return x_coordinate, y_coordinate


    def finding_neighbors(self, radius, type_neighborhood, x_coordinate_or_index, y_coordinate=None):
        """
        Arguments:
            radius: an integer
            type_neighborhood: a string in ["SQUARE", "CROSS", "DIAMOND"]
            x_coordinate_or_index: an integer
            y_coordinate: an integer
        Returns:
            String with the positions of the neighbors (nodes) 
            in the specified neighborhood type-form for the given radius
        """
        if type_neighborhood not in ["SQUARE", "CROSS", "DIAMOND"]:
            return "Neighborhood type not valid", []

        elif radius < 0 or radius > self.size/2:
            return "Neighborhood radius not valid", []

        elif y_coordinate is None:
            x_coordinate, y_coordinate = self.get_node_coordinates(x_coordinate_or_index)
        
        else:
            x_coordinate = x_coordinate_or_index

        if radius + x_coordinate >= self.size or x_coordinate - radius < 0 or radius + y_coordinate >= self.size or y_coordinate - radius < 0:
            return "The radius is too big to draw the neighbor type in that position", []

        print(f"finding_neighbors type {type_neighborhood}, radius {radius}, x {x_coordinate}, y {y_coordinate}")
        
        if type_neighborhood == "SQUARE":
            return self.print_square_neighbors(radius, x_coordinate, y_coordinate)

        if type_neighborhood == "CROSS":
            return self.print_cross_neighbors(radius, x_coordinate, y_coordinate)

        if type_neighborhood == "DIAMOND":
            return self.print_diamond_neighbors(radius, x_coordinate, y_coordinate)


    def print_square_neighbors(self, radius, x_coordinate, y_coordinate):
        """
        Arguments:
            radius: an integer
            x_coordinate: an integer
            y_coordinate: an integer
        Returns:
            - String with the positions of the neighbors (nodes) 
            in the specified neighborhood SQUARE for the given radius
            - Array with indexes of neighbors (nodes) 
            in the specified neighborhood SQUARE for the given radius
            example:
            print_square_neighbors radius 1, x 1, y 1
            output:
                x: 0, y: 1, index: 5
                x: 0, y: 2, index: 10
                x: 1, y: 2, index: 11
                x: 2, y: 2, index: 12
                x: 2, y: 1, index: 7
                x: 2, y: 0, index: 2
                x: 1, y: 0, index: 1
                x: 0, y: 0, index: 0
            [5, 10, 11, 12, 7, 2, 1, 0]
        """
        output = ""
        indexes = []
        stage = 1
        x = x_coordinate
        y = y_coordinate
        
        while radius >= stage:
            # first step go left
            x -= 1
            output += str(self.grid[y][x]) + "\n"
            indexes.append(self.grid[y][x].index)
            print(str(self.grid[y][x]))
            # down
            while y_coordinate + stage > y:
                y += 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            # right
            while x_coordinate + stage> x:
                x += 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            # up
            while y_coordinate - stage < y:
                y -= 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            # left
            while x_coordinate - stage < x:
                x -= 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            
            stage += 1

        return output, indexes
    

    def print_cross_neighbors(self, radius, x_coordinate, y_coordinate):
        """
        Arguments:
            radius: an integer
            x_coordinate: an integer
            y_coordinate: an integer
        Returns:
            - String with the positions of the neighbors (nodes) 
            in the specified neighborhood CROSS for the given radius
            - Array with indexes of neighbors (nodes) 
            in the specified neighborhood CROSS for the given radius
            example:
            print_cross_neighbors radius 1, x 1, y 1
            output:
                x: 1, y: 2, index: 11
                x: 2, y: 1, index: 7
                x: 1, y: 0, index: 1
                x: 0, y: 1, index: 5
            [11, 7, 1, 5]
        """
        output = ""
        indexes = []
        stage = 1
        while radius >= stage:
            # down
            output += str(self.grid[y_coordinate + stage][x_coordinate]) + "\n"
            print(str(self.grid[y_coordinate + stage][x_coordinate]))
            indexes.append(self.grid[y_coordinate + stage][x_coordinate].index)
            # right
            output += str(self.grid[y_coordinate][x_coordinate + stage]) + "\n"
            print(str(self.grid[y_coordinate][x_coordinate + stage]))
            indexes.append(self.grid[y_coordinate][x_coordinate + stage].index)
            # up
            output += str(self.grid[y_coordinate - stage][x_coordinate]) + "\n"
            print(str(self.grid[y_coordinate - stage][x_coordinate]))
            indexes.append(self.grid[y_coordinate - stage][x_coordinate].index)
            # left
            output += str(self.grid[y_coordinate][x_coordinate - stage]) + "\n"
            print(str(self.grid[y_coordinate][x_coordinate - stage]))
            indexes.append(self.grid[y_coordinate][x_coordinate - stage].index)
            
            stage += 1

        return output, indexes


    def print_diamond_neighbors(self, radius, x_coordinate, y_coordinate):
        """
        Arguments:
            radius: an integer
            x_coordinate: an integer
            y_coordinate: an integer
        Returns:
            - String with the positions of the neighbors (nodes) 
            in the specified neighborhood DIAMOND for the given radius
            - Array with indexes of neighbors (nodes) 
            in the specified neighborhood DIAMOND for the given radius
            example:
            print_cross_neighbors radius 2, x 2, y 2
            output:
                x: 1, y: 2, index: 11
                x: 2, y: 3, index: 17
                x: 3, y: 2, index: 13
                x: 2, y: 1, index: 7
                x: 1, y: 1, index: 6
                x: 0, y: 2, index: 10
                x: 1, y: 3, index: 16
                x: 2, y: 4, index: 22
                x: 3, y: 3, index: 18
                x: 4, y: 2, index: 14
                x: 3, y: 1, index: 8
                x: 2, y: 0, index: 2
            [11, 17, 13, 7, 6, 10, 16, 22, 18, 14, 8, 2]
        """
        output = ""
        indexes = []
        stage = 1
        x = x_coordinate
        y = y_coordinate
        
        while radius >= stage:
            # first step go left
            x -= 1
            output += str(self.grid[y][x]) + "\n"
            indexes.append(self.grid[y][x].index)
            print(str(self.grid[y][x]))
            # left down
            while x_coordinate - stage < x:
                x -= 1
                y += 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            # down left
            while y_coordinate + stage > y:
                x += 1
                y += 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            # right up
            while x_coordinate + stage> x:
                x += 1
                y -= 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            # up left
            while y_coordinate - stage < y:
                x -= 1
                y -= 1
                output += str(self.grid[y][x]) + "\n"
                indexes.append(self.grid[y][x].index)
                print(str(self.grid[y][x]))
            
            stage += 1

        return output, indexes
