# delta hedging algorithm

delta = float(input("Enter delta: "))
call_price = float(input("Buy call option at: "))
underlying_price = float(input("Price of underlying is: "))
short_amount = int(round(delta * 100))
print("\nFor this option, short", short_amount, "many shares to achieve delta neutral position.\n")
print("Total value of portfolio:", 100 * call_price - short_amount * underlying_price, "\n")