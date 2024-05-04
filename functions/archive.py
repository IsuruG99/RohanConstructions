import database
from utils import *

def load_all_archives(status: int = 0) -> list:
    ref = database.get_ref('archive')
    archives = []
    for archive_id, archive in ref.get().items():
        if archive_id == 'arZero':
            continue
        archive['id'] = archive_id
        archives.append(archive)
    if status == 0:
        archives = archives
    return archives


def get_archive(archive_id: str) -> dict:
    ref = database.get_ref('archive')
    archive = ref.child(archive_id).get()
    return archive


