import client

bovada = client.startup()

while True:
    client.run_hedge(bovada)
    
    quit = input("quit (y/n)?: ")
    
    if quit == "y":
        break