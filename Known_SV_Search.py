#!/usr/bin/env python

import argparse
import os

def makeArgs():
    parser = argparse.ArgumentParser(
        description="This script searches vcf files for known SVs from provided txt file")
    parser.add_argument("--knownSVfile",required=True,
                        help="File containing known SVs in 4 columns(Sample,Type,Chrm,Pos)")
    parser.add_argument("--vcf_direc",required=True,
                        help="Directory containing vcfs to search")
    parser.add_argument("--output",required=True,
                        help="Output file to write found SVs")
    return parser
if __name__ == "__main__":
    arguments=makeArgs()
    arguments=arguments.parse_args()
    knownSV=arguments.knownSVfile
    vcfs=arguments.vcf_direc
    out=arguments.output

kSV=open(knownSV,"r")
outfile=open(out,"w+")
SVs={}
for lines in kSV:
    line=lines.strip()
    line=line.split()
    Sample=line[0]
    Type=line[1]
    Chrm=line[2]
    Pos=line[3]
    if Sample not in SVs:
        SVs[Sample]={}
        if Chrm not in SVs[Sample]:
            SVs[Sample][Chrm]={}
            if Type not in SVs[Sample][Chrm]:
                SVs[Sample][Chrm][Type]=[]
                SVs[Sample][Chrm][Type].append(Pos)
            else:
                SVs[Sample][Chrm][Type].append(Pos)
        else:
            if Type not in SVs[Sample][Chrm]:
                SVs[Sample][Chrm][Type]=[]
                SVs[Sample][Chrm][Type].append(Pos)
            else:
                SVs[Sample][Chrm][Type].append(Pos)
    else:
        if Chrm not in SVs[Sample]:
            SVs[Sample][Chrm]={}
            if Type not in SVs[Sample][Chrm]:
                SVs[Sample][Chrm][Type]=[]
                SVs[Sample][Chrm][Type].append(Pos)
            else:
                SVs[Sample][Chrm][Type].append(Pos)
        else:
            if Type not in SVs[Sample][Chrm]:
                SVs[Sample][Chrm][Type]=[]
                SVs[Sample][Chrm][Type].append(Pos)
            else:
                SVs[Sample][Chrm][Type].append(Pos)
kSV.close()

for key in SVs:
    filepath=vcfs+key+"_insrm.vcf"
    vcf=open(filepath,"r")
    for lines in vcf:
        if lines[0] != "#":
            line=lines.strip("\n")
            line=line.split()
            Chrm=line[0]
            Pos=line[1]
            Type=line[4][1:-1]
            if Chrm in SVs[key]:
                if Type in SVs[key][Chrm]:
                    for i in range(int(Pos)-150,int(Pos)+151):
                        if str(i) in SVs[key][Chrm][Type]:
                            outfile.write(key+" "+Type+" "+Chrm+" "+str(i)+"\n")
                            SVs[key][Chrm][Type].remove(str(i))
