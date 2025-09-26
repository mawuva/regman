# mypy: ignore-errors

"""
Script to run all regman examples with detailed reporting.
"""

import sys
import time
import traceback
import subprocess
from pathlib import Path
from typing import Dict, List, Any


class ExampleRunner:
    """Example runner with detailed reporting."""

    def __init__(self) -> None:
        self.examples_dir = Path(__file__).parent
        self.results: List[Dict[str, Any]] = []
        self.start_time = time.time()

    def find_examples(self) -> List[Path]:
        """Finds all Python example files."""
        examples = []
        for file_path in self.examples_dir.glob("*.py"):
            if file_path.name != "run_all_examples.py":
                examples.append(file_path)
        return sorted(examples)

    def run_example(self, example_path: Path) -> Dict[str, Any]:
        """Runs an example and returns the results."""
        example_name = example_path.stem
        start_time = time.time()

        print(f"🔄 Running {example_name}...")

        try:
            # Execution with poetry
            result = subprocess.run(
                ["poetry", "run", "python", str(example_path)],
                capture_output=True,
                text=True,
                cwd=example_path.parent.parent,
            )

            end_time = time.time()
            duration = end_time - start_time

            if result.returncode == 0:
                # Display example output
                if result.stdout:
                    print(result.stdout)

                result_dict = {
                    "name": example_name,
                    "status": "SUCCESS",
                    "duration": duration,
                    "error": None,
                    "path": str(example_path),
                }

                print(f"✅ {example_name} completed successfully ({duration:.2f}s)")
                return result_dict
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"

                result_dict = {
                    "name": example_name,
                    "status": "ERROR",
                    "duration": duration,
                    "error": error_msg,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "path": str(example_path),
                }

                print(f"❌ {example_name} failed ({duration:.2f}s): {error_msg}")
                return result_dict

        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time

            result = {
                "name": example_name,
                "status": "ERROR",
                "duration": duration,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "path": str(example_path),
            }

            print(f"❌ {example_name} failed ({duration:.2f}s): {e}")
            return result

    def run_all_examples(self) -> None:
        """Runs all examples."""
        print("🚀 Starting execution of all regman examples")
        print("=" * 60)
        print()

        examples = self.find_examples()

        if not examples:
            print("❌ No examples found in examples/ folder")
            return

        print(f"📁 {len(examples)} example(s) found:")
        for example in examples:
            print(f"   - {example.name}")
        print()

        # Running examples
        for example_path in examples:
            result = self.run_example(example_path)
            self.results.append(result)
            print()  # Empty line between examples

        self.generate_report()

    def generate_report(self) -> None:
        """Generates a detailed report of the results."""
        total_time = time.time() - self.start_time
        successful = [r for r in self.results if r["status"] == "SUCCESS"]
        failed = [r for r in self.results if r["status"] == "ERROR"]

        print("📊 EXECUTION REPORT")
        print("=" * 60)
        print()

        # General summary
        print("📈 General summary:")
        print(f"   Total examples: {len(self.results)}")
        print(f"   Success: {len(successful)}")
        print(f"   Failures: {len(failed)}")
        print(f"   Total time: {total_time:.2f} seconds")
        print(f"   Success rate: {len(successful) / len(self.results) * 100:.1f}%")
        print()

        # Success details
        if successful:
            print("✅ Successful examples:")
            for result in successful:
                print(f"   - {result['name']} ({result['duration']:.2f}s)")
            print()

        # Failure details
        if failed:
            print("❌ Failed examples:")
            for result in failed:
                print(f"   - {result['name']} ({result['duration']:.2f}s)")
                print(f"     Error: {result['error']}")
            print()

        # Performance statistics
        if self.results:
            durations = [r["duration"] for r in self.results]
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)

            print("⏱️  Performance statistics:")
            print(f"   Average duration: {avg_duration:.2f}s")
            print(f"   Minimum duration: {min_duration:.2f}s")
            print(f"   Maximum duration: {max_duration:.2f}s")
            print()

        # Recommendations
        print("💡 Recommendations:")
        if failed:
            print("   - Check the errors above and fix the issues")
            print("   - Make sure all dependencies are installed")
        else:
            print("   - All examples work correctly!")
            print("   - You can use regman with confidence")

        if len(successful) > 0:
            print("   - Check the successful examples to learn how to use regman")

        print()
        print("🎉 Execution completed!")

        # Exit code
        if failed:
            sys.exit(1)
        else:
            sys.exit(0)


def main() -> None:
    """Main function."""
    runner = ExampleRunner()
    runner.run_all_examples()


if __name__ == "__main__":
    main()
