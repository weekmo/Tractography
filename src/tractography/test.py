from registration import register_all2
time_list = register_all2('data')
#time_list = {'A':30,'B':20,'C':10}
with open('time.txt','w') as f:
    for k,v in time_list.items():
        f.write(k+':'+str(v)+'\n')