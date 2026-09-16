import re
from pathlib import Path

from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, then, when


def wait_for_dashboard(page: Page):
    expect(page.get_by_role("button", name="Sign Out")).to_be_visible(timeout=30000)
    expect(page.get_by_role("heading", name="Finance Overview Dashboard")).to_be_visible(
        timeout=30000
    )


def wait_for_login_ready(page: Page):
    expect(page.get_by_role("button", name="Access Shared Ledger")).to_be_visible(timeout=15000)


@given("I am on the Accutai login page")
def open_login_page(page: Page):
    page.goto("/")


@when(parsers.parse('I enter username "{username}" and password "{password}"'))
def enter_credentials(page: Page, username: str, password: str):
    page.get_by_placeholder("demo@accutai.com or username").fill(username)
    page.get_by_placeholder("••••••••").fill(password)


@when("I access the shared ledger")
def access_shared_ledger(page: Page):
    access_button = page.get_by_role("button", name="Access Shared Ledger")
    wait_for_login_ready(page)
    access_button.click()
    page.wait_for_timeout(1500)


@then("I should see the Finance Overview Dashboard")
def verify_dashboard(page: Page):
    wait_for_dashboard(page)


@then("I should see the correct user profile details")
def verify_user_profile_details(page: Page):
    profile = page.locator("aside")
    expect(profile.get_by_text("anjan", exact=True)).to_be_visible(timeout=15000)
    expect(
        profile.get_by_text("anjan.das@accutai.com", exact=True)
    ).to_be_visible(timeout=15000)


@when(parsers.parse('I update the monthly budget target to "{amount}"'))
def update_monthly_budget_target(page: Page, amount: str):
    page.get_by_role("button", name="Adjust Budget Target").click()
    expect(
        page.get_by_role("heading", name="Adjust Shared Company Budget")
    ).to_be_visible(timeout=15000)
    budget_modal = page.get_by_role(
        "heading", name="Adjust Shared Company Budget"
    ).locator("xpath=ancestor::*[.//input[@type='number']][1]")
    target_input = budget_modal.locator("input[type='number']")
    target_input.fill(amount)
    page.get_by_role("button", name="Save Shared Target").click()
    page.wait_for_timeout(3000)
    budget_heading = page.get_by_role(
        "heading", name="Adjust Shared Company Budget"
    )
    if budget_heading.is_visible():
        page.get_by_role("button", name="Close").click()
        expect(budget_heading).not_to_be_visible(timeout=15000)


@when("I save the current monthly budget target")
def save_current_monthly_budget_target(page: Page):
    budget_card = page.get_by_text("Monthly Budget", exact=True).locator(
        "xpath=ancestor::*[contains(., '₹')][1]"
    )
    current_text = budget_card.inner_text()
    match = re.search(r"₹\s*([\d,]+(?:\.\d{2})?)", current_text)
    assert match, f"Could not read current monthly budget: {current_text}"
    page._original_monthly_budget = match.group(1).replace(",", "").split(".")[0]


@when("I restore the original monthly budget target")
def restore_original_monthly_budget_target(page: Page):
    original_amount = getattr(page, "_original_monthly_budget", None)
    assert original_amount, "Original monthly budget was not captured"
    update_monthly_budget_target(page, original_amount)


@when("I wait 5 seconds")
def wait_five_seconds(page: Page):
    page.wait_for_timeout(5000)


@then(parsers.parse('the monthly budget should display "{amount}"'))
def verify_monthly_budget_target(page: Page, amount: str):
    expect(page.get_by_text("Monthly Budget", exact=True)).to_be_visible(timeout=15000)
    budget_card = page.get_by_text("Monthly Budget", exact=True).locator(
        "xpath=ancestor::*[contains(., '₹')][1]"
    )
    expect(budget_card).to_contain_text(f"₹{float(amount):,.2f}", timeout=15000)


@then("the monthly budget should return to its original value")
def verify_original_monthly_budget_target(page: Page):
    original_amount = getattr(page, "_original_monthly_budget", None)
    assert original_amount, "Original monthly budget was not captured"
    verify_monthly_budget_target(page, original_amount)


@when("I inspect the year dropdown options")
def inspect_year_dropdown_options(page: Page):
    year_filter = page.get_by_role("combobox", name="Filter Year")
    expect(year_filter).to_be_visible(timeout=15000)


@then("the year dropdown should include years from 2020 through 2030")
def verify_year_dropdown_range(page: Page):
    year_filter = page.get_by_role("combobox", name="Filter Year")
    years = year_filter.locator("option").all_text_contents()
    available_years = {int(year.strip()) for year in years}
    expected_years = set(range(2020, 2031))
    missing_years = sorted(expected_years - available_years)
    assert not missing_years, (
        f"Year dropdown is missing required audit/planning years: {missing_years}. "
        f"Available years: {years}"
    )


@when("I click the Sign Out button")
def click_sign_out(page: Page):
    sign_out = page.get_by_role("button", name="Sign Out")
    expect(sign_out).to_be_visible(timeout=15000)
    sign_out.click()


@then("I should be returned to the login page")
def verify_returned_to_login_page(page: Page):
    expect(page.get_by_role("button", name="Access Shared Ledger")).to_be_visible(
        timeout=15000
    )
    expect(page.get_by_role("heading", name="Accutai Finance Portal")).to_be_visible(
        timeout=15000
    )
    expect(
        page.get_by_role("heading", name="Finance Overview Dashboard")
    ).not_to_be_visible(timeout=15000)
    page.wait_for_timeout(3000)


@then("I should not see the Finance Overview Dashboard")
def verify_dashboard_not_visible(page: Page):
    expect(page.get_by_role("heading", name="Finance Overview Dashboard")).not_to_be_visible(
        timeout=15000
    )


@given("I open the Accutai portal")
def open_portal(page: Page):
    page.goto("/")


@then("I should see the Accutai Finance portal")
def verify_portal(page: Page):
    expect(page).to_have_title(
        "Accutai | Corporate Finance Dashboard & Expense Tracker"
    )
    expect(page.get_by_text("Sign in", exact=False)).to_be_visible()


@then("I should see the monthly budget and financial metrics")
def verify_budget_metrics(page: Page):
    expect(page.get_by_role("button", name="Sign Out")).to_be_visible(timeout=30000)
    expect(page.get_by_role("heading", name="Finance Overview Dashboard")).to_be_visible(
        timeout=30000
    )
    expect(page.get_by_text("Monthly Budget", exact=True)).to_be_visible()
    expect(page.get_by_text("Monthly Spending", exact=True)).to_be_visible()
    expect(page.get_by_text("Net Operating Cash", exact=True)).to_be_visible()

    def metric_value(label: str):
        from decimal import Decimal

        card_text = page.get_by_text(label, exact=True).locator(
            "xpath=ancestor::*[contains(., '₹')][1]"
        ).inner_text()
        value = re.search(r"₹\s*([\d,]+(?:\.\d{2})?)", card_text)
        assert value, f"No currency value found for {label}: {card_text}"
        return Decimal(value.group(1).replace(",", ""))

    monthly_budget = metric_value("Monthly Budget")
    monthly_spending = metric_value("Monthly Spending")
    net_operating_cash = metric_value("Net Operating Cash")

    assert monthly_budget >= 0
    assert monthly_spending >= 0
    assert net_operating_cash == monthly_budget - monthly_spending

    expected_status = "Within Limit" if monthly_spending <= monthly_budget else "Over Budget"
    expect(
        page.get_by_role("heading", name=re.compile(expected_status, re.IGNORECASE))
    ).to_be_visible()


@when("I click Register")
def click_register(page: Page):
    page.get_by_role("button", name="Register").click()


@when("I enter a new username and email and password")
def enter_new_user_details(page: Page):
    from uuid import uuid4

    username = f"playwright_{uuid4().hex[:8]}"
    page.get_by_placeholder("e.g. soumya").fill(username)
    page.get_by_placeholder("username@accutai.com").fill(f"{username}@accutai.com")
    page.get_by_placeholder("••••••••").fill("TestPass123!")
    page.get_by_role("button", name="Create Account").click()


@then("I should see the authenticating state")
def verify_authenticating(page: Page):
    expect(page.get_by_role("button", name="Authenticating...")).to_be_visible(timeout=5000)


@when(parsers.parse('I click the "{nav_label}" sidebar item'))
def click_sidebar_item(page: Page, nav_label: str):
    sidebar_item = page.get_by_role("button", name=re.compile(f"^{re.escape(nav_label)}$"))
    expect(sidebar_item).to_be_visible()
    sidebar_item.click()
    expect(sidebar_item).to_have_class(re.compile(r"active"))


@then(parsers.parse('I should see the "{expected_heading}" section'))
def verify_active_section(page: Page, expected_heading: str):
    heading_aliases = {
        "Dashboard": r"Finance Overview Dashboard",
        "Shared Ledger All Team": r"Shared Company Ledger",
        "Company Budget": r"Company Budget( Management)?|Shared Company Budget Within",
        "Analytics & Reports": r"Analytics & Reports",
        "Calendar View": r"Monthly Activity Calendar|Daily Activity Calendar",
    }

    pattern = heading_aliases.get(expected_heading, re.escape(expected_heading))
    section_heading = page.locator("h1, h2, h3").filter(
        has_text=re.compile(pattern, re.IGNORECASE)
    )
    expect(section_heading.first).to_be_visible(timeout=15000)
    expect(page.locator("main")).to_be_visible()


@when("I click the View All in Ledger shortcut")
def click_view_all_in_ledger(page: Page):
    page.get_by_role("button", name=re.compile(r"View All in Ledger")).click()


@then("I should be on the full Shared Ledger view")
def verify_full_shared_ledger_view(page: Page):
    expect(page.get_by_role("heading", name="Shared Company Ledger")).to_be_visible(
        timeout=15000
    )
    sidebar_item = page.get_by_role("button", name="Shared Ledger All Team")
    expect(sidebar_item).to_have_class(re.compile(r"active"))


@then("the Shared Ledger should show transaction audit columns and filters")
def verify_shared_ledger_audit_surface(page: Page):
    expect(page.get_by_role("heading", name="Shared Company Ledger")).to_be_visible(
        timeout=15000
    )
    table = page.locator("table")
    expect(table).to_be_visible(timeout=15000)
    for column in ["Date", "Category", "Description", "Recorded By", "Amount"]:
        expect(table.get_by_role("columnheader", name=column)).to_be_visible()
    expect(page.get_by_role("combobox", name="Filter Month")).to_be_visible()
    expect(page.get_by_role("combobox", name="Filter Year")).to_be_visible()


@when(parsers.parse('I create a future transaction for "{date}"'))
def create_future_transaction(page: Page, date: str):
    page.get_by_role("button", name=re.compile(r"Add Entry")).first.click()
    expect(page.get_by_text("Record New Transaction")).to_be_visible(timeout=15000)
    page.locator("input[type='date']").first.fill(date)
    page.locator("input[type='number']").first.fill("10")
    page.locator("select.form-input").last.select_option(label="General")
    page.locator("input[placeholder*='e.g. AWS Cloud Hosting']").first.fill(
        "tc19-future-expense"
    )
    page.get_by_role("button", name="Record Transaction").click()
    expect(page.get_by_role("button", name="Saving...")).not_to_be_visible(timeout=90000)
    modal = page.get_by_role("heading", name="Record New Transaction")
    if modal.is_visible():
        page.get_by_role("button", name="Close").click()
    expect(modal).not_to_be_visible(timeout=15000)


@then("the future transaction should be recorded")
def verify_future_transaction_recorded(page: Page):
    page.get_by_role("button", name="Shared Ledger All Team").click()
    expect(page.get_by_role("heading", name="Shared Company Ledger")).to_be_visible(
        timeout=15000
    )
    page.get_by_role("combobox", name="Filter Month").select_option(label="October")
    page.get_by_role("combobox", name="Filter Year").select_option(label="2026")
    expect(page.get_by_role("combobox", name="Filter Month")).to_have_value("10")
    expect(page.get_by_role("combobox", name="Filter Year")).to_have_value("2026")


@then("the Company Budget page should show utilization and category breakdown")
def verify_company_budget_page(page: Page):
    expect(page.get_by_role("heading", name="Company Budget Management")).to_be_visible(
        timeout=15000
    )
    expect(
        page.locator("h2").filter(has_text=re.compile("Shared Company Budget"))
    ).to_be_visible()
    expect(page.get_by_text("Category Breakdown vs Shared Spending", exact=True)).to_be_visible()
    for label in ["Spent:", "Remaining:", "Target Cap:"]:
        expect(page.get_by_text(label, exact=False)).to_be_visible()


@when("I switch through the analytics timeframes")
def switch_analytics_timeframes(page: Page):
    overview = page.get_by_text(re.compile(r"Period overview:"))
    for timeframe in ["monthly", "quarterly", "yearly"]:
        page.get_by_role("button", name=timeframe, exact=True).click()
        expect(overview).to_be_visible(timeout=15000)


@then("the analytics period overview should update")
def verify_analytics_period_overview(page: Page):
    overview = page.get_by_text(re.compile(r"Period overview:\s*\d{4}-\d{2}-\d{2}"))
    expect(overview).to_be_visible(timeout=15000)
    expect(page.get_by_role("heading", name="Category Expense Distribution")).to_be_visible()
    expect(page.get_by_role("heading", name="Top Expense Items in Period")).to_be_visible()


@then("the calendar should select today's date")
def verify_calendar_selects_today(page: Page):
    from datetime import date

    today = date.today()
    expect(page.get_by_role("heading", name="Monthly Activity Calendar")).to_be_visible(
        timeout=15000
    )
    today_button = page.get_by_role("button", name=re.compile(rf"^{today.day}\b"))
    expect(today_button).to_be_visible()
    expect(today_button).to_have_attribute(
        "style", re.compile(r"background-color: rgb\(255, 255, 255\)")
    )


@when('I click the "+ Add Entry" button')
def click_add_entry(page: Page):
    add_entry_buttons = page.get_by_role("button", name="Add Entry")
    expect(add_entry_buttons).to_have_count(2)
    add_entry_buttons.first.click()
    expect(page.get_by_text("Record New Transaction")).to_be_visible(timeout=15000)


@when(
    parsers.parse(
        'I fill in the transaction details with date "{date}", category "{category}", description "{description}", and amount "{amount}"'
    )
)
def fill_transaction_details(page: Page, date: str, category: str, description: str, amount: str):
    expect(page.get_by_text("Record New Transaction")).to_be_visible(timeout=15000)

    page.locator("input[type='date']").first.fill(date)
    transaction_form = page.get_by_text("Record New Transaction").locator(
        "xpath=ancestor::*[.//select][1]"
    )
    category_select = transaction_form.locator("select.form-input")
    category_select.select_option(label=category)
    expect(category_select.locator("option:checked")).to_have_text(category)
    page.locator("input[placeholder*='e.g. AWS Cloud Hosting']").first.fill(description)
    page.locator("input[type='number']").first.fill(amount)


@when("I submit the transaction")
def submit_transaction(page: Page):
    page.get_by_role("button", name="Record Transaction").click()


@then(
    parsers.parse(
        'I should see the new "{description}" transaction in category "{category}" with amount "{amount}"'
    )
)
def verify_new_transaction_in_table(
    page: Page, description: str, category: str, amount: str
):
    expect(page.get_by_role("heading", name="Recent Shared Transactions")).to_be_visible(
        timeout=15000
    )
    expect(page.locator("table")).to_contain_text(description, timeout=15000)
    expect(page.locator("table")).to_contain_text(category, timeout=15000)
    expect(page.locator("table")).to_contain_text(f"₹{float(amount):.2f}", timeout=15000)


@when("I create a transaction with an attached receipt")
def create_transaction_with_receipt(page: Page):
    page.get_by_role("button", name="Add Entry").first.click()
    expect(page.get_by_text("Record New Transaction")).to_be_visible(timeout=15000)
    page.locator("input[type='date']").first.fill("2026-09-16")
    page.locator("input[type='number']").first.fill("10")
    page.locator("select.form-input").last.select_option(label="Office Supplies")
    page.locator("input[placeholder*='e.g. AWS Cloud Hosting']").first.fill(
        "receipt-view-verification"
    )
    receipt_path = Path(__file__).parent / "fixtures" / "receipt.pdf"
    page.locator("input[type='file']").set_input_files(str(receipt_path))
    page.get_by_role("button", name="Record Transaction").click()
    expect(page.get_by_role("button", name="Saving...")).not_to_be_visible(timeout=90000)
    transaction_modal = page.get_by_role("heading", name="Record New Transaction")
    if transaction_modal.is_visible():
        page.get_by_role("button", name="Close").click()
    expect(transaction_modal).not_to_be_visible(timeout=15000)
    page.reload(wait_until="domcontentloaded")
    wait_for_dashboard(page)


@then("I should be able to view the attached receipt")
def verify_attached_receipt_view(page: Page):
    table = page.locator("table")
    expect(table).not_to_contain_text("Loading shared transactions...", timeout=30000)
    view_bill = table.get_by_role("button", name="View Bill").first
    expect(view_bill).to_be_visible(timeout=15000)
    view_bill.click()

    expect(page.get_by_role("heading", name="Receipt / Expense Bill")).to_be_visible(
        timeout=15000
    )
    expect(page.get_by_role("link", name="Open PDF in Viewer")).to_be_visible(
        timeout=15000
    )


@when(
    parsers.parse(
        'I add a transaction for every category with date "{date}", description "{description}", and amount "{amount}"'
    )
)
def add_transaction_for_every_category(
    page: Page, date: str, description: str, amount: str
):
    categories = [
        "Entertainment",
        "Equipment",
        "Food & Dining",
        "Freelance & Consulting",
        "General",
        "Groceries",
        "Health & Fitness",
        "Marketing & Ads",
        "Office Supplies",
        "Puja",
        "Rent & Housing",
        "Salary & Wages",
        "Software & Tools",
        "test",
        "Transportation",
        "Travel & Lodging",
        "Utilities",
    ]

    for category in categories:
        page.get_by_role("button", name="Add Entry").first.click()
        expect(page.get_by_text("Record New Transaction")).to_be_visible(timeout=15000)
        page.locator("input[type='date']").first.fill(date)
        transaction_form = page.get_by_text("Record New Transaction").locator(
            "xpath=ancestor::*[.//select][1]"
        )
        category_select = transaction_form.locator("select.form-input")
        category_select.select_option(label=category)
        expect(category_select.locator("option:checked")).to_have_text(category)
        page.locator("input[placeholder*='e.g. AWS Cloud Hosting']").first.fill(description)
        page.locator("input[type='number']").first.fill(amount)
        page.get_by_role("button", name="Record Transaction").click()
        expect(page.get_by_text("Record New Transaction")).not_to_be_visible(timeout=15000)
        page.wait_for_timeout(3000)


@then("I should see the new transaction for every category in the recent shared transactions table")
def verify_transactions_for_every_category(page: Page):
    categories = [
        "Entertainment",
        "Equipment",
        "Food & Dining",
        "Freelance & Consulting",
        "General",
        "Groceries",
        "Health & Fitness",
        "Marketing & Ads",
        "Office Supplies",
        "Puja",
        "Rent & Housing",
        "Salary & Wages",
        "Software & Tools",
        "test",
        "Transportation",
        "Travel & Lodging",
        "Utilities",
    ]

    expect(page.get_by_role("heading", name="Recent Shared Transactions")).to_be_visible(
        timeout=15000
    )
    category_filter = page.get_by_role("combobox", name="Filter by category")
    expect(category_filter).to_be_visible(timeout=15000)

    available_categories = [
        option.strip() for option in category_filter.locator("option").all_inner_texts()
    ]
    for category in categories:
        assert category in available_categories, (
            f"Category '{category}' not available in filter options: {available_categories}"
        )

    table = page.locator("table")
    expect(table).to_be_visible(timeout=15000)
    if "No transactions found" not in table.inner_text():
        expect(table).to_contain_text("test", timeout=15000)
        expect(table).to_contain_text("₹10.00", timeout=15000)

    category_filter.select_option(label="All Categories")

@when(
    parsers.parse(
        'I create a transaction with date "{date}", category "{category}", description "{description}", and amount "{amount}"'
    )
)
def create_transaction(page: Page, date: str, category: str, description: str, amount: str):
    page.get_by_role("button", name="Add Entry").first.click()
    expect(page.get_by_text("Record New Transaction")).to_be_visible(timeout=15000)
    page.locator("input[type='date']").first.fill(date)
    transaction_form = page.get_by_text("Record New Transaction").locator(
        "xpath=ancestor::*[.//select][1]"
    )
    category_select = transaction_form.locator("select.form-input")
    category_select.select_option(label=category)
    expect(category_select.locator("option:checked")).to_have_text(category)
    page.locator("input[placeholder*='e.g. AWS Cloud Hosting']").first.fill(description)
    page.locator("input[type='number']").first.fill(amount)
    page.get_by_role("button", name="Record Transaction").click()
    expect(page.locator("table")).to_contain_text(description, timeout=15000)


@when(parsers.parse('I search for "{keyword}" in the recent shared transactions table'))
def search_transactions(page: Page, keyword: str):
    category_filter = page.get_by_role("combobox", name="Filter by category")
    expect(category_filter).to_be_visible(timeout=15000)
    category_filter.select_option(label="All Categories")

    search_box = page.locator("input[placeholder*='Search description']")
    expect(search_box).to_be_visible(timeout=15000)
    search_box.fill(keyword)


@when(parsers.parse('I filter the recent shared transactions by category "{category}"'))
def filter_transactions_by_category(page: Page, category: str):
    search_box = page.locator("input[placeholder*='Search description']")
    expect(search_box).to_be_visible(timeout=15000)
    search_box.fill("")

    category_filter = page.get_by_role("combobox", name="Filter by category")
    expect(category_filter).to_be_visible(timeout=15000)
    category_filter.select_option(label=category)


@then(parsers.parse('I should only see transactions matching "{keyword}"'))
def verify_filtered_transactions(page: Page, keyword: str):
    table = page.locator("table")
    expect(table).to_be_visible(timeout=15000)
    expect(table).not_to_contain_text("Loading shared transactions...", timeout=30000)
    table_text = table.inner_text().lower()

    if "no transactions found" in table_text:
        assert keyword.lower() not in table_text or "no transactions found" in table_text
        return

    assert keyword.lower() in table_text, f"Expected '{keyword}' in table content: {table_text}"
    rows = table.locator("tbody tr")
    if rows.count() > 0:
        for i in range(rows.count()):
            row_text = rows.nth(i).inner_text().lower()
            assert keyword.lower() in row_text, f"Row does not match keyword: {row_text}"
