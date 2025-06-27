from sklearn.metrics.pairwise import cosine_similarity
from BERTMode import get_embedding_verbose
import ast
import numpy as np
import pandas as pd


# Membaca dataset yang sudah dihitung nilai mebeding deskripsi silabusnya
dataset_path = "data_embding.xlsx"
dataset = pd.read_excel(dataset_path)


def conversionData(text_silabus, judul_silabus):
    df_konversi = pd.DataFrame(
        columns=["subject", "sks", "semester", "similarity_score"]
    )
    embedding_silabus = get_embedding_verbose(text_silabus)["embedding"]
    for i in range(len(dataset)):

        embedding_target = dataset.at[i, "embedding"]
        if embedding_target is not None:
            embedding_target = np.fromstring(embedding_target.strip("[]"), sep=" ")
            similarity_score = cosine_similarity(
                [embedding_silabus], [embedding_target]
            )[0][0]

            if similarity_score > 0.60:
                df_konversi = pd.concat(
                    [
                        df_konversi,
                        pd.DataFrame(
                            {
                                "subject": [dataset.at[i, "subject"]],
                                "sks": [dataset.at[i, "sks"]],
                                "semester": [dataset.at[i, "semester"]],
                                "similarity_score": [similarity_score],
                                "Mata Kuliah Tujuan": [judul_silabus],
                            }
                        ),
                    ],
                    ignore_index=True,
                )

    # Filter: Ambil hanya subject dengan similarity_score tertinggi
    df_konversi = (
        df_konversi.loc[df_konversi.groupby("subject")["similarity_score"].idxmax()]
        .sort_values(by="similarity_score", ascending=False)
        .reset_index(drop=True)
    )

    return df_konversi
