from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        Search for a password by username.
        Return the password if found.

        :param username:
        :return:
        """

    @classmethod
    def check_passwords_match(cls, password1: str, password2: str) -> bool:
        """
        Check passwords for matches.

        :param password1:
        :param password2:
        :return:
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        Check if the password is valid.

        :param username:
        :param password:
        :return:
        """

        db_password = self.get_user_password(username)

        if db_password is None:
            return False
        return self.check_passwords_match(
            password1=db_password,
            password2=password,
        )
