import json
from pathlib import Path
DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "debt.json"

def save_debts(debts):
    DATA_DIR.mkdir(exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(debts, file, indent=4)

def load_debts():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Warning: Saved debt data could not be read.")
        return []

    
def display_header():
    print("===================")
    print("    DEBTTRACK")
    print("===================")
    print("Personal Debt Management System")


def get_debt_details():
    creditor_name = input("Creditor Name: ")
    debt_name = input("Enter the debt name: ")
    balance = float(input("Enter the current blaance: R"))
    interest_rate = float(input("Enter the annual interest rate (%): "))
    monthly_payment = float(input("Enter the monthly payment: R"))

    return creditor_name, debt_name, balance, interest_rate, monthly_payment


def calculate_payoff(balance, interest_rate, monthly_payment):
    annual_payment = monthly_payment * 12 

    monthly_interest_rate = interest_rate / 100 /12
    monthly_interest_amount = balance * monthly_interest_rate

    if balance <= 0:
        return None, "Error: Balance must be greateer than R0."
    if interest_rate < 0:
        return None, "Error: Interest rate cannot be negative"
    if monthly_payment <= 0:
        return None, "Error: Monthly payment must be greater than R0"
    if monthly_payment <= monthly_interest_amount: 
        return None, "Warning: Your monthly payment is too low to reduce this debt."

    remaining_balance = balance 
    months_to_payoff = 0
    total_interest = 0

    while remaining_balance > 0:
        interest_for_month = remaining_balance * monthly_interest_rate

        total_interest += interest_for_month
        remaining_balance += interest_for_month

        payment_this_month = min(monthly_payment, remaining_balance)

        remaining_balance -= payment_this_month
        months_to_payoff += 1

    years = months_to_payoff//12
    remaining_months = months_to_payoff % 12

    total_paid = balance + total_interest

    result = (
        annual_payment,
        years,
        remaining_months,
        total_interest,
        total_paid
    )

    return result, None


def display_summary(
        creditor_name,
        debt_name,
        balance,
        interest_rate,
        monthly_payment,
        result
    ):
    annual_payment, years, remaining_months, total_interest, total_paid = result

    print("\n--- Debt Summary ---")
    print("Creditor: ", creditor_name)
    print("Debt:", debt_name)
    print(f"Starting Balance: R{balance:,.2f}")
    print(f"Interest Rate: {interest_rate}%")
    print(f"Monthly Payment: R{monthly_payment:,.2f}")
    print(f"Planned Annual Payments: R{annual_payment:,.2f}")
    print(f"Estimated Payoff Time: {years} years and {remaining_months} months")
    print(f"Estimated Interest Paid: R{total_interest:,.2f}")
    print(f"Estimated Total Paid: R{total_paid:,.2f}")

def display_portfolio_summary(debts):
    total_debt = 0
    total_monthly_payments = 0
    total_interest = 0
    total_paid = 0

    for debt in debts:
        total_debt += debt["balance"]
        total_monthly_payments += debt["monthly_payment"]


        (
            annual_payment,
            years,
            remaining_months,
            debt_interests,
            debt_total_paid,
        ) = debt["result"]

        total_interest += debt_interests
        total_paid += debt_total_paid

    highest_interest_debt = max(
        debts,
        key=lambda debt: debt["interest_rate"]
    )

    largest_debt = max(
        debts,
        key=lambda debt: debt["balance"]
    )

    print("\n================DEBT PORTFOLIO================")
    print(f"Number of Debts: {len(debts)}")
    print(f"Total Debt: R{total_debt:,.2f}")
    print(f"Total Monthly Payments: R{total_monthly_payments:,.2f}")
    print(f"Estimated Total Interest: R{total_interest:,.2f}")
    print(f"Estimated Total Repayment: R{total_paid:,.2f}")

    print("n\--- Portfolio Insights ---")

    print(
        f"Highest Interest Debt: "
        f"{highest_interest_debt['debt_name']}"
        f"({highest_interest_debt['interest_rate']}%)"
    )

    print(
        f"largest Debt: "
        f"{largest_debt['debt_name']}"
        f"(R{largest_debt['balance']:,.2f})"

    )

    print("\n--- Debts ---")

    for index, debt in enumerate(debts, start=1):
        print(
            f"{index}. {debt['creditor']} - "
            f"{debt['debt_name']} - "
            f"R{debt['balance']:,.2f}"
        )


def display_menu():
    print("\n========== DEBTRACK MENU ===========")
    print("1. View debt portfolio")
    print("2. Add a debt")
    print("3. Remove a debt")
    print("4. Exit")

    return input("\nChoose an option: ").strip()

def remove_debt(debts):
    if not debts:
        print("\nNo debts available to remove.")
        return

    print("\n--- Select Debt to Remove ---")

    for index, debt in enumerate(debts, start=1):
        print(
            f"{index}. {debt['creditor']} - "
            f"{debt['debt_name']} - "
            f"R{debt['balance']:,.2f}"
        )

    try:
        choice = int(input("\nEnter debt number to remove: "))
    except ValueError:
        print("\nInvalid input. Please eneter a number.")
        return 

    if choice < 1 or choice > len(debts):
        print("\nInvalid debt number.")
        return

    remove_debt = debts.pop(choice -1)

    save_debts(debts)

    print(
        f"\nRemoved: {remove_debt['creditor']} - "
        f"{remove_debt['debt_name']}"
    )


def main():
    display_header()

    debts = load_debts()

    if debts:
        print(f"\nLoaded {len(debts)} saved debt(s).")

    while True:

        choice = display_menu()

        if choice == "1":
            if debts:
                display_portfolio_summary(debts)
            else: 
                print("\nNo debts have been added yet.")

        elif choice == "2":


            creditor_name, debt_name, balance, interest_rate, monthly_payment = (
                get_debt_details()
            )

            result, error = calculate_payoff(
                balance, 
                interest_rate,
                monthly_payment

            )

            if error:
                print(error)
                continue

            print("Payment is sufficient to reduce the debt.")

            debt = {
                "creditor": creditor_name,
                "debt_name": debt_name,
                "balance": balance,
                "interest_rate": interest_rate,
                "monthly_payment": monthly_payment,
                "result": result
            }

            debts.append(debt)
            save_debts(debts)

            print("\nDebt added successfully.")

            display_summary(
                creditor_name,
                debt_name,
                balance,
                interest_rate,
                monthly_payment,
                result,
            )
        elif choice == "3":
            remove_debt(debts)

        elif choice == "4":
            print("\nThank you for using DebtTrack")
            break

        else: 
            print("\nInvalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()