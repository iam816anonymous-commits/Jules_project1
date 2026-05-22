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

    async def start(self, **kwargs):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            logger.info("Browser started")
        return {"status": "started"}

    async def navigate(self, url: str = None, query: str = None, **kwargs):
        await self.start()
        target = url or f"https://www.google.com/search?q={query}"
        if self.page:
            logger.info(f"Navigating to {target}")
            await self.page.goto(target)
        return {"status": "navigated", "url": target}

    async def extract_content(self, **kwargs):
        if self.page:
            return await self.page.content()
        return ""

    async def stop(self, **kwargs):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.playwright = None
        logger.info("Browser stopped")
        return {"status": "stopped"}
