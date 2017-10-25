from arctic import Arctic
from datetime import datetime as dt
import pandas as pd


# Connect to mongo
store = Arctic('localhost')
store.list_libraries()

# Create a library
store.initialize_library('username.scratch')

print('Current liberriess')
store.list_libraries()

# Get a library
library = store['username.scratch']

# Store some data in the library
df = pd.DataFrame({'prices': [1, 2, 3]},
                  [dt(2014, 1, 1), dt(2014, 1, 2), dt(2014, 1, 3)])
library.write('SYMBOL', df)

# # Read some data from the library
# # (Note the returned object has an associated version number and metadata.)
library.read('SYMBOL')
#
# # Store some data into the library
# library.write('MY_DATA', library.read('SYMBOL').data)
#
# # What symbols (keys) are stored in the library
# library.list_symbols()
#
# # Delete the data item
# library.delete('MY_DATA')
