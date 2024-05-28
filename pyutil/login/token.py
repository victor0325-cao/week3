import jwt


def gen_token(name, user_id, timestamp, key):
    token_dict = {
        'user_id': user_id,
        'name': name,
        'timestamp': timestamp,
    }

    token = jwt.encode(token_dict, key)

    return token


def parse_token(token, key):
    return jwt.decode(token, key, algorithms="HS256")


