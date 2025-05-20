import psycopg2
from config import load_config


def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(5) NOT NULL,
            unread_msgs INTEGER NOT NULL
        );
        """,
        """ 
        DROP TABLE IF EXISTS messages;
        CREATE TABLE messages (
            msg_id SERIAL PRIMARY KEY,
            sender_name VARCHAR(255) NOT NULL,
            receiver_name VARCHAR(255) NOT NULL,
            message VARCHAR(255)
        );

        INSERT INTO users (username, password, role, unread_msgs)
        VALUES 
        ('user1', '1234', 'user', 0),
        ('user2', '1234', 'admin', 0),
        ('user3', '1234', 'user', 5),
        ('user4', '1234', 'user', 2);

        INSERT INTO messages (sender_name, receiver_name, message)
        VALUES
        ('user1', 'user3', 'msg1'),
        ('user1', 'user3', 'msg2'),
        ('user1', 'user3', 'msg3'),
        ('user1', 'user3', 'msg4'),
        ('user1', 'user3', 'msg5'),
        ('user1', 'user4', 'msg1'),
        ('user2', 'user4', 'msg2');        
        """
        )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
if __name__ == '__main__':
    create_tables()

    # & "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres
    # \c client_server_db
    # \dt
    # \d users