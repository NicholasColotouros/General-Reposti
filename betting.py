import reposti

@reposti.bot.command(pass_context=True)
async def bet(ctx, amount : float, contestant : str):
    await ctx.send('<@' + str(ctx.message.author.id) + '> is betting: ' + str(amount) + ' on ' + contestant)

@reposti.bot.command(description='start betting', pass_context=True)
async def bet_start(ctx, p1 : str, p2 : str):
    if not reposti.is_admin(ctx.author):
        await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
    else:
        await ctx.send('Taking bets for ' + p1 + ' vs. ' + p2)

@reposti.bot.command(description='start betting', pass_context=True)
async def bet_end(ctx):
    if not reposti.is_admin(ctx.author):
        await ctx.send('You are on this counsel, but we do not grant you the rank of master.\nOnly<@' + reposti.ADMIN_ID + '> can do this.')
    else:
        await ctx.send('Betting closed! No more bets for the current match.')