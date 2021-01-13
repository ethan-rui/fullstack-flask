import uuid
from data import Entry, Database
import os

basedir = os.getcwd()


class Inquiry(Entry):
    def __init__(
        self,
        sender_email: str,
        sender_name: str,
        subject: str,
        content: str,
    ):
        super().__init__(uid=None)
        self.__sender_name = sender_name
        self.__sender_email = sender_email
        self.__subject = subject
        self.__content = content
        self.status = True
        """status denotes whether the ticket is open"""

    @property
    def sender_name(self):
        return self.__sender_name

    @property
    def sender_email(self):
        return self.__sender_email

    @property
    def subject(self):
        return self.__subject

    @property
    def content(self):
        return self.__content


class TableInquiry(Database):
    def __init__(self):
        label = "inquiries"
        super().__init__(label)
        self.label = label