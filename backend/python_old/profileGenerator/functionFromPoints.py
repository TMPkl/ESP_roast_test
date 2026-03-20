class curveFunction:
    def __init__(self, points):
        '''
        Docstring for __init__
        
        :param self: Description
        :param points: list of points
        '''
        self.points = points
        self.func_is_generated = False
        self.func = None
    
    
    def add_point(self, point):
        '''
        Docstring for add_point
        
        :param self: Description
        :param point: point to add
        '''
        if point not in self.points:
            self.points.append(point)
            self.func_is_generated = False
        else:
            print("Point already exists in the list.")
            

    def remove_point(self, point):
        '''
        Docstring for remove_point
        
        :param self: Description
        :param point: point to remove
        '''
        if point in self.points:
            self.points.remove(point)
            self.func_is_generated = False
        else:
            print("Point not found in the list.")


    def generate_function(self):
        '''
        Docstring for generate_function
        
        :param self: Description
        :return: function generated from the points
        '''
        if len(self.points) < 2:
            raise ValueError("At least two points are required to generate a function.")
        
        self.points.sort(key=lambda p: p[0])
        
        def func(x):
            if x <= self.points[0][0]:
                return self.points[0][1]
            if x >= self.points[-1][0]:
                return self.points[-1][1]
            
            for i in range(len(self.points) - 1):
                p_i, p_next = self.points[i], self.points[i + 1]
                if p_i[0] <= x <= p_next[0]:
                    t = (x - p_i[0]) / (p_next[0] - p_i[0])
                    return (1 - t) * p_i[1] + t * p_next[1]
        self.func = func
        self.func_is_generated = True

        return func
    
if __name__ == "__main__":
    points = [(0, 0), (1, 2), (2, 1)]
    curve = curveFunction(points)
    func = curve.generate_function()
    
    import matplotlib.pyplot as plt
    import numpy as np

    x_values = np.linspace(-1, 3, 100)
    y_values = [func(x) for x in x_values]
    plt.plot(x_values, y_values)
    plt.scatter(*zip(*points), color='red')
    plt.title("Function Generated from Points")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid()
    plt.show()