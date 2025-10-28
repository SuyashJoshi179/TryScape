"""
TryScape Application Entry Point
"""
from app.app import create_app
from app.config import Config

if __name__ == '__main__':
    try:
        # Validate configuration
        Config.validate()

        # Create and run app
        app = create_app()
        # Respect optional env/config values for host/port
        host = getattr(Config, 'FLASK_RUN_HOST', '0.0.0.0')
        port = getattr(Config, 'FLASK_RUN_PORT', 5000)
        app.run(host=host, port=port, debug=Config.DEBUG)
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your Azure OpenAI credentials")
        print("3. Run the application again")
