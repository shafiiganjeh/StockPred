#this is for creating a correlation matrix to find high correlating stocks and visualize the correlations with a bubble graph

import igraph as gr
import numpy as np
import pandas as pd

def VolP(DF): 
    return np.sqrt(len(DF))*DF.std()


df = pd.read_csv( "fListe.csv",index_col=False,header=None)
dates=list(pd.read_csv(df.iat[0, 0][df.iat[0, 0].find("=")+1:]+".csv",skip_blank_lines=False)["Date"])
N=df.shape[1]
liste=[]
volume=[]
vol=[]
start=1600
end=2295

df1 = pd.DataFrame()

for i in range(N):   
    if df.iat[1, i]=='OK':
        check=pd.read_csv( df.iat[0, i][df.iat[0, i].find("=")+1:]+".csv",skip_blank_lines=False)[["Date","Volume","Close"]]
        templist=list(set(check["Date"]) & set(dates[start:end])) 
        if (check[check["Date"].isin(templist)]["Volume"][-11:-1].sum()>5000000) :
#            print(i)
            volume.append(check[check["Date"].isin(templist)]["Volume"].dropna().iloc[-1])
            df2 = pd.read_csv(df.iat[0, i][df.iat[0, i].find("=")+1:]+".csv",skip_blank_lines=False)
            df2 = df2[df2["Date"].isin(templist)]
            df2=pd.concat([df2["Date"], (df2["Open"] - df2["Close"])/(df2["Open"] + df2["Close"])], axis=1).set_index(df2.columns[0])
            vol.append(VolP(df2))
            df1=pd.concat([df1, df2], axis=1)
            liste.append(df.iat[0, i][df.iat[0, i].find("=")+1:-4])     

df1.columns = liste
mat=df1.corr()
volume=(np.log2(volume)*np.log2(volume)/1)

g = gr.Graph()
g.add_vertices(len(liste))
g.vs["Label"] = liste
g.vs["Size"] = volume
g.vs["Vol"] = vol


for i in range(mat.shape[0]):
    for j in range(i,mat.shape[0]):
        if (i != j) and (np.absolute(mat.iloc[i, j])>.6):
            g.add_edges([(i, j)])
        
a=0      
for i in range(mat.shape[0]):
    for j in range(i,mat.shape[0]):
        if (i != j) and (np.absolute(mat.iloc[i, j])>.6):
            g.es[a]["weight"]=mat.iloc[i, j]
            a=a+1
            
            
g.write_gml("GRAPH.gml")

        
print(len(liste) )
