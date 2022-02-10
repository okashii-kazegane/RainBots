import sys
from Rain.Monsoon.Monsoon import Monsoon
from Rain.Common.Configs import Configs

mToken = ''
dToken = 'Error'
if len(sys.argv) >= 2:
    mToken = sys.argv[1]
Configs.initialize(mToken, dToken)
monsoon = Monsoon()
monsoon.run(Configs.monsoonToken, reconnect=True)
