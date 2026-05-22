from playwright.async_api import async_playwright
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            logger.info("Browser started")

    async def navigate(self, url: str):
        await self.start()
        if self.page:
            logger.info(f"Navigating to {url}")
            await self.page.goto(url)

    async def search(self, query: str):
        await self.navigate(f"https://www.google.com/search?q={query}")

    async def extract_content(self) -> str:
        if self.page:
            return await self.page.content()
        return ""

    async def click(self, selector: str):
        if self.page:
            await self.page.click(selector)

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.playwright = None
        logger.info("Browser stopped")

    async def stop(self):
        await self.close()
