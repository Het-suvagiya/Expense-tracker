from database import get_connection

def create_tables():
    """
    Create all tables for ExpenseDesk application.
    """
    connection = get_connection()
    if not connection:
        print("Failed to connect to database")
        return
    
    cursor = connection.cursor()
    
    try:
        # Create sequences
        sequences = [
            "CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1",
            "CREATE SEQUENCE categories_seq START WITH 1 INCREMENT BY 1",
            "CREATE SEQUENCE expenses_seq START WITH 1 INCREMENT BY 1"
        ]
        
        for seq in sequences:
            try:
                seq_name = seq.split()[2]
                # Try to drop if exists
                try:
                    cursor.execute(f"DROP SEQUENCE {seq_name}")
                    print(f"✓ Sequence dropped: {seq_name}")
                except:
                    pass  # Sequence might not exist, that's OK
                
                # Create new sequence
                cursor.execute(seq)
                print(f"✓ Sequence created: {seq_name}")
            except Exception as e:
                if "already exists" not in str(e):
                    print(f"⚠ Sequence {seq.split()[2]}: {e}")
        
        # Create USERS table
        try:
            cursor.execute("""
                CREATE TABLE USERS (
                    USER_ID NUMBER PRIMARY KEY,
                    USERNAME VARCHAR2(50) NOT NULL UNIQUE,
                    PASSWORD VARCHAR2(50) NOT NULL,
                    FULL_NAME VARCHAR2(100)
                )
            """)
            print("✓ USERS table created")
        except Exception as e:
            if "already exists" in str(e):
                print("✓ USERS table already exists")
            else:
                raise
        
        # Create CATEGORIES table
        try:
            cursor.execute("""
                CREATE TABLE CATEGORIES (
                    CAT_ID NUMBER PRIMARY KEY,
                    CAT_NAME VARCHAR2(100) NOT NULL,
                    ICON VARCHAR2(50),
                    COLOR VARCHAR2(20),
                    DESCRIPTION VARCHAR2(200)
                )
            """)
            print("✓ CATEGORIES table created")
        except Exception as e:
            if "already exists" in str(e):
                print("✓ CATEGORIES table already exists")
            else:
                raise
        
        # Create EXPENSES table
        try:
            cursor.execute("""
                CREATE TABLE EXPENSES (
                    EXP_ID NUMBER PRIMARY KEY,
                    USER_ID NUMBER NOT NULL,
                    CAT_ID NUMBER NOT NULL,
                    AMOUNT NUMBER(12,2) NOT NULL,
                    EXP_DATE DATE DEFAULT SYSDATE,
                    DESCRIPTION VARCHAR2(500),
                    EXP_TYPE VARCHAR2(20),
                    STATUS VARCHAR2(20),
                    NOTES VARCHAR2(500),
                    FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID),
                    FOREIGN KEY (CAT_ID) REFERENCES CATEGORIES(CAT_ID)
                )
            """)
            print("✓ EXPENSES table created")
        except Exception as e:
            if "already exists" in str(e):
                print("✓ EXPENSES table already exists")
            else:
                raise
        
        
        connection.commit()
        
        # Insert sample data
        print("\n--- Inserting sample data ---")
        
        # Check if admin user exists
        cursor.execute("SELECT COUNT(*) as cnt FROM USERS WHERE USERNAME='admin'")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Insert default user
            cursor.execute(
                "INSERT INTO USERS VALUES (users_seq.NEXTVAL, :1, :2, :3)",
                ['admin', 'admin123', 'Admin User']
            )
            print("✓ Admin user created")
        else:
            print("✓ Admin user already exists")
        
        # Insert categories
        cursor.execute("SELECT COUNT(*) as cnt FROM CATEGORIES")
        cat_count = cursor.fetchone()[0]
        
        if cat_count == 0:
            categories = [
                ('Food & Dining', '🍽', '#006c49', 'Groceries and restaurants'),
                ('Transport', '🚗', '#004ac6', 'Fuel and travel'),
                ('Rent & Home', '🏠', '#ab0b1c', 'Rent and utilities'),
                ('Entertainment', '🎬', '#737686', 'Movies and hobbies'),
                ('Healthcare', '🏥', '#006c49', 'Medical expenses'),
                ('Shopping', '🛒', '#004ac6', 'Clothes and gadgets'),
                ('Other', '📌', '#434655', 'Miscellaneous')
            ]
            
            for cat in categories:
                cursor.execute(
                    "INSERT INTO CATEGORIES VALUES (categories_seq.NEXTVAL, :1, :2, :3, :4)",
                    cat
                )
                print(f"✓ Category added: {cat[0]}")
        else:
            print(f"✓ Categories already exist ({cat_count} found)")
        
        connection.commit()
        print("\n✅ Database setup done!")
        
    except Exception as e:
        error_msg = str(e).lower()
        if "already exists" in error_msg or "ora-00955" in error_msg or "ora-01408" in error_msg:
            print("✓ Tables already exist - skipping creation")
            print("✅ Database setup complete!")
        else:
            print(f"Error: {e}")
            connection.rollback()
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Setting up ExpenseDesk database...")
    create_tables()
