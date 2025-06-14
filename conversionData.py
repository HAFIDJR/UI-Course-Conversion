from sklearn.metrics.pairwise import cosine_similarity
from BERTMode import get_embedding_verbose
import ast
import numpy as np
import pandas as pd


# Membaca dataset yang sudah dihitung nilai mebeding deskripsi silabusnya
dataset_path = "data_embding.xlsx"
dataset = pd.read_excel(dataset_path)


def conversionData(text_silabus):
    df_konversi = pd.DataFrame(columns=["subject", "sks", "similarity_score"])
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
                                "similarity_score": [similarity_score],
                            }
                        ),
                    ],
                    ignore_index=True,
                )

    return df_konversi.sort_values(by="similarity_score", ascending=False)
