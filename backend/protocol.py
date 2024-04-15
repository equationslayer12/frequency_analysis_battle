class Protocol:
    success = True
    DELETE_CHAR = "del"
    GAME_ENDED = "end"
    
    class Encrypt:
        @staticmethod
        def combine(*args):
            return ";".join(args)

        @staticmethod
        def change_letter(score: int) -> str:
            """change letter response.

            Args:
                score (int): how many letters have the user guessed.

            Returns:
                _type_: str
            """
            return str(score)

    class Decrypt:
        @staticmethod
        def seperate_to_fields(request: str):
            return request.split(";")

        @staticmethod
        def change_letter(fields: list):
            if len(fields) != 2:
                return None
            from_letter, to_letter = fields
            return from_letter, to_letter
    
    class Command:
        change_letter = "CL"
        new_text = "new"
    class Error:
        empty_request = "ERR.EMPTY"
        invalid_request = "ERR.INVALID"
        user_already_exists = "ERR.USER_ALREADY_EXISTS"


if __name__ == '__main__':
    print(Protocol.Encrypt.combine('hi', 'arg2', 'arg3'))