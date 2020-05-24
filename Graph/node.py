class Route:

    def __init__(self, name, next_step, end, key):
        self.name = name
        self.next_step = next_step
        self.end = end
        self.key = key


class NodeGraph:

    def __init__(self, num, question, photo, gif, left_name, left_next_step, left_end, left_key, right_name,
                 right_next_step, right_end, right_key):

        self.num = num
        self.question = question

        if len(photo) == 0:
            photo = None

        self.photo = photo

        if len(gif) == 0:
            gif = None

        self.gif = gif
        self.left = Route(left_name, left_next_step, left_end, left_key)
        self.right = Route(right_name, right_next_step, right_end, right_key)

    def get_left_name(self):
        return self.left.name

    def get_left_next_step(self):
        return self.left.next_step

    def get_left_key(self):
        return self.left.key

    def get_right_name(self):
        return self.right.name

    def get_right_next_step(self):
        return self.right.next_step

    def get_right_key(self):
        return self.right.key
