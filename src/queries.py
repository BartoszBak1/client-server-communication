def query_insert_user(arguments: dict): 

    username = arguments['username']
    password = arguments['password']
    role = arguments['role']
    unread_msgs = arguments['unread_msgs']

    return f"""
    INSERT INTO users (username, password, role, unread_msgs)
    VALUES (%s, %s, %s, %s)
    """, (username, password, role, unread_msgs)

def query_insert_message(arguments: dict):

    sender = arguments['sender']
    receiver = arguments['receiver']
    message = arguments['message']

    return f"""
    INSERT INTO messages (sender_name, receiver_name, message)
    VALUES (%s, %s, %s)
    """, (sender, receiver, message)

def query_check_if_user_exist(arguments: dict):

    username = arguments['username']

    return f"""
    SELECT user_id
    FROM users
    WHERE username = %s
    """, (username, )

def query_get_user_data(arguments: dict):

    username = arguments['username']

    return f"""
    SELECT *
    FROM users
    WHERE username = %s
    """, (username, )

def query_check_user_credentials(arguments: dict):

    username = arguments['username']
    password = arguments['password']

    return f"""
    SELECT *
    FROM users
    WHERE username = %s and password = %s
    """, (username, password)

def query_get_user_messages(arguments: dict):

    receiver = arguments['receiver']

    return f"""
    SELECT sender_name, message
    FROM messages
    WHERE receiver_name = %s
    """, (receiver, )

def query_get_all_messages():

    return f"""
    SELECT sender_name, receiver_name, message
    FROM messages
    """, ()

def query_update_unread_msgs(arguments: dict):

    unread_msgs = arguments['unread_msgs']
    username = arguments['username']

    return f"""
    UPDATE users SET unread_msgs = %s WHERE username = %s
    """, (unread_msgs, username)




