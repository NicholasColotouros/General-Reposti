import asyncio
import json
import reposti

from pathlib import Path

class NoMoneyToBetError(Exception):
    """You're betting money you don't have"""
    pass

class NonPositiveBetError(Exception):
    """You can only bet positive amounts of money"""
    pass

BETTING_ACCOUNTS_PATH = "secret/BettingAccounts.json"
class BettingInfo:
    _accounts = {}
    _currentBets = {}
    _contestant1 = ""
    _contestant2 = ""
    _matchup = ""
    _bettingAllowed = False

    def __init__(self):
        if Path(BETTING_ACCOUNTS_PATH).is_file():
            with open(BETTING_ACCOUNTS_PATH) as f: 
                self._accounts = json.load(f)
        else:
            self._accounts = {}

        self._currentBets = {}
        self._contestant1 = ""
        self._contestant2 = ""
        self._matchup = ""

    def GetAccount(self, userID : str):
        if not userID in self._accounts:
            self._accounts[userID] = float(10000)
        return self._accounts[userID]

    def GetCurrentBet(self, userID : str):
        if not self.IsBettingAllowed():
            return None
        
        if userID in self._currentBets[userID]:
            return (self._currentBets[userID][0], self._currentBets[userID][1])
        else:
            return None


    def Bet(self, userID : str, contestant : str, amount : float):
        if not userID in self._accounts:
            self._accounts[userID] = float(10000)
        
        # You can't bet money you can't have
        if self._accounts[userID] < amount:
            raise NoMoneyToBetError
        if amount <= 0:
            raise NonPositiveBetError

        self._currentBets[userID] = (contestant, amount)

    def IsBettingAllowed(self):
        return self._bettingAllowed

    def StartBetting(self, p1 : str, p2 : str):
        # TODO clear existing bets
        # TODO check that betting is not in progress
        self._matchup = p1 + ' vs. ' + p2
        self._contestant1 = p1.lower()
        self._contestant2 = p2.lower()

        if(self._contestant1 == self._contestant2):
            self.StartBetting(p1 + '1', p2 + '2')

        self._bettingAllowed = True

    def EndBetting(self):
        # TODO check that betting is in progress
        self._bettingAllowed = False
    
    def ClearMatchup(self):
        self._contestant1 = ''
        self._contestant2 = ''
        self._bettingAllowed = False
        self._currentBets = {}

    def CalculateResults(self, declaredWinner : str):
        declaredWinner = declaredWinner.lower()

        # IDEA FOR PAYOUT FUNCTION: Max(2x or #BettingAgainst / #BettingFor)
        if declaredWinner != self._contestant1 and declaredWinner !=  self._contestant2:
            return None
        else:
            winner = self._contestant1
            loser = self._contestant2

            if(declaredWinner == self._contestant2):
                winner = self._contestant2
                loser = self._contestant1

            lossModifier = -1
            winModifier = 2 # TODO calculate better odds here

            results = []
            for userID, bet in self._currentBets.items():
                contestant = bet[0]
                betAmount = bet[1]

                winningsModifier = lossModifier
                if contestant == winner:
                    winningsModifier = winModifier

                amountWon = betAmount * winningsModifier
                self._accounts[userID] += amountWon
                results.append((userID, amountWon, self._accounts[userID]))
            
            self._save()
            return results

    def IsValidContestant(self, contestant : str):
        contestant = contestant.lower()
        return self._contestant1 == contestant or self._contestant2 == contestant
    
    def GetCurrentMatchup(self):
        return self._matchup

    def _save(self):
        with open(BETTING_ACCOUNTS_PATH, 'w') as f:
            json.dump(self._accounts, f)


Lock = asyncio.Lock()
BettingInfo = BettingInfo()


@reposti.bot.command(pass_context=True)
async def bet(ctx, amount : float, contestant : str):
    await Lock.acquire()
    try:
        if BettingInfo.IsBettingAllowed():
            if not BettingInfo.IsValidContestant(contestant):
                await ctx.send(contestant + ' is not a valid contestant. The current matchup is ' + BettingInfo.GetCurrentMatchup())
            else:
                # TODO trim float to 2 decimals
                strID = str(ctx.message.author.id)
                try:
                    BettingInfo.Bet(strID, contestant, amount)
                    await ctx.send('<@' + strID + '> is betting: ' + str(amount) + ' on ' + contestant)
                except NoMoneyToBetError:
                    await ctx.send('<@' + strID + '> -- You cannot bet more than you have! You have ' + str(BettingInfo.GetAccount(strID)) + ' in the bank.')
                except NonPositiveBetError:
                    await ctx.send('<@' + strID + '> -- You must bet a positive amount of money instead of ' + str(amount))
        else:
            await ctx.send('Betting is not currently allowed.')
    finally:
        Lock.release()


# TODO format the amount as currency
@reposti.bot.command(pass_context=True)
async def bet_get_account(ctx):
    await Lock.acquire()
    try:
        strID = str(ctx.message.author.id)
        amount = BettingInfo.GetAccount(strID)
        await ctx.send('<@' + strID + '> has $' + str(amount) + ' in their account.')
    finally:
        Lock.release()

# TODO format the amount as currency
@reposti.bot.command(pass_context=True)
async def bet_get(ctx):
    await Lock.acquire()
    try:
        strID = str(ctx.message.author.id)
        result = BettingInfo.GetCurrentBet(strID)
        
        bet = 'no active bets.'
        if result is not None:
            bet = '$' + str(result[1]) + ' on ' + result[0]

        await ctx.send('<@' + strID + '> has ' + bet)
    finally:
        Lock.release()


######## Admin commands ########
@reposti.bot.command(description='(admin) start betting', pass_context=True)
async def bet_start(ctx, p1 : str, p2 : str):
    await Lock.acquire()
    try:
        if not reposti.is_admin(ctx.author):
            await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
        else:
            BettingInfo.StartBetting(p1, p2)
            await ctx.send('Taking bets for ' + BettingInfo.GetCurrentMatchup())
    finally:
        Lock.release()
        

@reposti.bot.command(description='(admin) end betting', pass_context=True)
async def bet_close(ctx):
    await Lock.acquire()
    try:
        if not reposti.is_admin(ctx.author):
            await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
        else:
            BettingInfo.EndBetting()
            await ctx.send('Betting closed! No more bets for the current match.')
    finally:
        Lock.release()

@reposti.bot.command(description='(admin) calculate bet results', pass_context=True)
async def bet_result(ctx, winner : str):
    await Lock.acquire()
    try:
        if not reposti.is_admin(ctx.author):
            await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
        else:
            results = BettingInfo.CalculateResults(winner)
            if results is None:
                await ctx.send(winner + ' is not a valid contestant. The current matchup is ' + BettingInfo.GetCurrentMatchup())
            else:
                BettingInfo.ClearMatchup()

                resultsMsg = winner + ' takes the match!\n\n**Results:**\n'
                for userID, winnings, total in results:
                    resultsMsg += '<@' + userID + '> wins $' + str(winnings) + '. $' + str(total) + ' left in the bank.\n'
                await ctx.send(resultsMsg)
    finally:
        Lock.release()

@reposti.bot.command(description='(admin) Reset all accounts', pass_context=True)
async def bet_reset(ctx):
    await Lock.acquire()
    try:
        if not reposti.is_admin(ctx.author):
            await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
        else:
            BettingInfo = BettingInfo()
            await ctx.send('All accounts reset')
    finally:
        Lock.release()

# TODO payout function
