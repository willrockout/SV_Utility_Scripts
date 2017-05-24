#!/usr/bin/env python

import argparse
import os
import re
import gzip

def makeArgs():
    parser = argparse.ArgumentParser(
        description="Search vcf for overlapping insertions off by a single base")
    parser.add_argument("-sample_direc", required=True,
                        help="Directory containing sample vcfs")
    parser.add_argument("-parent_direc", required=True,
                        help="Directory containing parent vcfs")
    parser.add_argument("-output_direc", required=True,
                        help="Output directory to write new vcfs")
    return parser
if __name__ == "__main__":
    arguments=makeArgs()
    arguments=arguments.parse_args()
    Samples=arguments.sample_direc
    Parents=arguments.parent_direc
    Output=arguments.output_direc

PDict={}

for sample in os.listdir(Samples):
    for subdirs,dirs,files in os.walk(Parents):
        for parent in files:
            if re.search("Overlap_out*",sample):
                if "variants.vcf.gz" == parent:
                    sampleID = sample[12:-4]
                    SInPath=Samples+sample
                    PInPath=subdirs+"/"+parent
                    Outpath=Output+sampleID+"_insrm.vcf"
                    Outfile=open(Outpath,"w+")
                    Sfile=open(SInPath,"r")
                    Pfile=gzip.open(PInPath,"r")
                    if Sfile and Pfile:
                        for lines in Pfile:
                            line=lines.strip("\n")
                            if line[0] != "#":
                                line=line.split()
                                if line[4] == "<INS>":
                                    Chrom=line[0]
                                    Pos=line[1]
                                    if int(Pos) not in PDict:
                                        PDict[int(Pos)]=Chrom
                                    else:
                                        continue
                    Pfile.close()
                    for lines in Sfile:
                        line=lines.strip("/n")
                        if line[0] == "#":
                            Outfile.write(lines)
                        else:
                            line=line.split()
                            Chrom=line[0]
                            Pos=line[1]
                            if line[4] =="<INS>":
                                Match=False
                                for i in  range(int(Pos)-1,int(Pos)+2):
                                    if i in PDict and PDict[i] == Chrom:
                                        Match=True
                                if not Match:
                                    Outfile.write(lines)
                            else:
                                Outfile.write(lines)
                                        

