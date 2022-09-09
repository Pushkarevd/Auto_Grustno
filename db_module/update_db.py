def create_update_command(id, timestamp):
    update_command = f"""
    INSERT INTO today_likes VALUES ({id},'{timestamp}')
    """
    return update_command


def check_like(id):
    check_command = f"""
    SELECT * FROM today_likes
    WHERE id='{id}'
    """

    return check_command