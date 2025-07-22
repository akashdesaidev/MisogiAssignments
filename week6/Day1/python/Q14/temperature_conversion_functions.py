def celcius_to_fahrenheit(celcius):
    return (celcius * 9/5) + 32

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_celcius(kelvin):
    return kelvin - 273.15

print(celcius_to_fahrenheit(0),"F")
print(format(fahrenheit_to_kelvin(32),".2f"),"K")
print(format(kelvin_to_celcius(300),".2f"),"C")





