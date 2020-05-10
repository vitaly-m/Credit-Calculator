import math
import argparse


def calc_months(principal, payment, interest):
    m_irate = interest / 12 / 100
    months = math.ceil(math.log(payment / (payment - m_irate * principal), 1 + m_irate))
    years = math.floor(months // 12)
    y_months = months % 12
    if years == 0:
        print(f"You need {y_months} month{'s' if months > 1 else ''} to repay the credit!")
    else:
        if y_months == 0:
            print(f"You need {years} year{'s' if years > 1 else ''} to repay the credit!")
        else:
            print(f"You need {years} year{'s' if years > 1 else ''} and",
                  f"{y_months} month{'s' if months > 1 else ''} to repay the credit!")
    print(f"Overpayment = {math.floor(payment * months - principal)}")


def calc_payment(p_type, principal, months, interest):
    m_irate = interest / 12 / 100
    if p_type == "annuity":
        payment = math.ceil(principal * m_irate * math.pow(1 + m_irate, months) \
                  / (math.pow(1 + m_irate, months) - 1))
        print(f"Your annuity payment = {payment}!")
        print(f"Overpayment = {math.floor(payment * months - principal)}")
    elif p_type == "diff":
        payments = []
        for m in range(1, months + 1):
            payment = math.ceil(principal / months + m_irate * (principal - principal * (m - 1) / months))
            payments.append(payment)
            print(f"Month {m}: paid out {payment}")
        print(f"\nOverpayment = {math.floor(sum(payments) - principal)}")


def calc_credit(payment, months, interest):
    m_irate = interest / 12 / 100
    m_irate_n = math.pow(1 + m_irate, months)
    principal = math.floor(payment / (m_irate * m_irate_n / (m_irate_n - 1)))
    print(f"Your credit principal = {principal}!")
    print(f"Overpayment = {payment * months - principal}")


def validate_args(arguments):
    if arguments.type is None:
        print("Incorrect parameters.")
        return False
    if arguments.type == "diff" and arguments.payment is not None:
        print("Incorrect parameters.")
        return False
    if arguments.payment is not None and arguments.payment <= 0:
        print("Incorrect parameters.")
        return False
    if arguments.interest is not None and arguments.interest < 0:
        print("Incorrect parameters.")
        return False
    if arguments.periods is not None and arguments.periods < 0:
        print("Incorrect parameters.")
        return False
    if arguments.principal is not None and arguments.principal < 0:
        print("Incorrect parameters.")
        return False
    args_len = len([a for a in args.__dict__.keys() if a != "type" and args.__dict__[a] is not None])
    if args.type == "annuity" and args_len < 3:
        print("Incorrect parameters.")
        return False
    if args.type == "diff" and args_len < 2:
        print("Incorrect parameters.")
        return False
    return True


parser = argparse.ArgumentParser()
parser.add_argument("--type",
                    help='indicates the type of payments: "annuity" or "diff" (differentiated)',
                    choices=("annuity", "diff"))
parser.add_argument("--payment",
                    help="monthly payment, can be used ony with --type=diff",
                    type=int)
parser.add_argument("--principal",
                    help="""is used for calculations of both types of payment.
                    You can get its value knowing the interest, annuity payment and periods""",
                    type=float)
parser.add_argument("--periods",
                    help="""parameter denotes the number of months needed to repay the credit.
                    It's calculated based on the interest, annuity payment and principal.""",
                    type=int)
parser.add_argument("--interest",
                    help="is specified without a percent sign",
                    type=float)
args = parser.parse_args()

if not validate_args(args):
    exit(-1)
if args.principal is None:
    calc_credit(args.payment, args.periods, args.interest)
if args.payment is None:
    calc_payment(args.type, args.principal, args.periods, args.interest)
if args.periods is None:
    calc_months(args.principal, args.payment, args.interest)
