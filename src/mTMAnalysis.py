import re
import pandas as pd
import os
import streamlit as st
import subprocess


def mTMInputFile(path):
    res_mtmalign = os.path.join(path, "res_mtmalign")
    try:
        os.mkdir(res_mtmalign)
    except FileExistsError:
        st.warning("Analysis already made for these files.")
    pdblist = [os.path.join(path, i) for i in os.listdir(path) if i.endswith(".pdb")]
    input_file = os.path.join(path, "input_file.txt")
    with open(input_file, "w") as file:
        for i in pdblist:
            file.write(i + "\n")


def mTMAlignRun(input_file, out_path):
    subprocess.call(
        [
            "./src/programs/mTM-align",
            "-i",
            input_file,
            "-outdir",
            out_path,
        ]
    )
    return st.success("Done")


def mTMAlignAnalysis(out_path):
    rmsd_data = []
    rmsd_matrix = out_path + "/pairwise_rmsd.txt"
    with open(rmsd_matrix) as rmsd_matrix:
        lines = rmsd_matrix.readlines()
        lines[0] = "proteins.pdb" + lines[0]
        for i in lines:
            rmsd_data.append(list(filter(None, re.split(".pdb|\s+", i))))
    rmsd_df = pd.DataFrame(data=rmsd_data)
    rmsd_df = rmsd_df.set_index(0)

    TM_data = []
    TM_matrix = out_path + "/pairwise_TMscore.txt"
    with open(TM_matrix) as TM_matrix:
        lines = TM_matrix.readlines()
        lines[0] = "proteins.pdb" + lines[0]
        for i in lines:
            TM_data.append(list(filter(None, re.split(".pdb|\s+", i))))
    TM_df = pd.DataFrame(data=TM_data)
    TM_df = TM_df.set_index(0)

    return rmsd_df, TM_df
