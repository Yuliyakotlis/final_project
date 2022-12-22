import uuid


class FullRegInfo:

    def __init__(self):
        self._first_name = 'Имя'
        self._last_name = 'Фамилия'
        self._address = f'{uuid.uuid4()}@mail.ru'
        self._password = 'Pass123!'
        self._password_confirm = 'Pass123!'

    @property
    def first_name(self):
        return self._first_name.capitalize()

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name.capitalize()

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def password_confirm(self):
        return self._password_confirm

    @password_confirm.setter
    def password_confirm(self, value):
        self._password_confirm = value

