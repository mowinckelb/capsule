"""
Capsule Application Entry Point

This is the main entry point for deployment platforms like Render.
It imports and runs the actual application from the develop/ directory.
"""

import sys
import os
from pathlib import Path

# Add the develop directory to Python path
develop_dir = Path(__file__).parent / "develop"
sys.path.insert(0, str(develop_dir))

# Import and run the main application
if __name__ == "__main__":
    # Change to develop directory for proper module imports
    os.chdir(develop_dir)
    
    # Import the main app
    from app import main
    
    # Run the application
    main()
