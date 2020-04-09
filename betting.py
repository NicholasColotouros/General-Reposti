import asyncio
import reposti

class BettingInfo:
    _accounts = {}
    _currentBets = {{}}
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

    def Bet(self, userID : str, contestant : str, amount : float):
        if not userID in self._accounts:
            self._accounts[userID] = float(10000)
        
        self._currentBets[contestant][userID] = amount

    def IsBettingAllowed(self):
        return self._bettingAllowed

    def StartBetting(self, p1 : str, p2 : str):
        # TODO clear existing bets
        # TODO check that betting is not in progress
        _contestant1 = p1
        _contestant2 = p2
        _bettingAllowed = True

    def EndBetting(self):
        # TODO check that betting is in progress
        # TODO payouts and clear bets... can send messages from here? Probably want a "payout bets function" instead
        self._bettingAllowed = False

    def IsValidContestant(self, contestant : str):
        return self._contestant1 == contestant or self._contestant2 == contestant

Lock = asyncio.Lock()
BettingInfo = BettingInfo()


@reposti.bot.command(pass_context=True)
async with Lock def bet(ctx, amount : float, contestant : str):
    if BettingInfo.IsBettingAllowed():
        if not BettingInfo.IsValidContestant(contestant):
            await ctx.send(contestant + ' is not a valid contestant. The current matchup is ' + Contestant1 + ' vs ' + Contestant2)
        else:
            # TODO trim float to 2 decimals
            strID = str(ctx.message.author.id)
            BettingInfo.Bet(strID, contestant, amount)
            await ctx.send('<@' + strID + '> is betting: ' + str(amount) + ' on ' + contestant)
    else:
        await ctx.send('Betting is not currently allowed.')

######## Admin commands ########
@reposti.bot.command(description='(admin) start betting', pass_context=True)
async with Lock def bet_start(ctx, p1 : str, p2 : str):
    if not reposti.is_admin(ctx.author):
        await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
    else:
        BettingInfo.StartBet(p1, p2)
        await ctx.send('Taking bets for ' + p1 + ' vs. ' + p2)
        

@reposti.bot.command(description='(admin) end betting', pass_context=True)
async with Lock def bet_end(ctx):
    if not reposti.is_admin(ctx.author):
        await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
    else:
        BettingInfo.EndBetting()
        await ctx.send('Betting closed! No more bets for the current match.')

@reposti.bot.command(description='(admin) Reset all accounts', pass_context=True)
async with Lock def bet_reset(ctx):
    if not reposti.is_admin(ctx.author):
        await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
    else:
        BettingInfo = BettingInfo()
        await ctx.send('All accounts reset')
