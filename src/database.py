import psycopg2
from psycopg2.extras import RealDictCursor

class Database():
    def __init__(self, config) -> None:
        self.config = config 
        self.conn = self.connect(config)

    def connect(self, config):
        """ Connect to the PostgreSQL database server """
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**config) as conn:
                print('Connected to the PostgreSQL server.')
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            
    def save_data(self, params:dict):
 
        """Execute query.

        Args:
            query (string): query
        """
        import src.queries as queries
        query, values = getattr(queries, params['query'])(params['query_arguments'])

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            self.conn.commit()

    def get_data(self, params: dict):
        """Get data from database.

        Args:
            query (str): query
            params (dict): dictionary with parameters for query.
        Returns:
            _type_: data
        """
        import src.queries as queries

        if params['query'] == "query_get_all_messages":
            query, values = getattr(queries, params['query'])()
        else:
            query, values = getattr(queries, params['query'])(params['query_arguments'])

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            data = cur.fetchall()
            cur.close()
        return data
    
    def check_data(self, params: dict):
        """Check data if exist.

        Args:
            query (str): query
            params (dict): {query: query_name, query_arguments: dict} dictionary with parameters for query.

        Returns:
            bool: True if exist or False if not
        """
        import src.queries as queries

        query, values = getattr(queries, params['query'])(params['query_arguments'])

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            data = cur.fetchone()

            cur.close()
        return data is not None
