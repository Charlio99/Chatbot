class Route:

    def __init__(self, name, next_step, end, key, photo):
        self.name = name
        self.next_step = next_step
        self.end = end
        self.key = key
        self.photo = photo


class NodeGraph:

    def __init__(self, num, question, left_name, left_next_step, left_end, left_key, left_photo, right_name,
                 right_next_step, right_end, right_key, right_photo):

        self.num = num
        self.question = question

        if len(left_photo) == 0:
            left_photo = None

        if len(right_photo) == 0:
            right_photo = None

        self.left = Route(left_name, left_next_step, left_end, left_key, left_photo)
        self.right = Route(right_name, right_next_step, right_end, right_key, right_photo)

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
