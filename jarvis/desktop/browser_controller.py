from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)

class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        logger.info("Browser started")

    async def navigate(self, url: str):
        if self.page:
            logger.info(f"Navigating to {url}")
            await self.page.goto(url)

    async def click(self, selector: str):
        if self.page:
            await self.page.click(selector)

    async def type(self, selector: str, text: str):
        if self.page:
            await self.page.fill(selector, text)

    async def screenshot(self, path: str):
        if self.page:
            await self.page.screenshot(path=path)

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser stopped")
