import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
from work import work

class TestBuildScript(unittest.TestCase):
    
    @patch("subprocess.run")
    @patch("os.chmod")
    def test_successful_compile_and_run(self, mock_chmod, mock_subprocess):
        """Test when compilation and execution are successful."""
        # Mock build() function from build_c module
        with patch("build_c.build", return_value=0):
            # Mock the 'pwd' command
            mock_pwd = MagicMock()
            mock_pwd.returncode = 0
            mock_pwd.stdout = "/home/user/project"
            mock_pwd.stderr = ""

            # Mock the compilation subprocess
            mock_compile = MagicMock()
            mock_compile.returncode = 0
            mock_compile.stdout = "Compilation successful."
            mock_compile.stderr = ""

            # Mock the execution subprocess
            mock_run = MagicMock()
            mock_run.returncode = 0
            mock_run.stdout = "Execution successful."
            mock_run.stderr = ""

            # Configure mock_subprocess to return values in order: pwd → compile → run
            mock_subprocess.side_effect = [mock_pwd, mock_compile, mock_run]

            result = work()
            print("work result", result)
            
            self.assertTrue(result["compile"])
            self.assertTrue(result["run"])
    
    @patch("subprocess.run")
    @patch("os.chmod")
    def test_compile_fail(self, mock_chmod, mock_subprocess):
        """Test when compilation and execution are successful."""
        # Mock build() function from build_c module
        with patch("build_c.build", return_value=0):
            # Mock the 'pwd' command
            mock_pwd = MagicMock()
            mock_pwd.returncode = 0
            mock_pwd.stdout = "/home/user/project"
            mock_pwd.stderr = ""

            # Mock the compilation subprocess
            mock_compile = MagicMock()
            mock_compile.returncode = 1
            mock_compile.stdout = "Compilation failed."
            mock_compile.stderr = "Fail"

            # Configure mock_subprocess to return values in order: pwd → compile
            mock_subprocess.side_effect = [mock_pwd, mock_compile]

            result = work()
            print("work result", result)
            
            self.assertFalse(result["compile"])
            
    @patch("subprocess.run")
    @patch("os.chmod")
    def test_compile_and_run_fail(self, mock_chmod, mock_subprocess):
        """Test when compilation and execution are successful."""
        # Mock build() function from build_c module
        with patch("build_c.build", return_value=0):
            # Mock the 'pwd' command
            mock_pwd = MagicMock()
            mock_pwd.returncode = 0
            mock_pwd.stdout = "/home/user/project"
            mock_pwd.stderr = ""

            # Mock the compilation subprocess
            mock_compile = MagicMock()
            mock_compile.returncode = 0
            mock_compile.stdout = "Compilation successful."
            mock_compile.stderr = ""

            # Mock the execution subprocess
            mock_run = MagicMock()
            mock_run.returncode = 1
            mock_run.stdout = "Execution fail."
            mock_run.stderr = "fail"



            # Configure mock_subprocess to return values in order: pwd → compile → run
            mock_subprocess.side_effect = [mock_pwd, mock_compile, mock_run]

            result = work()
            print("work result", result)
            
            self.assertTrue(result["compile"])
            self.assertFalse(result["run"])

    @patch("subprocess.run")
    @patch("os.chmod")
    def test_infinite_loop(self, mock_chmod, mock_subprocess):
        """Test when compilation and execution are successful."""
        # Mock build() function from build_c module
        with patch("build_c.build", return_value=0):
            # Mock the 'pwd' command
            mock_pwd = MagicMock()
            mock_pwd.returncode = 0
            mock_pwd.stdout = "/home/user/project"
            mock_pwd.stderr = ""

            # Mock the compilation subprocess
            mock_compile = MagicMock()
            mock_compile.returncode = 0
            mock_compile.stdout = "Compilation successful."
            mock_compile.stderr = ""

            mock_subprocess.side_effect = [
            mock_pwd,        # First call (pwd)
            mock_compile,    # Second call (compile.sh)
            subprocess.TimeoutExpired(cmd="./run.sh", timeout=5)  # Third call (run.sh) → Timeout
            ]

            result = work()
            print("work result", result)
            
            self.assertTrue(result["compile"])
            self.assertFalse(result["run"])
            self.assertEqual(result["output"], "Timeout")

 

if __name__ == "__main__":
    unittest.main()
