import sys

def main():

    cval=0          #initialize counter value
    interval=2     # counter interval 
    count = int(sys.argv[1])            # takes user count 
    source=1000
    dst=100
    file_dst=200
    port_num=2222
    print("rule active prio match action")
    for i in range(0,(count),5):
        #print("R"+str(i)+" true"+" 100 "+" (SMTP.MTA="+str(i)+")"+" add(R"+str((i+1))+")"+",add(R"+str((i+2))+")"+",delete("+"R"+str(i)+")"+",send()"+"\n" ,%(i,i,i+1,i+2,i))
        print("R{0} false 100 src={1} drop()".format(i,source))
        print("R{0} false 50 src={1},dst={2} add(R{3}),drop()".format(i+1,source,dst,i))
        print("R{0} false 50 src={1},dst={2} add(R{3}),send()".format(i+2,source,file_dst,i+1))
        print("R{0} true 40 dst={1},port={2} add(R{3}),send()".format(i+3,source,port_num,i+2))
        print("R{0} true 10 * send()".format(i+4))
        source=source+1


if __name__ == "__main__":
    main()
