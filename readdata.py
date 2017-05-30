import pandas as pd
folder = 'H:/dataset/2017datachallenge/'
filename = '20170315'
filename = 'test'
pd = pd.read_csv(folder+filename+'.csv')

def namemerge(a):
    return str(a[0])+','+str(a[1])

pd['pos'] = pd[['lat','lng']].apply(namemerge,axis=1)
print(pd[['phone','lat','lng','pos']])
poss = pd['pos'].unique()
print(type(poss))
# pd['gps'] = pd['lat'].str.cat(pd['lng'],seq=',')
for pos in poss:
    print(pos)
print(len(poss))
# print(len(pd[['lng','lat']].unique()))
# gps = pd[['lng','lat']].unique()
# print(gps)
# print(pd.head())