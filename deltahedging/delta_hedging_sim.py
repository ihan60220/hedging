# delta hedging is a way to hedge options
# so that the overall portfolio has a neutral delta
# deltas are calculated periodically
# and subsequently the portfolios are updated

price_of_option = []
price_of_underlying = []
delta = [0]

while True:
    price_of_option.append(float(input("option: ")))
    price_of_underlying.append(float(input("underlying: ")))

    if len(price_of_underlying) < 2 or len(price_of_option) < 2:
        print("too few data points")
        continue

    if price_of_underlying[-1] == price_of_underlying[-2]:
        print("no change in underlying, cannot calculate delta")
        continue
    
    delta.append((price_of_option[-1] - price_of_option[-2]) / (price_of_underlying[-1] - price_of_underlying[-2]))

    print("delta changed from", delta[-2], "to", delta[-1])
    print("hedge:", (delta[-1] - delta[-2]) * 100, "of underlying")
    