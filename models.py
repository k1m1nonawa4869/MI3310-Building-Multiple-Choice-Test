# models.py

class User:
    """
    Represents a user account. Passwords are stored in plain text for now.
    """

    def __init__(self, username, password, name, admin=False, verified=False):
        self.username = username
        self.password = password       # plain text
        self.name = name               # uses JSON key "name"
        self.admin = admin             # uses JSON key "admin"
        self.verified = verified       # uses JSON key "verified"

    @classmethod
    def create(cls, username, plaintext_password, name, admin=False):
        """
        Factory: return a new User instance with a plain-text password.
        """
        return cls(username, plaintext_password, name, admin, verified=False)

    def to_dict(self):
        """
        Serialize back to the same key names your JSON expects.
        """
        return {
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "admin": self.admin,
            "verified": self.verified
        }

    @classmethod
    def from_dict(cls, data):
        """
        Read from JSON entries that have keys:
          - "username"
          - "password"
          - "name"
          - "admin"
          - "verified"
        """
        return cls(
            username=data.get("username", ""),
            password=data.get("password", ""),
            name=data.get("name", ""),
            admin=data.get("admin", False),
            verified=data.get("verified", False)
        )


class Question:
    """
    Represents a question with 4 possible answers.

    JSON keys:
      - "ID"           (may be a number in JSON, but we always cast it to string internally)
      - "question"
      - "answer"       (list of 4 choices)
      - "rightanswer"  (one of "A"/"B"/"C"/"D")
      - "level"        ("BIẾT", "HIỂU", "VẬN DỤNG THẤP", or "VẬN DỤNG CAO")
    """

    VALID_LEVELS = {"BIẾT", "HIỂU", "VẬN DỤNG THẤP", "VẬN DỤNG CAO"}

    def __init__(self, qid, text, options, correct_option, level):
        # Force ID to be a string internally, even if JSON had it as a number.
        self.id = str(qid)
        self.text = text
        self.options = options              # list of exactly 4 strings
        self.correct_option = correct_option  # "A","B","C","D"
        self.level = level

    @classmethod
    def from_dict(cls, data):
        """
        When loading from JSON, data["ID"] might be an int. We cast it to str in __init__,
        so self.id always becomes a string.
        """
        return cls(
            qid=data["ID"],
            text=data["question"],
            options=[
                data["answer"][0],
                data["answer"][1],
                data["answer"][2],
                data["answer"][3]
            ],
            correct_option=data["rightanswer"],
            level=data["level"]
        )

    def to_dict(self):
        """
        When saving back to JSON, convert the string ID back to an integer if possible.
        Otherwise, leave it as a string.
        """
        try:
            # If self.id consists of digits only, cast back to int
            id_as_int = int(self.id)
        except ValueError:
            id_as_int = self.id  # leave as string if not purely numeric

        return {
            "ID": id_as_int,
            "question": self.text,
            "answer": [
                self.options[0],
                self.options[1],
                self.options[2],
                self.options[3]
            ],
            "rightanswer": self.correct_option,
            "level": self.level
        }
