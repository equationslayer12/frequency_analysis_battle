class Protocol:
    success = "success"
    DELETE_CHAR = "del"
    GAME_ENDED = "end"

    SPLIT = ";"
    
    class Encrypt:
        class Event:
            @staticmethod
            def player_joined(username: str):
                return Protocol.Encrypt.combine("PJ", username)
            
            START_COUNTDOWN = "SC"

        @staticmethod
        def combine(*args):
            return Protocol.SPLIT.join(args)

        @staticmethod
        def opponents(opponents: list):
            return Protocol.Encrypt.combine("UEP", *opponents)

        @staticmethod
        def text_length(text_length: int):
            return str(text_length)

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

    class Request:
        text_length = "len"
            
    class Error:
        empty_request = "ERR.EMPTY"
        invalid_request = "ERR.INVALID"
        user_already_exists = "ERR.USER_ALREADY_EXISTS"


if __name__ == '__main__':
    print(Protocol.Encrypt.combine('hi', 'arg2', 'arg3'))