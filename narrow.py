#!/usr/bin/python

import sys
import getopt
import os
import pandas as pd
class banana:
    def __init__(self):
        self.simper = ""
        self.taxon = ""
        self.numberofOtu = 20
        self.OrderBy = 'DissSD'
    def simperparser(self, simperfile):
        otuDic={}
        with open(simperfile) as f:
            
            line= f.readline()
            while line:
                if line.startswith("Species"):
                    linenum= 0
                    line= f.readline()
                    while(line.startswith("Otu")): 

                        
                        linenum+= 1
                        feature = line.split('\t')
                        
                        if feature[0] in otuDic:
                            freq =1 + otuDic[feature[0]][0]
                            abund1 = float(feature[1]) + otuDic[feature[0]][1]
                            abund2 = float(feature[2]) + otuDic[feature[0]][2]
                            avDiss = float(feature[3])+ otuDic[feature[0]][3]
                            dissSd = float(feature[4])+ otuDic[feature[0]][4]
                            Contrib = float(feature[5])+ otuDic[feature[0]][5]
                            cum = float(feature[6])+ otuDic[feature[0]][6]
                            otuDic[feature[0]] = [freq, abund1 ,abund2 ,avDiss ,dissSd ,Contrib,cum]
                        else:
                            freq = 1
                            abund1 = float(feature[1])
                            abund2 = float(feature[2])
                            avDiss = float(feature[3])
                            dissSd = float(feature[4])
                            Contrib = float(feature[5])
                            cum = float(feature[6])
                            otuDic[feature[0]] = [freq,abund1,abund2,avDiss,dissSd,Contrib,cum]
                            
                        line = f.readline()
                else:
                    line= f.readline()
                    continue
        df = pd.DataFrame.from_dict(otuDic)
        print(df)
    def spitOTU(self,simper,taxon,numberofOtu,orderBy,taxonomyColumn):
        df = pd.read_csv(simper, index_col = [0]).dropna()
        dft = pd.read_csv(taxon, sep=',', index_col = [0])
        #print(df)
        #df['AvAbundSub'] = df['AvAbund1'] - df['AvAbund2']
        #df['AvAbundSub'] = df['AvAbundSub'].abs()
        #cols = ['AvAbundSub', 'AvDiss']
        ####df['AvAbundSubXContrib'] = df['AvAbundSub'] * df['Contrib']
        ####df['AvAbundSubXAvDiss'] = df['AvAbundSub'] * df['AvDiss']
        ####df['AvAbundSubXDissSD'] = df['AvAbundSub'] * df['DissSD']
        #df['Rankfunction'] = df.sort_values(cols, ascending=True).groupby(cols, sort=False).ngroup() + 1
        
        #df['Rank']= df[str(orderBy)].rank()

        #df = df.sort_values('Rank', ascending = True) #dropped the duplicates
        #dropped the duplicates 
        df = df.sort_values(orderBy, axis = 0, ascending=False).head(int(numberofOtu))
        if len(taxonomyColumn) <1:
            df2 = dft.loc[df.index]
            df22 = df2
            df3 = df2.join(df, lsuffix='_caller', rsuffix='_other')        
        else:
            df2 = dft.loc[df.index]
            df22 = df2[taxonomyColumn].to_frame()
            #print(df22)
            df3 = df22.join(df, lsuffix='_caller', rsuffix='_other')
        #df23.to_csv('finalAD23.csv',index=True, sep=',')  
        

        #df3['Rank']= df3['DissSD'].rank()

        #df = df.sort_values('Rank', ascending = True) #dropped the duplicates
        #dropped the duplicates
        #print(df3[orderBy])

        #df5 = df22.sort_values(orderBy, axis = 0, ascending=False).head(int(numberofOtu))
        print(df22)
        #df5 = df3.groupby('Taxonomy.6').sum()
        #df5 = df3.sort_values('DissSD', ascending=False).head(50)
        #df5.to_csv('finalAD.csv',index=True, sep=',')  
    def main(self, argv):
        #print (argv)
        simper = self.simper
        taxon = self.taxon
        numberofOtu = 20
        OrderBy = 'DissSD'
        taxonomyColumn = ''
        try:
            opts, args = getopt.getopt(argv,"h:s:t:n:o:c",["simperFile=","taxonomyFile=","numberofOtu=", "orderbycomulninSimper=","taxonomyColumn="])
        except getopt.GetoptError:
            print ('banana.py -s <simperFile> -t <taxonomyFile> -n <numberofOtu> -o <orderbycomulninSimper> -c <taxonomyColumn>') 
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print ('banana.py -s <simperFile> -t <taxonomyFile> -n <numberofOtu> -o <orderbycomulninSimper> -c <taxonomyColumn>')
                sys.exit(2)
            elif opt in ("-s", "--simperFile"):
                simper = arg
                #print(opt,arg)
            elif opt in ("-t", "--taxonomyFile"):
                taxon = arg      
                #print(opt,arg)
            elif opt in ("-n", "--numberofOtu"):
                numberofOtu = int(arg)
            elif opt in ("-o", "--orderbycomulninSimper"):
                OrderBy = arg
                #print(opt,arg)
            elif opt in ("-c", "--taxonomyColumn"):
                taxonomyColumn = argv[-1]
                #print(opt,argv[-1])

          

        #self.simperparser(simper)
        self.spitOTU(simper,taxon,numberofOtu,OrderBy,taxonomyColumn)

if __name__ == "__main__":
    ban = banana()
    ban.main(sys.argv[1:])