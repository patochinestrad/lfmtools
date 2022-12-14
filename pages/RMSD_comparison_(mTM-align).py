import streamlit as st
import os
from src import mTMAnalysis, helper_funcs
from tempfile import TemporaryDirectory
import zipfile
import io

st.title("mTM-Align RMSD Analysis")

st.subheader(
    "Upload two or more PDB files to be compared to each other with mTM-Align."
)

files = st.file_uploader("Upload PDB files", type="pdb", accept_multiple_files=True)

if files:
    with TemporaryDirectory() as tempDir:

        # """
        # Save input files to tempDir to work on them
        # """

        for file in files:
            with open(os.path.join(tempDir, file.name), "wb") as f:
                f.write(file.getbuffer())

        if st.button("Run all vs all comparison"):
            with st.spinner("Comparing structures. Please wait."):
                mTMAnalysis.mTMInputFile(tempDir)
                mTMAnalysis.mTMAlignRun(
                    os.path.join(tempDir, "input_file.txt"),
                    os.path.join(tempDir, "res_mtmalign"),
                )

                rmsd_df, TM_df = mTMAnalysis.mTMAlignAnalysis(
                    os.path.join(tempDir, "res_mtmalign")
                )
                st.write("RMSD Matrix")
                st.dataframe(rmsd_df, use_container_width=True)
                st.write("TM Score Matrix")
                st.dataframe(TM_df, use_container_width=True)

        with io.BytesIO() as buffer:

            with zipfile.ZipFile(buffer, mode="w") as archive:
                helper_funcs.zipdir(tempDir, archive)
            buffer.seek(0)
            st.download_button(
                "Download results",
                data=buffer,
                file_name="mtmalign_results.zip",
                mime="application/zip",
            )
