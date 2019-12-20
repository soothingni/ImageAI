list1 = [100, 200, 300]
def getItem(idx):
    print("Start")
    try:
        print(list1[idx])
        print("normally execute")
        return(list1[idx])
    except IndexError as e:
        print(str(e).title(), ": abnormal event...and next")    
    finally:
        print("finally block execute")
        print("End")
