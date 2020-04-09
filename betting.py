import asyncio
import reposti

class BettingInfo:
    _accounts = {}
    _currentBets = {}
    _contestant1 = ""
    _contestant2 = ""
    _bettingAllowed = False

    # TODO
    # def LoadFromJSon(path : str)
    # def SaveToJSon(path : str)

    def __init__(self):
        self._accounts = {}
        self._currentBets = {}
        self._contestant1 = ""
        self._contestant2 = ""

    def GetAccount(self, userID : str):
        if not userID in self._accounts:
            self._accounts[userID] = float(10000)
        return self._accounts[userID]

    def GetCurrentBet(self, userID : str):
        if not self.IsBettingAllowed():
            return None
        if userID in self._currentBets[self._contestant1]:
            return (self._contestant1, self._currentBets[self._contestant1][userID])
        if userID in self._currentBets[self._contestant2]:
            return (self._contestant2, self._currentBets[self._contestant2][userID])
        else:
            return None


    def Bet(self, userID : str, contestant : str, amount : float):
        if not userID in self._accounts:
            self._accounts[userID] = float(10000)
        
        if self._accounts[userID] < amount:
            raise

        contestant = contestant.lower()
        if not contestant in self._currentBets:
            self._currentBets[contestant] = {}
        
        self._currentBets[contestant][userID] = amount

    def IsBettingAllowed(self):
        return self._bettingAllowed

    def StartBetting(self, p1 : str, p2 : str):
        # TODO clear existing bets
        # TODO check that betting is not in progress
        self._contestant1 = p1.lower()
        self._contestant2 = p2.lower()
        self._bettingAllowed = True

    def EndBetting(self):
        # TODO check that betting is in progress
        self._bettingAllowed = False
    
    def ClearMatchup(self):
        self._contestant1 = ''
        self._contestant2 = ''
        self._bettingAllowed = False
        self._currentBets = {}

    def CalculateResults(self, winner : str):
        winner = winner.lower()

        # IDEA FOR PAYOUT FUNCTION: Max(2x or #BettingAgainst / #BettingFor)
        if winner != self._contestant1 and winner !=  self._contestant2:
            return None
        else:
            winner = self._contestant1
            loser = self._contestant2

            if(winner == self._contestant2):
                winner = self._contestant2
                loser = self._contestant1

            results = []
            for contestant, bets in self._currentBets.items():
                winningsModifier = -1
                if contestant == winner:
                    winningsModifier = 2# TODO calculate better odds here
                
                for userID, betAmount in bets.items():
                    amountWon = betAmount * winningsModifier
                    self._accounts[userID] += amountWon
                    results.append((userID, betAmount, self._accounts[userID]))
            
            return results

    def IsValidContestant(self, contestant : str):
        contestant = contestant.lower()
        return self._contestant1 == contestant or self._contestant2 == contestant
    
    def GetCurrentMatchup(self):
        return self._contestant1 + ' vs ' + self._contestant2

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
                except:
                    await ctx.send('<@' + strID + '> -- You cannot bet more than you have! You have ' + str(BettingInfo.GetAccount(strID)) + ' in the bank.')
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
