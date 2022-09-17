import LEACH
import FLEACH

def main():
    # myLeach = LEACH.LEACHSimulation(n=100)
    # myLeach.start()
    # myFLeach = FLEACH.FLEACHSimulation(n=100)
    # myFLeach.start()
    myFLeach2 = FLEACH.FLEACHSimulation(n=100, version=2)
    myFLeach2.start()

if __name__ == '__main__':
    main()
