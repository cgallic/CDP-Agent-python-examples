import asyncio
import logging
import os
import sys
from decimal import Decimal
from pathlib import Path
from dotenv import load_dotenv
from types import MethodType  # Import MethodType for monkey-patching

# Load environment variables from .env file



# Adjust paths as needed if your cdp_agent.py is in a subdirectory
from cdp_agent import CDPAgent, CreateChargeInput, CreatePayLinkInput


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_credentials() -> str:
    """Securely loads the API key from environment variables."""
    # Load environment variables from a .env file (ensure .env is in .gitignore)
    load_dotenv()
    
    api_key = os.getenv("KEY_API")
    if not api_key:
        logger.critical("Initialization Failed: KEY_API environment variable is missing.")
        raise ValueError("Missing critical API credentials.")
        
    return api_key

async def main():
    # Initialize credentials securely
    try:
        api_key = load_credentials()
        logger.info("Credentials loaded securely. Initializing payment test sequence...")
    except Exception as e:
        logger.error(f"Fatal error during execution: {e}")
        return

    # Initialize CDPAgent
    # Note: Assuming CDPAgent has been updated to accept api_key directly
    agent = CDPAgent(api_key=api_key, wallet_path='wallet_data.txt')

    # Test create_charge tool directly
    # Set name, description, amount, currency as needed.
    charge_args = CreateChargeInput(
        name="Test Payment",
        description="Testing charge creation",
        amount="5.00",
        currency="USD",
        pricing_type="fixed_price"
    )

    logger.info("Testing create_charge:")
    try:
        # The create_charge tool is integrated as a structured tool in the agent
        # Let's find the create_charge tool from the agent
        create_charge_tool = next((t for t in agent.all_tools if t.name == "create_charge"), None)
        if create_charge_tool is None:
            logger.error("create_charge tool not found.")
            return

        response = create_charge_tool.run(charge_args.model_dump())
        print("Create Charge Response:")
        print(response)
    except Exception as e:
        logger.error(f"Error creating charge: {e}", exc_info=True)


    # Test create_pay_link tool
    # If your network_id is 'base' or 'base-mainnet', this should generate a pay link.
    pay_link_args = CreatePayLinkInput(blockchain="base")
    logger.info("Testing create_pay_link:")
    try:
        create_pay_link_tool = next((t for t in agent.all_tools if t.name == "create_pay_link"), None)
        if create_pay_link_tool is None:
            logger.error("create_pay_link tool not found.")
            return
        pay_response = create_pay_link_tool.run(pay_link_args.model_dump())

        print("Create Pay Link Response:")
        print(pay_response)
    except Exception as e:
        logger.error(f"Error creating pay link: {e}")

    # Optionally, you can test get_balance to ensure you can interact with the wallet
    try:
        balance = await agent.get_balance("eth")
        print("Current ETH Balance:", balance)
    except Exception as e:
        logger.error(f"Error creating charge: {e}", exc_info=True)


if __name__ == "__main__":
    # Run the async main in an event loop
    asyncio.run(main())
