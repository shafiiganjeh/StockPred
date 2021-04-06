#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 20:59:42 2021

@author: borz
"""

import igraph as gr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import os
import cairo

def add_vertex_with_attrs(graph, attrs):
    n = graph.vcount()
    graph.add_vertices(1)
    for key, value in attrs.items():
        graph.vs[n][key] = value


download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files")
df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Liste.csv"),index_col=False,header=None)
dates=list(pd.read_csv(os.path.join(download_path, df.iat[0, 0][df.iat[0, 0].find("=")+1:]+".csv"),skip_blank_lines=False)["Date"])
N=df.shape[1]
liste=[]
vol=[]

start=1500
end=2295
#2295
#and (check["Close"].var()/check["Close"].mean()>0.05)
df1 = pd.DataFrame()
for i in range(N):   
    if df.iat[1, i]=='OK':
        check=pd.read_csv(os.path.join(download_path, df.iat[0, i][df.iat[0, i].find("=")+1:]+".csv"),skip_blank_lines=False)[["Date","Volume","Close"]]
        templist=list(set(check["Date"]) & set(dates[start:end])) 
#        print(check["Close"].var()/check["Close"].mean())
        if (check[check["Date"].isin(templist)]["Volume"][-11:-1].sum()>5000000) :
            print(i)
            print(df.iat[0, i][df.iat[0, i].find("=")+1:-4])
            vol.append(check[check["Date"].isin(templist)]["Volume"].dropna().iloc[-1])
            df2 = pd.read_csv(os.path.join(download_path, df.iat[0, i][df.iat[0, i].find("=")+1:]+".csv"),skip_blank_lines=False)
            df2 = df2[df2["Date"].isin(templist)]
            df2=pd.concat([df2["Date"], (df2["Open"] - df2["Close"])/(df2["Open"] + df2["Close"])], axis=1).set_index(df2.columns[0])
            df1=pd.concat([df1, df2], axis=1)
            liste.append(df.iat[0, i][df.iat[0, i].find("=")+1:-4])     

df1.columns = liste
mat=df1.corr()
vol=(np.log2(vol)*np.log2(vol)/1)

#color_map = plt.cm.get_cmap('RdBu')
#reversed_color_map = color_map.reversed()  
#plt.pcolormesh(mat, cmap=reversed_color_map)
#plt.title('corr-H')
#plt.colorbar()

g = gr.Graph()
g.add_vertices(len(liste))
g.vs["Label"] = liste
g.vs["size"] = vol

maxX=[1] * len(liste)
maxY=[1] * len(liste)
minX=[-1] * len(liste)
minY=[-1] * len(liste)

li=[]

for i in range(mat.shape[0]):
    for j in range(i,mat.shape[0]):
        if (i != j) and (np.absolute(mat.iloc[i, j])>.2):
            g.add_edges([(i, j)])
        
a=0      
for i in range(mat.shape[0]):
    for j in range(i,mat.shape[0]):
        if (i != j) and (np.absolute(mat.iloc[i, j])>.2):
            g.es[a]["weight"]=mat.iloc[i, j]
            a=a+1
            
#add_vertex_with_attrs(g, {"name": "dummy"})
#
#for i in range(mat.shape[0]):
#    g.add_edges([(i, mat.shape[0])])
#    g.es[a]["weight"]=0
#    a=a+1
#            
#g.delete_vertices(g.vs.select(name="HTDF"))
            
g.write_gml("asd.gml")
          
print(len(liste) )
temp=np.sqrt(len(liste) )*150
deg =g.degree(mode="all")
deg=[x+1 for x in deg]


#layout = g.layout_fruchterman_reingold(weights=g.es["weight"],niter=100000,start_temp=temp)
#layout =g.layout_circle()

#layout =g.layout_kamada_kawai()
#layout = g.layout_fruchterman_reingold(weights=g.es["weight"],niter=1000,start_temp=temp)
#,maxx=maxX,miny=minY,minx=minX
#layout = g.layout_fruchterman_reingold(weights=g.es["weight"],niter=5000)


#gr.plot(g, "name2.pdf",layout=layout,bbox=(10000,10000),vertex_label=g.vs["name"],vertex_size=g.vs["size"],margin=1,asp = 0.35)
