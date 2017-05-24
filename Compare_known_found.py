#!/usr/bin/env python

import argparse

def makeArgs():
    parser = argparse.ArgumentParser(
        description="This script compares two files with SVs")
    parser.add_argument("-found",required=True,
                        help="File containing found SVs")
    parser.add_argument("-known",required=True,
                        help="File containing found SVs")
    parser.add_argument("-out_missing",required=True,
                    help="Output file to place missing SVs")
    parser.add_argument("-out_found",required=True,
                        help="Output file to place found SVs")
    return parser

if __name__ == "__main__":
    arguments=makeArgs()
    arguments=arguments.parse_args()
    found=arguments.found
    known=arguments.known
    outfileM=arguments.out_missing
    outfileF=arguments.out_found

Found=open(found,"r")
Known=open(known,"r")
outfileM=open(outfileM,"w")
outfileF=open(outfileF,"w")

f={}
k={}

def sort_sv_into_dic(File,dictionary):
    for lines in File:
        line=lines.strip()
        line=line.split()
        Sample=line[0]
        Type=line[1]
        Chrm=line[2]
        Pos=line[3]
        if Sample not in dictionary:
            dictionary[Sample]={}
            if Chrm not in dictionary[Sample]:
                dictionary[Sample][Chrm]={}
                if Type not in dictionary[Sample][Chrm]:
                    dictionary[Sample][Chrm][Type]=[]
                    dictionary[Sample][Chrm][Type].append(int(Pos))
                else:
                    dictionary[Sample][Chrm][Type].append(int(Pos))
            else:
                if Type not in dictionary[Sample][Chrm]:
                    dictionary[Sample][Chrm][Type]=[]
                    dictionary[Sample][Chrm][Type].append(int(Pos))
                else:
                    dictionary[Sample][Chrm][Type].append(int(Pos))
        else:
            if Chrm not in dictionary[Sample]:
                dictionary[Sample][Chrm]={}
                if Type not in dictionary[Sample][Chrm]:
                    dictionary[Sample][Chrm][Type]=[]
                    dictionary[Sample][Chrm][Type].append(int(Pos))
                else:
                    dictionary[Sample][Chrm][Type].append(int(Pos))
            else:
                if Type not in dictionary[Sample][Chrm]:
                    dictionary[Sample][Chrm][Type]=[]
                    dictionary[Sample][Chrm][Type].append(int(Pos))
                else:
                    dictionary[Sample][Chrm][Type].append(int(Pos))

sort_sv_into_dic(Found,f)
#sort_sv_into_dic(Known,k)
for lines in Known:
    line=lines.strip("\n")
    line=line.split()
    Sample=line[0]
    Type=line[1]
    Chrm=line[2]
    Pos=line[3]
    if Sample in f.keys():
        if Chrm in f[Sample]:
            if Type in f[Sample][Chrm]:
                if int(Pos) in f[Sample][Chrm][Type]:
                    outfileF.write(Sample+" "+Type+" "+Chrm+" "+Pos+"\n")
                else:
                    outfileM.write(Sample+" "+Type+" "+Chrm+" "+Pos+"\n")
            else:
                outfileM.write(Sample+" "+Type+" "+Chrm+" "+Pos+"\n")
        else:
            outfileM.write(Sample+" "+Type+" "+Chrm+" "+Pos+"\n")
    else:
        outfileM.write(Sample+" "+Type+" "+Chrm+" "+Pos+"\n")


# for key,val in k.items():
#      if key in f:
#          for val in vals:
#              if val not in f[key]:
#                  outfileM.write(key+" "+val+"\n")
#              else:
#                  outfileF.write(key+" "+val+"\n")
#      else:
#          for val in vals:
#              outfileM.write(key+" "+val+"\n")

# for lines in Found:
#     line=lines.strip("\n")
#     line=line.split()
#     if line[0]+":"+line[1] not in f:
#         f[line[0]+":"+line[1]]=[]
#         f[line[0]+":"+line[1]].append(line[2]+":"+line[3])
#     else:
#         f[line[0]+":"+line[1]].append(line[2]+":"+line[3])

# for lines in Known:
#     line=lines.strip("\n")
#     line=line.split()
#     if line[0]+":"+line[1] not in k:
#         k[line[0]+":"+line[1]]=[]
#         k[line[0]+":"+line[1]].append(line[2]+":"+line[3])
#     else:
#         k[line[0]+":"+line[1]].append(line[2]+":"+line[3])
