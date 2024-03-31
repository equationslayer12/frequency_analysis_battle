class Protocol:
    success = True

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
    
    class Error:
        empty_request = "ERR.EMPTY"
        invalid_request = "ERR.INVALID"
        user_already_exists = "ERR.USER_ALREADY_EXISTS"
    