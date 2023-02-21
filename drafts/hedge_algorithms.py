import time
import datetime
#Algorithm to find strike position
oddsA = 0#Static, found through Selenium driver#
oddsB = 0#Dynamic, found through Selenium driver#
stakeA = 0#Can either be prompted input or detected from Selenium driver#
stakeA = int(stakeA)
stakeB = 0
payoutA = 0
TruepayoutB = 0
Derivativecheck = True
oddsBlist = []
dx = []
dydx = 0
#Determines value given out if a side wins
def determinesidepayout(odds,payout,stake):
    if odds > 0:
        payout = odds * (stake / 100)
    elif odds < 0:
        payout = (100 / abs(odds)) * stake


def commitSideBbet():
    #whatever the Selenium code is to execute Side B bet on the site
    pass

determinesidepayout(oddsA, payoutA, stakeA) #Upon locked in stakeA


def determinestakeB():
    fullstakeB = payoutA - stakeA
    lamestakeB = (.5 * fullstakeB) - (.5 * stakeA) + stakeA 
    stakeB = .5 * (fullstakeB + lamestakeB)
    stakeB = round(stakeB,2)
    determinesidepayout(oddsB, TruepayoutB, stakeB)
    derivativefinder(oddsB,oddsBlist) #Placeholder for derivative equation
    if (TruepayoutB - stakeB - stakeA) > 0) and (Derivativecheck = False):#Get Paul to fix this if statement
        commitSideBbet(stakeB)
        print("The value of this hedge is: " + str(TruepayoutB - stakeB - stakeA))
        hedgelog = open("closedpositionslog.txt")
        x = datetime.datetime.now()
        hedgelog.write(nameA + " vs. " + nameB + x.strftime("%c") + "   Total Leveraged: " + str(stakeA + stakeB) + "   Payout:"+ str(TruepayoutB - stakeB - stakeA))
        hedgelog.close()
        del oddsBlist[:]
    else:
        pass




#Basic derivative algorithm. Will get better over time with better analysis and data feeding. Look into databases
def derivativefinder(odds,oddslist):
    timebetweenchange = time.ctime()#Placeholder until Paul shows me how to time
    if odds != oddslist[-1]:
        oddslist.append(odds)
        dx.append(timebetweenchange)
        timebetweenchange = 0
        dydx = (oddslist[-2] - oddslist[-1]) / dx[-1]
        if dydx > 0:
            Derivativecheck = True
        elif dydx < 0:
            Derivativecheck = False
        if len(oddslist) > 4:
            oddslist.pop(0)
        else:
            pass









