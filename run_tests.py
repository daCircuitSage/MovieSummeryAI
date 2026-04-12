#!/usr/bin/env python3
"""
Test Suite for MovieSummeryAI Application
Tests Docker setup, dependencies, and core functionality
"""

import sys
import subprocess
import time
import requests
from pathlib import Path
from typing import Tuple


class TestRunner:
    """Runs comprehensive tests for the MovieSummeryAI Docker setup"""

    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        self.passed_tests = []

    def print_header(self, message: str) -> None:
        """Print test section header"""
        print(f"\n{'='*60}")
        print(f"  {message}")
        print(f"{'='*60}\n")

    def print_test(self, test_name: str, status: str, message: str = "") -> None:
        """Print individual test result"""
        status_symbol = "✅" if status == "PASS" else "❌"
        print(f"{status_symbol} {test_name}")
        if message:
            print(f"   → {message}")

    def test_docker_installed(self) -> bool:
        """Test 1: Check if Docker is installed"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.print_test("Docker Installation", "PASS", result.stdout.strip())
                return True
            else:
                self.print_test("Docker Installation", "FAIL", "Docker command failed")
                return False
        except FileNotFoundError:
            self.print_test("Docker Installation", "FAIL", "Docker not found in PATH")
            return False
        except Exception as e:
            self.print_test("Docker Installation", "FAIL", str(e))
            return False

    def test_docker_compose_installed(self) -> bool:
        """Test 2: Check if Docker Compose is installed"""
        try:
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.print_test("Docker Compose Installation", "PASS", result.stdout.strip())
                return True
            else:
                self.print_test("Docker Compose Installation", "FAIL", "Docker Compose command failed")
                return False
        except FileNotFoundError:
            self.print_test("Docker Compose Installation", "FAIL", "Docker Compose not found in PATH")
            return False
        except Exception as e:
            self.print_test("Docker Compose Installation", "FAIL", str(e))
            return False

    def test_docker_daemon(self) -> bool:
        """Test 3: Check if Docker daemon is running"""
        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.print_test("Docker Daemon Running", "PASS", "Docker daemon is active")
                return True
            else:
                self.print_test("Docker Daemon Running", "FAIL", "Cannot connect to Docker daemon")
                return False
        except Exception as e:
            self.print_test("Docker Daemon Running", "FAIL", str(e))
            return False

    def test_dockerfile_exists(self) -> bool:
        """Test 4: Check if Dockerfile exists"""
        dockerfile_path = Path("Dockerfile")
        if dockerfile_path.exists():
            size = dockerfile_path.stat().st_size
            self.print_test("Dockerfile Presence", "PASS", f"Dockerfile found ({size} bytes)")
            return True
        else:
            self.print_test("Dockerfile Presence", "FAIL", "Dockerfile not found")
            return False

    def test_requirements_exists(self) -> bool:
        """Test 5: Check if requirements.txt exists"""
        req_path = Path("requirements.txt")
        if req_path.exists():
            size = req_path.stat().st_size
            self.print_test("requirements.txt Presence", "PASS", f"Found ({size} bytes)")
            return True
        else:
            self.print_test("requirements.txt Presence", "FAIL", "requirements.txt not found")
            return False

    def test_env_example_exists(self) -> bool:
        """Test 6: Check if .env.example exists"""
        env_path = Path(".env.example")
        if env_path.exists():
            self.print_test(".env.example Presence", "PASS", "Example environment file found")
            return True
        else:
            self.print_test(".env.example Presence", "FAIL", ".env.example not found")
            return False

    def test_docker_compose_file_exists(self) -> bool:
        """Test 7: Check if docker-compose.yml exists"""
        compose_path = Path("docker-compose.yml")
        if compose_path.exists():
            self.print_test("docker-compose.yml Presence", "PASS", "File found")
            return True
        else:
            self.print_test("docker-compose.yml Presence", "FAIL", "docker-compose.yml not found")
            return False

    def test_build_docker_image(self) -> bool:
        """Test 8: Build Docker image"""
        try:
            self.print_test("Docker Image Build", "PASS" if False else "IN_PROGRESS", 
                          "Building image (this may take 2-3 minutes)...")
            result = subprocess.run(
                ["docker", "build", "-t", "movieai:test", "."],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            if result.returncode == 0:
                self.print_test("Docker Image Build", "PASS", "Image built successfully")
                return True
            else:
                error_msg = result.stderr[-200:] if result.stderr else "Unknown error"
                self.print_test("Docker Image Build", "FAIL", f"Build failed: {error_msg}")
                return False
        except subprocess.TimeoutExpired:
            self.print_test("Docker Image Build", "FAIL", "Build timeout (>10 minutes)")
            return False
        except Exception as e:
            self.print_test("Docker Image Build", "FAIL", str(e))
            return False

    def test_image_layers(self) -> bool:
        """Test 9: Verify Docker image layers"""
        try:
            result = subprocess.run(
                ["docker", "inspect", "movieai:test"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.print_test("Docker Image Layers", "PASS", "Image structure valid")
                return True
            else:
                self.print_test("Docker Image Layers", "FAIL", "Cannot inspect image")
                return False
        except Exception as e:
            self.print_test("Docker Image Layers", "FAIL", str(e))
            return False

    def test_container_startup(self) -> bool:
        """Test 10: Start container and verify it runs"""
        container_name = "movieai-test"
        try:
            # Stop any existing container
            subprocess.run(
                ["docker", "stop", container_name],
                capture_output=True,
                timeout=5
            )
            subprocess.run(
                ["docker", "rm", container_name],
                capture_output=True,
                timeout=5
            )

            # Start new container
            result = subprocess.run(
                ["docker", "run", "-d", "--name", container_name, 
                 "-p", "8501:8501", "movieai:test"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Give container time to start
                time.sleep(3)
                
                # Check if container is running
                check = subprocess.run(
                    ["docker", "ps", "--filter", f"name={container_name}"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if container_name in check.stdout:
                    self.print_test("Container Startup", "PASS", "Container running")
                    return True
                else:
                    self.print_test("Container Startup", "FAIL", "Container exited unexpectedly")
                    return False
            else:
                self.print_test("Container Startup", "FAIL", "Failed to start container")
                return False
        except Exception as e:
            self.print_test("Container Startup", "FAIL", str(e))
            return False
        finally:
            # Cleanup
            subprocess.run(["docker", "stop", container_name], capture_output=True)
            subprocess.run(["docker", "rm", container_name], capture_output=True)

    def test_python_dependencies(self) -> bool:
        """Test 11: Verify Python dependencies in Dockerfile"""
        try:
            with open("Dockerfile", "r") as f:
                content = f.read()
                has_streamlit = "streamlit" in content
                has_langchain = "langchain" in content
                has_healthcheck = "HEALTHCHECK" in content
                
                if has_streamlit and has_langchain and has_healthcheck:
                    self.print_test("Python Dependencies", "PASS", 
                                   "Streamlit, LangChain, and health checks configured")
                    return True
                else:
                    missing = []
                    if not has_streamlit: missing.append("Streamlit")
                    if not has_langchain: missing.append("LangChain")
                    if not has_healthcheck: missing.append("HealthCheck")
                    self.print_test("Python Dependencies", "FAIL", f"Missing: {', '.join(missing)}")
                    return False
        except Exception as e:
            self.print_test("Python Dependencies", "FAIL", str(e))
            return False

    def test_security_best_practices(self) -> bool:
        """Test 12: Verify security best practices"""
        try:
            with open("Dockerfile", "r") as f:
                content = f.read()
                has_nonroot_user = "useradd" in content and "USER appuser" in content
                has_slim_image = "python:3.11-slim" in content
                has_healthcheck = "HEALTHCHECK" in content
                
                checks = [
                    ("Non-root user", has_nonroot_user),
                    ("Slim base image", has_slim_image),
                    ("Health check", has_healthcheck)
                ]
                
                all_pass = all(check[1] for check in checks)
                
                msg = "; ".join([f"{check[0]}: {'✓' if check[1] else '✗'}" for check in checks])
                status = "PASS" if all_pass else "FAIL"
                self.print_test("Security Best Practices", status, msg)
                return all_pass
        except Exception as e:
            self.print_test("Security Best Practices", "FAIL", str(e))
            return False

    def test_dockerignore(self) -> bool:
        """Test 13: Check .dockerignore file"""
        try:
            dockerignore_path = Path(".dockerignore")
            if dockerignore_path.exists():
                with open(dockerignore_path, "r") as f:
                    content = f.read()
                    has_venv = "venv" in content or "env" in content
                    has_git = ".git" in content
                    has_pycache = "__pycache__" in content
                    
                    if has_venv and has_git and has_pycache:
                        self.print_test(".dockerignore Presence", "PASS", 
                                       "Contains venv, git, and pycache rules")
                        return True
                    else:
                        self.print_test(".dockerignore Presence", "FAIL", 
                                       "Incomplete ignore rules")
                        return False
            else:
                self.print_test(".dockerignore Presence", "FAIL", ".dockerignore not found")
                return False
        except Exception as e:
            self.print_test(".dockerignore Presence", "FAIL", str(e))
            return False

    def run_all_tests(self) -> Tuple[int, int]:
        """Run all tests and return pass/fail counts"""
        self.print_header("🧪 MovieSummeryAI Docker Setup Test Suite")

        tests = [
            ("Prerequisites", [
                self.test_docker_installed,
                self.test_docker_compose_installed,
                self.test_docker_daemon,
            ]),
            ("Project Files", [
                self.test_dockerfile_exists,
                self.test_requirements_exists,
                self.test_env_example_exists,
                self.test_docker_compose_file_exists,
                self.test_dockerignore,
            ]),
            ("Configuration & Security", [
                self.test_python_dependencies,
                self.test_security_best_practices,
            ]),
            ("Docker Build & Runtime", [
                self.test_build_docker_image,
                self.test_image_layers,
                self.test_container_startup,
            ]),
        ]

        for section, test_list in tests:
            print(f"\n📋 {section}\n")
            for test_func in test_list:
                result = test_func()
                if result:
                    self.passed_tests.append(test_func.__name__)
                else:
                    self.failed_tests.append(test_func.__name__)

        return len(self.passed_tests), len(self.failed_tests)

    def print_summary(self, passed: int, failed: int) -> None:
        """Print test summary"""
        total = passed + failed
        self.print_header("📊 Test Summary")
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed == 0:
            print(f"\n🎉 All tests passed! Your Docker setup is ready.\n")
            print("Next Steps:")
            print("1. Configure .env file with your API keys")
            print("2. Run: docker-compose up")
            print("3. Access the app at http://localhost:8501")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please review above.\n")


def main():
    """Main test runner"""
    runner = TestRunner()
    passed, failed = runner.run_all_tests()
    runner.print_summary(passed, failed)
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
