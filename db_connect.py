import os
import motor.motor_asyncio
import json
import sys

def get_mongodb_client():
    """Get MongoDB client with proper error handling for serverless environment"""
    try:
        # First try to get connection string from environment variable
        connection_string = os.environ.get("MONGODB_URI")
        
        # If not found, try to load from config file
        if not connection_string:
            try:
                # Find the config file
                root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                config_path = os.path.join(root_path, "config.json")
                
                with open(config_path, "r") as config_file:
                    config = json.load(config_file)
                
                # Use the direct connection string if available
                connection_string = config.get("database", {}).get("connection_string")
                
                if not connection_string:
                    # Fall back to building the connection string from parts
                    db_config = config["database"]
                    connection_string = f"mongodb+srv://{db_config['db_username']}:{db_config['db_password']}@{db_config['db_hostname']}/?retryWrites=true&w=majority"
                
                print(f"Using connection string from config file")
            
            except Exception as e:
                print(f"Error loading config: {str(e)}")
                raise Exception(f"Failed to load MongoDB configuration: {str(e)}")
        
        # Create and return the client
        print("Connecting to MongoDB...")
        client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
        
        # Test the connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        return client
        
    except Exception as e:
        print(f"MongoDB connection error: {str(e)}", file=sys.stderr)
        raise Exception(f"MongoDB connection failed: {str(e)}")

# Initialize the client once when the module is loaded
try:
    mongodb_client = get_mongodb_client()
except Exception as e:
    print(f"Failed to initialize MongoDB client: {str(e)}", file=sys.stderr)
    mongodb_client = None