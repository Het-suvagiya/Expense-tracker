import oracledb
import os
import re

# Try to initialize thick mode for Oracle 11g XE
try:
    oracledb.init_oracle_client()
except:
    pass

# Oracle connection parameters
ORACLE_HOST = "localhost"
ORACLE_PORT = 1521
ORACLE_SID = "xe"
ORACLE_USER = "system"
ORACLE_PASSWORD = "admin"

def get_connection():
    """
    Connect to Oracle 11g XE database.
    Returns a connection object.
    """
    try:
        dsn = oracledb.makedsn(ORACLE_HOST, ORACLE_PORT, ORACLE_SID)
        connection = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def _convert_params(query, params):
    """Convert positional parameters (:1, :2) to oracledb named parameters (:p0, :p1)"""
    if not params or not isinstance(params, list):
        return query, params
    
    # Find all :number or :name parameters
    param_names = re.findall(r':([a-zA-Z_]\w*|\d+)', query)
    if not param_names:
        return query, params
    
    if param_names[0].isdigit():
        # Positional parameters (:1, :2, etc.)
        # Track unique parameters in order
        seen = {}
        ordered_params = []
        for name in param_names:
            if name not in seen:
                seen[name] = True
                ordered_params.append(name)
        
        # Sort by numeric value
        ordered_params.sort(key=lambda x: int(x))
        
        # Replace :1, :2, etc. with :p0, :p1, etc.
        for i, name in enumerate(ordered_params):
            query = query.replace(f':{name}', f':p{i}')
        
        # Build param dict from params list
        params = {f'p{i}': params[i] for i in range(len(params))}
    
    return query, params

def run_query(query, params=None):
    """
    Execute a SELECT query and return results as a list of dictionaries.
    """
    connection = get_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        
        # Convert parameters if needed
        query, params = _convert_params(query, params)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch all rows and convert to dictionaries
        rows = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            rows.append(row_dict)
        
        cursor.close()
        connection.close()
        return rows
    except Exception as e:
        print(f"Query error: {e}")
        try:
            cursor.close()
            connection.close()
        except:
            pass
        return []

def run_command(query, params=None):
    """
    Execute INSERT, UPDATE, or DELETE query.
    """
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Convert parameters if needed
        query, params = _convert_params(query, params)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Command error: {e}")
        try:
            connection.rollback()
            cursor.close()
            connection.close()
        except:
            pass
        return False
