import sys
import subprocess
import logging

def launch():
    """
    Main entry point to bootstrap Jarvis OS.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("JarvisLauncher")

    logger.info("Initializing Jarvis OS v1...")

    # 1. Validate Environment
    from jarvis.validation.deployment_validator import DeploymentValidator
    validator = DeploymentValidator()
    if not validator.check_environment():
        sys.exit(1)

    # 2. Run API in background
    logger.info("Starting API Gateway...")
    # subprocess.Popen(["uvicorn", "jarvis.api.main:app", "--port", "8000"])

    logger.info("Jarvis OS Ready.")

if __name__ == "__main__":
    launch()
