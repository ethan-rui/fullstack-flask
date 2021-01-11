from data import Entry, Database
import os
import os.path

basedir = os.getcwd()


class Inquiry(Entry):
    def __init__(
        self,
        name: str,
        email: str = "",
        subject: str = "subject",
        msg: str = "message",
        uid: str = None,
    ):
        super().__init__(uid)
        self.name = name
        self.email=email
        self.subject=subject
        self.msg=msg

class TableInquiry(Database):
    def __init__(self):
        label = "inquiries"
        super().__init__(label)
        self.label = label