print("================================")
print("       DEBTTRACK")
print("================================")
print("Personal Debt Management System")

creditor_name = input("Creditor Name: ")
debt_name = input("Enter the debt name: ")
balance = float(input("Enter the current blaance: R"))
interest_rate = float(input("Enter the annual interest rate (%): "))
monthly_payment = float(input("Enter the monthly payment: R"))

annual_payment = monthly_payment * 12 

monthly_interest_rate = interest_rate / 100 /12
monthly_interest_amount = balance * monthly_interest_rate

if balance <= 0:
    print("Error: Balance must be greater than R0.")
elif monthly_payment <= 0:
    print("Error: Monthly payment must be greater than R0.")
elif monthly_payment <= monthly_interest_amount:
    print("Warning: Your monthly payment is too low to reduce this debt.")
else: 
    print("Payment is sufficient to reduce the debt.")
    remaining_balance = balance 
    months_to_payoff = 0
    total_interest = 0

    while remaining_balance > 0:
        interest_for_month = remaining_balance * monthly_interest_rate

        total_interest = total_interest + interest_for_month
        remaining_balance = remaining_balance + interest_for_month

        payment_this_month = min(monthly_payment, remaining_balance)

        remaining_balance = remaining_balance - payment_this_month
        months_to_payoff = months_to_payoff + 1
        
    years = months_to_payoff//12
    remaining_months = months_to_payoff % 12

    total_paid = balance + total_interest

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
