from Instance import Instance
from SQLiteDriver import SQLiteDriver
from Configuration import Configuration

def run_one(name):
    Configuration.load_filters()
    Instance(name).run()

if __name__ == '__main__':
    run_one('wiki-pct-english-speakers')

    #Instance('health-care-system-description').run()
    
    #Instance('unemployment-rate-australia').run()
    #Instance('unemployment-rate-canada').run()
    #Instance('unemployment-rate-france').run()
    #Instance('unemployment-rate-germany').run()
    #Instance('unemployment-rate-uk').run()
    #Instance('unemployment-rate-usa').run()