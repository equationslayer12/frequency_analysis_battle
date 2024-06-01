from typing import List


class Protocol:
    success = "success"
    DELETE_CHAR = "del"
    FINISHED: int = -1
    GAME_ENDED = "end"

    SPLIT = ";"

    class Encrypt:
        class Event:
            START_COUNTDOWN = "SC"
            UPDATE_SCORE = "US"

            @staticmethod
            def player_joined(username: str, user_id: int):
                return Protocol.Encrypt.combine("PJ", username, str(user_id))

            @staticmethod
            def player_left(user_id: int):
                return Protocol.Encrypt.combine("PJ", user_id)

            @staticmethod
            def change_letter_in_race(player_id: int, score: int) -> str:
                """change letter response.

                Args:
                    score (int): how many letters have the user guessed.

                Returns:
                    _type_: str
                """
                return Protocol.Encrypt.combine(
                    Protocol.Encrypt.Event.UPDATE_SCORE,
                    player_id,
                    score
                )

        @staticmethod
        def combine(*args):
            return Protocol.SPLIT.join(args)

        @staticmethod
        def opponents(opponents_usernames: List[str], opponents_user_ids):
            response = []
            for username, user_id in zip(opponents_usernames, opponents_user_ids):
                response.append(Protocol.Encrypt.combine(
                    username, str(user_id)))

            return Protocol.Encrypt.combine("UEP", *response)

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

        @staticmethod
        def finished():
            return str(Protocol.FINISHED)

        @staticmethod
        def sync(user_ids: List[str], scores: List[int], game_status: str) -> str:
            """response to player's request to get the lobby's state. a response should look like:
            game_status;id1;score;id2;score;...

            * score may be Protocol.FINISHED

            Args:
                user_ids (List[str]): list of user ids
                scores (List[int]): list of scores (should be corresponding with user ids)
                game_status (str): game.status

            Returns:
                str: response
            """
            response = game_status
            for user_id, score in zip(user_ids, scores):
                response += f"{Protocol.SPLIT}{user_id}{Protocol.SPLIT}{score}"

            return response

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
        text = "text"
        sync = "sync"

    class Error:
        empty_request = "ERR.EMPTY"
        invalid_request = "ERR.INVALID"
        user_already_exists = "ERR.USER_ALREADY_EXISTS"
        not_in_game = "ERR.NOT_IN_GAME"


if __name__ == '__main__':
    print(Protocol.Encrypt.combine('hi', 'arg2', 'arg3'))
