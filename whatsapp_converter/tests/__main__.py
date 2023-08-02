import os
import sys
import unittest

if __name__ == "__main__":
    # Get the current directory (where this file is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the relative path to your project directory
    project_dir = os.path.join(current_dir, "..")  # Adjust ".." based on your project's directory structure
    sys.path.append(project_dir)

    # Import and run the tests
    from test_parse import TestParse

    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestParse)
    unittest.TextTestRunner().run(test_suite)