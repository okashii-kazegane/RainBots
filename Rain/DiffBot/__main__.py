import sys
from Rain.DiffBot.DiffBot import DiffBot
from Rain.Common.Configs import Configs

mToken = ''
dToken = ''
if len(sys.argv) >= 2:
    dToken = sys.argv[1]
Configs.initialize(mToken, dToken)
diffbot = DiffBot()
diffbot.run(Configs.diffbotToken, reconnect=True)
