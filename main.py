import requests
import re

def get_exchange_rates():
    try:
        response = requests.get("https://api.frankfurter.app/latest?from=USD")
        if response.status_code == 200:
            data = response.json()
            rates = data['rates']
            rates['USD'] = 1.0
            return rates
    except:
        return {
            'USD': 1.0, 'EUR': 0.92, 'GBP': 0.79, 'JPY': 150.5,
            'CAD': 1.35, 'AUD': 1.52, 'CHF': 0.88, 'CNY': 7.19
        }

def convert_currency(amount, from_curr, to_curr, rates):
    if from_curr == to_curr:
        return amount
    if from_curr != 'USD':
        amount = amount / rates[from_curr]
    return amount * rates[to_curr]

def show_rates(rates):
    print("\nExchange Rates (vs USD)")
    print("-" * 30)
    for curr in ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']:
        if curr in rates:
            print(f"1 USD = {rates[curr]:.4f} {curr}")

def main():
    print("Currency Converter")
    print("=" * 30)
    print("Commands:")
    print("  '100 USD to EUR' - convert")
    print("  'rates' - show rates")
    print("  'quit' - exit")
    print()
    
    rates = get_exchange_rates()
    
    while True:
        user_input = input("> ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'rates':
            show_rates(rates)
            continue
        
        match = re.search(r'(\d+(?:\.\d+)?)\s*([A-Za-z]{3})\s+(?:to|in)\s+([A-Za-z]{3})', user_input, re.IGNORECASE)
        
        if match:
            amount = float(match.group(1))
            from_curr = match.group(2).upper()
            to_curr = match.group(3).upper()
            
            if from_curr not in rates or to_curr not in rates:
                print("Currency not supported")
                continue
            
            result = convert_currency(amount, from_curr, to_curr, rates)
            print(f"{amount} {from_curr} = {result:.2f} {to_curr}")
        else:
            print("Try: 100 USD to EUR")

if __name__ == "__main__":
    main()
