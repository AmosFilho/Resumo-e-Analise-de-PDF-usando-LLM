#Code used just for download the model for locally use

from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Qwen/Qwen3-4B",
    local_dir="../qwen-4b",
    revision="main"
)