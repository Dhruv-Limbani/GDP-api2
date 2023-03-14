from sentence_transformers import cached_download

print(cached_download("https://huggingface.co/sentence-transformers/stsb-roberta-large/resolve/main/pytorch_model.bin").cache_files[0].cache_directory)