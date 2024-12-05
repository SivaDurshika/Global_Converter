import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout

class CurrencyConverterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.amount_input = TextInput(hint_text="Enter amount", size_hint_y=None, height=40, multiline=False)
        self.layout.add_widget(self.amount_input)

        # Dropdown for selecting currencies
        self.dropdown_from = DropDown()
        self.dropdown_to = DropDown()
        self.currencies = ['USD', 'EUR', 'INR', 'GBP', 'AUD', 'CAD', 'JPY']  # Add more currencies as needed
        
        self.from_button = Button(text="Select From Currency", size_hint_y=None, height=40)
        self.from_button.bind(on_release=self.dropdown_from.open)
        self.dropdown_from.bind(on_select=lambda instance, x: self.set_from_currency(x))
        self.layout.add_widget(self.from_button)

        self.to_button = Button(text="Select To Currency", size_hint_y=None, height=40)
        self.to_button.bind(on_release=self.dropdown_to.open)
        self.dropdown_to.bind(on_select=lambda instance, x: self.set_to_currency(x))
        self.layout.add_widget(self.to_button)

        self.result_label = Label(text="Converted Amount: ", size_hint_y=None, height=40)
        self.layout.add_widget(self.result_label)

        self.convert_button = Button(text="Convert", size_hint_y=None, height=40)
        self.convert_button.bind(on_press=self.convert_currency)
        self.layout.add_widget(self.convert_button)

        # Add currencies to dropdown menus
        for currency in self.currencies:
            self.dropdown_from.add_widget(Button(text=currency, size_hint_y=None, height=40))
            self.dropdown_to.add_widget(Button(text=currency, size_hint_y=None, height=40))

        self.from_currency = 'USD'
        self.to_currency = 'INR'

        return self.layout

    def set_from_currency(self, currency):
        self.from_currency = currency
        self.from_button.text = f"From: {currency}"

    def set_to_currency(self, currency):
        self.to_currency = currency
        self.to_button.text = f"To: {currency}"

    def convert_currency(self, instance):
        amount = self.amount_input.text
        if not amount:
            self.result_label.text = "Please enter a valid amount"
            return

        try:
            amount = float(amount)
        except ValueError:
            self.result_label.text = "Invalid amount entered"
            return

        # Fetch conversion rate from the API
        url = f"https://api.exchangerate-api.com/v4/latest/{self.from_currency}"
        response = requests.get(url)
        data = response.json()

        if 'rates' in data:
            rates = data['rates']
            conversion_rate = rates.get(self.to_currency)

            if conversion_rate:
                converted_amount = amount * conversion_rate
                self.result_label.text = f"Converted Amount: {converted_amount:.2f} {self.to_currency}"
            else:
                self.result_label.text = f"Error: Unable to convert to {self.to_currency}"
        else:
            self.result_label.text = "Error fetching conversion rates"

if __name__ == "__main__":
    CurrencyConverterApp().run()