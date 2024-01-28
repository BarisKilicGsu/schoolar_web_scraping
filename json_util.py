import json

def read_json_in_chunks(file_path, chunk_size):
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield json.loads(chunk)

            