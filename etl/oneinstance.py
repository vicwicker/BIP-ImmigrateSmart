from Instance import Instance
from SQLiteDriver import SQLiteDriver

sql = SQLiteDriver()

sql.close()

#Instance('health-care-system-description').run()

Instance('unemployment-rate-australia').run()
#Instance('unemployment-rate-canada').run()
#Instance('unemployment-rate-france').run()
#Instance('unemployment-rate-germany').run()
#Instance('unemployment-rate-uk').run()
#Instance('unemployment-rate-usa').run()