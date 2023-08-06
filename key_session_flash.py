import secrets


def key_flash():
    return secrets.token_hex()


if __name__ == '__main__':
    print(key_flash())
