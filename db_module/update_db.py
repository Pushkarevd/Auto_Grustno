def create_update_command(id: int, timestamp, name: str):
    update_command = f"""
    INSERT INTO likes VALUES ({id},'{timestamp}', '{name}')
    """
    return update_command


def check_like(id: int):
    check_command = f"""
    SELECT * FROM likes
    WHERE id='{id}'
    """

    return check_command