NODE_FOOD = 17
NODE_STORE = 2
NODE_ENTERTAINMENT = 2
NODE_HEALTH = 2
NODE_TOURISM = 2
NODE_NO_SE = 0


class Category:

    def __init__(self, name, emoji, node):
        self.name = name
        self.emoji = emoji
        self.node = node


class Categories:

    __instance = None

    @staticmethod
    def getInstance():
        if Categories.__instance is None:
            Categories()
        return Categories.__instance

    def __init__(self):
        Categories.__instance = self
        self.activities = []
        self.activities.append(Category('Comida', '🥪', NODE_FOOD))
        self.activities.append(Category('Tienda', '🛍', NODE_STORE))
        self.activities.append(Category('Entretenimiento', '🎞 🏋 🎳', NODE_ENTERTAINMENT))
        self.activities.append(Category('Salud', '🧖‍ ️🏞', NODE_HEALTH))
        self.activities.append(Category('Turismo', '🗺', NODE_TOURISM))
        self.activities.append(Category("No lo se", '🤷‍♂️', NODE_NO_SE))
        pass

    def get_node(self, name):

        for activity in self.activities:
            if name == activity.name:
                return activity.node

        return False

    def get_activities(self):
        return self.activities
