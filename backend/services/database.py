"""
Supabase database service using direct PostgreSQL connection
More reliable than Supabase Python client - uses psycopg2
"""
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connection pool
connection_pool: Optional[SimpleConnectionPool] = None

def get_db_connection():
    """Get database connection from pool"""
    global connection_pool
    
    if connection_pool is None:
        return None
    
    try:
        return connection_pool.getconn()
    except Exception as e:
        print(f"❌ Error getting connection from pool: {e}")
        return None

def return_db_connection(conn):
    """Return connection to pool"""
    global connection_pool
    if connection_pool and conn:
        try:
            connection_pool.putconn(conn)
        except:
            pass

def init_database_connection():
    """Initialize PostgreSQL connection pool"""
    global connection_pool
    
    if connection_pool is not None:
        return True
    
    # Use DATABASE_URL (direct PostgreSQL connection string from Supabase)
    if DATABASE_URL:
        try:
            connection_pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=DATABASE_URL
            )
            # Test connection
            conn = get_db_connection()
            if conn:
                conn.close()
                return_db_connection(conn)
                print("✅ Connected to Supabase PostgreSQL database")
                return True
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            connection_pool = None
            return False
    
    # If DATABASE_URL not set, show helpful message
    if SUPABASE_URL:
        print("⚠️  DATABASE_URL not set in .env")
        print("💡 Get your connection string from:")
        print("   Supabase Dashboard → Settings → Database → Connection String")
        print("   Use the 'URI' format: postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres")
    else:
        print("⚠️  Database not configured. Using in-memory storage.")
    
    return False

def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return results"""
    from decimal import Decimal
    
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
            # Convert Decimal to float for JSON serialization
            converted_results = []
            for row in results:
                row_dict = dict(row)
                # Convert Decimal values to float
                for key, value in row_dict.items():
                    if isinstance(value, Decimal):
                        row_dict[key] = float(value)
                converted_results.append(row_dict)
            return converted_results
    except Exception as e:
        print(f"❌ Query error: {e}")
        return []
    finally:
        return_db_connection(conn)

def execute_insert(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """Execute an INSERT query and return the inserted row"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            conn.commit()
            # Get the inserted row
            cur.execute("SELECT * FROM activities WHERE id = %s", (cur.lastrowid,))
            result = cur.fetchone()
            return dict(result) if result else None
    except Exception as e:
        conn.rollback()
        print(f"❌ Insert error: {e}")
        return None
    finally:
        return_db_connection(conn)

def execute_insert_returning(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """Execute INSERT with RETURNING clause"""
    from decimal import Decimal
    
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            result = cur.fetchone()
            conn.commit()
            if result:
                result_dict = dict(result)
                # Convert Decimal values to float
                for key, value in result_dict.items():
                    if isinstance(value, Decimal):
                        result_dict[key] = float(value)
                return result_dict
            return None
    except Exception as e:
        conn.rollback()
        print(f"❌ Insert error: {e}")
        return None
    finally:
        return_db_connection(conn)

# Initialize connection on import
init_database_connection()
