from chatterbotapi import ChatterBotFactory, ChatterBotType


def botChat (message):
    factory = ChatterBotFactory()
    bot = factory.create(ChatterBotType.PANDORABOTS, "b0dafd24ee35a477")
    bot2session = bot.create_session()
    send = message.strip('<@273529250689318923>')
    if not send:
        return "Don't give me silence..."
    else:
        return bot2session.think(send)
