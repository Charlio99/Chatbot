NODE_FOOD = 0
NODE_STORE = 0
NODE_ENTERTAINMENT = 0
NODE_HEALTH = 0
NODE_TOURISM = 0


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
        self.activities.append(Category('Food', '🥪', NODE_FOOD))
        self.activities.append(Category('Store', '🛍', NODE_STORE))
        self.activities.append(Category('Entertainment', '🎞 🏋 🎳', NODE_ENTERTAINMENT))
        self.activities.append(Category('Health', '🧖‍ ️🏞', NODE_HEALTH))
        self.activities.append(Category('Tourism', '🗺', NODE_TOURISM))
        pass

    def get_node(self, name):

        for activity in self.activities:
            if name == activity.name:
                return activity.node

        return False

    def get_activities(self):
        return self.activities
