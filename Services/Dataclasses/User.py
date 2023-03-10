from aiogram.filters.state import State


class User(dict):
    ATTRS = ["uid", "inner_name", "is_bot", "first_name", "last_name", "username", "language_code", "email", "sheet_id",
             "permission_id", "state", "categories"]
    DEFAULT_CATEGORIES = ["Еда", "Транспорт", "Жильё", "Разное"]

    def __init__(self, uid: str | int | list | dict = 1,
                 inner_name: str = "",
                 is_bot: bool = False,
                 first_name: str = "EMPTY_VALUE",
                 last_name: str = "EMPTY_VALUE",
                 username: str = "EMPTY_VALUE",
                 language_code: str = "EMPTY_VALUE",
                 email: str = "EMPTY_VALUE",
                 sheet_id: str = "EMPTY_VALUE",
                 permission_id: str = "EMPTY_VALUE",
                 state: State = None,
                 categories: list = [][:]):
        """ Accepts *args or list or dict"""
        if isinstance(uid, int | str):
            self.uid = str(uid)
            self.inner_name = inner_name or "EMPTY_VALUE"
            self.is_bot = is_bot
            self.first_name = first_name
            self.last_name = last_name
            self.username = username
            self.language_code = language_code
            self.email = email
            self.sheet_id = sheet_id
            self.permission_id = permission_id
            self.state = state or dict()
            self.categories = categories
        elif (isinstance(uid, list) and len(User.ATTRS) != len(uid)) or \
                (isinstance(uid, dict) and User.ATTRS != list(uid.keys())):
            raise ValueError(f"Not expected length in initialization, expected {len(User.ATTRS)}, got {len(uid)}")
        elif isinstance(uid, dict):
            self.__dict__ = {key: value for key, value in uid.items()}
        elif isinstance(uid, list):
            self.__dict__ = {User.ATTRS[key]: value for key, value in enumerate(uid)}
        else:
            raise ValueError("Not expected type in initialization")
        super().__init__(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.uid == other.uid
        else:
            return False

    @classmethod
    def __call__(cls, pairs: dict):
        return User(pairs)

    def __iter__(self):
        return iter(self.__dict__.values())

    def __next__(self):
        return next(iter(self))

    def __repr__(self):
        return f"User : {str({key: value for key, value in self.__dict__.items()})}\n"


if __name__ == "__main__":
    u1 = User(1)
    test_1 = User(1)
    test_l = User([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, []])
    test_d = {'uid': 1, 'is_bot': False, 'first_name': 'EMPTY_VALUE', 'last_name': 'EMPTY_VALUE',
              'username': 'EMPTY_VALUE', 'language_code': 'EMPTY_VALUE', 'email': 'EMPTY_VALUE',
              'sheet_id': 'EMPTY_VALUE', 'permission_id': 0, 'state': None, 'categories': []}
    print(test_1)
    print(test_l)
    print(User(test_d))
    print(dict(test_l))
