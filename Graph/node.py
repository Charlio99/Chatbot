class Route:

    def __init__(self, name, next_step):
        self.name = name
        self.next_step = next_step


class NodeGraph:

    def __init__(self, num, question, left_name, left_next_step, right_name, right_next_step):
        self.num = num
        self.question = question
        self.left = Route(left_name, left_next_step)
        self.right = Route(right_name, right_next_step)

    def get_left_name(self):
        return self.left.name

    def get_left_next_step(self):
        return self.left.next_step

    def get_right_name(self):
        return self.right.name

    def get_right_next_step(self):
        return self.right.next_step
