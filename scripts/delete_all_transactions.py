import os

from playwright.sync_api import Page, expect, sync_playwright


BASE_URL = os.getenv(
    "ACCUTAI_BASE_URL", "https://storied-cuchufli-1e70f1.netlify.app"
)
USERNAME = os.getenv("ACCUTAI_USERNAME", "anjan")
PASSWORD = os.getenv("ACCUTAI_PASSWORD", "123456")


def login(page: Page) -> None:
    page.goto(BASE_URL)
    page.locator('input[placeholder="demo@accutai.com or username"]').fill(USERNAME)
    page.locator('input[placeholder="••••••••"]').fill(PASSWORD)
    page.get_by_role("button", name="Access Shared Ledger").click()
    page.get_by_role("button", name="Sign Out").wait_for(state="visible", timeout=30000)
    page.get_by_role("button", name="Shared Ledger All Team").click()
    page.get_by_role("heading", name="Shared Company Ledger").wait_for(
        state="visible", timeout=15000
    )


def delete_visible_transactions(page: Page) -> int:
    deleted = 0
    delete_buttons = page.get_by_role("button", name="Delete")

    while True:
        button_count = delete_buttons.count()
        if button_count == 0:
            break

        delete_buttons.first.click()
        page.wait_for_timeout(1500)
        deleted += 1

    return deleted


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("dialog", lambda dialog: dialog.accept())

        try:
            login(page)
            month_filter = page.get_by_role("combobox", name="Filter Month")
            year_filter = page.get_by_role("combobox", name="Filter Year")
            months = month_filter.locator("option").all_text_contents()
            years = year_filter.locator("option").all_text_contents()
            total_deleted = 0

            for year in years:
                year_filter.select_option(label=year)
                expect(year_filter).to_have_value(year, timeout=15000)
                for month in months:
                    month_filter.select_option(label=month)
                    expect(month_filter).to_have_value(
                        month_filter.locator("option").filter(has_text=month).get_attribute("value"),
                        timeout=15000,
                    )
                    page.wait_for_timeout(8000)
                    total_deleted += delete_visible_transactions(page)

            for year in years:
                year_filter.select_option(label=year)
                expect(year_filter).to_have_value(year, timeout=15000)
                for month in months:
                    month_filter.select_option(label=month)
                    page.wait_for_timeout(8000)
                    remaining = page.get_by_role("button", name="Delete").count()
                    if remaining:
                        total_deleted += delete_visible_transactions(page)
                        page.wait_for_timeout(3000)
                        remaining = page.get_by_role("button", name="Delete").count()
                        if remaining:
                            raise RuntimeError(
                                f"Cleanup incomplete for {month} {year}: "
                                f"{remaining} transaction(s) remain"
                            )

            print(f"Deleted {total_deleted} transaction(s).")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
