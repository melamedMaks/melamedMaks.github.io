from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__, template_folder='../templates')

# Фильтр для форматирования валюты
def format_currency(value):
    return '${:,.2f}'.format(value)

app.jinja_env.filters['format_currency'] = format_currency

# Главная страница с формой и результатами
@app.route('/', methods=['GET', 'POST'])
def calculate_profit():
    if request.method == 'POST':
        form_data = request.form

        try:
            # Извлечение и преобразование данных формы
            purchase_price = convert_to_float(form_data['purchase_price'])
            repair_price = convert_to_float(form_data['repair_price'])
            sale_price = convert_to_float(form_data['sale_price'])
            sale_percent = convert_to_float(form_data['sale_percent'])
            downpayment_percent = convert_to_float(form_data['downpayment_percent'])
            loan_interest_rate = convert_to_float(form_data['loan_interest_rate'])
            project_term_months = int(convert_to_float(form_data['project_term_months']))
            lenders_origination_fee_percent = convert_to_float(form_data['lenders_origination_fee_percent'])
            appraisal_fee = convert_to_float(form_data['appraisal_fee'])
            closing_costs = convert_to_float(form_data['closing_costs'])
            agent_fee_percent = convert_to_float(form_data['agent_fee_percent'])
            property_tax_percent = convert_to_float(form_data['property_tax_percent'])
            insurance_year = convert_to_float(form_data['insurance_year'])
            risks = convert_to_float(form_data['risks'])
            utilities_monthly = convert_to_float(form_data['utilities_monthly'])

            # Основные расчеты
            downpayment_amount = calculate_downpayment(purchase_price, downpayment_percent)
            loan_amount = calculate_loan_amount(purchase_price, downpayment_amount, repair_price)
            lenders_origination_fee = calculate_lenders_origination_fee(loan_amount, lenders_origination_fee_percent)
            agent_fee = calculate_agent_fee(sale_price, agent_fee_percent)
            total_downpayment = calculate_total_downpayment(downpayment_amount, lenders_origination_fee, appraisal_fee, closing_costs, agent_fee, risks)
            monthly_payment = calculate_monthly_payment(loan_amount, loan_interest_rate, insurance_year, utilities_monthly)
            total_loan_payments = calculate_total_loan_payments(monthly_payment, project_term_months)
            property_tax = calculate_property_tax(purchase_price, property_tax_percent)
            liquid_money = total_downpayment + repair_price / 2

            # Рассчет прибыли
            profit = calculate_profit(sale_price, purchase_price, repair_price, total_loan_payments, total_downpayment, downpayment_amount, agent_fee, property_tax, insurance_year, sale_percent)

            return render_template('result.html',
                                   profit=float(profit),
                                   total_downpayment=float(total_downpayment),
                                   liquid_money=float(liquid_money),
                                   lenders_origination_fee=float(lenders_origination_fee),
                                   monthly_payment=float(monthly_payment),
                                   total_loan_payments=float(total_loan_payments),
                                   agent_fee=float(agent_fee),
                                   property_tax=float(property_tax),
                                   insurance_year=float(insurance_year),
                                   utilities_monthly=float(utilities_monthly),
                                   risks=float(risks))
        except ValueError:
            return render_template('index.html', error="Please enter valid numeric values.")
    return render_template('index.html')

# Функции для конвертации значений
def convert_to_float(value, default=0.0):
    try:
        return float(value.replace('$', '').replace(',', '').replace('%', ''))
    except ValueError:
        return default

# Функции для расчетов
def calculate_downpayment(purchase_price, downpayment_percent):
    return round(purchase_price * (downpayment_percent / 100), 2)

def calculate_loan_amount(purchase_price, downpayment_amount, repair_price):
    return round((purchase_price - downpayment_amount) + repair_price, 2)

def calculate_lenders_origination_fee(loan_amount, lenders_origination_fee_percent):
    return round(loan_amount * (lenders_origination_fee_percent / 100), 2)

def calculate_agent_fee(sale_price, agent_fee_percent):
    return round(sale_price * (agent_fee_percent / 100), 2)

def calculate_total_downpayment(downpayment_amount, lenders_origination_fee, appraisal_fee, closing_costs, agent_fee, risks):
    return round(downpayment_amount + lenders_origination_fee + appraisal_fee + closing_costs + agent_fee + risks, 2)

def calculate_monthly_payment(loan_amount, loan_interest_rate, insurance_year, utilities_monthly):
    monthly_interest = loan_amount * (loan_interest_rate / 100) / 12
    insurance_monthly = insurance_year / 12
    return round(monthly_interest + insurance_monthly + utilities_monthly, 2)

def calculate_total_loan_payments(monthly_payment, project_term_months):
    return round(monthly_payment * project_term_months, 2)

def calculate_property_tax(purchase_price, property_tax_percent):
    return round(purchase_price * (property_tax_percent / 100), 2)

def calculate_profit(sale_price, purchase_price, repair_price, total_loan_payments, total_downpayment, downpayment_amount, agent_fee, property_tax, insurance_year, sale_percent):
    sale_price_after_percent = sale_price * (1 - sale_percent / 100)
    return round(sale_price_after_percent - purchase_price - repair_price - total_loan_payments - total_downpayment - property_tax - insurance_year + downpayment_amount - agent_fee, 2)

if __name__ == '__main__':
    app.run(debug=True)