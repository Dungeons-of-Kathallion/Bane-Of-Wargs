import logger_sys
import uuid


# Handling functions
def generate_random_uuid():
    logger_sys.log_message("INFO: Generating new random UUID using 'uuid.4' method")
    random_uuid = uuid.uuid4()
    random_uuid = str(random_uuid)
    random_uuid = random_uuid.replace('UUID', '')
    random_uuid = random_uuid.replace('(', '')
    random_uuid = random_uuid.replace(')', '')
    random_uuid = random_uuid.replace("'", '')
    logger_sys.log_message(f"INFO: Generated new random UUID: '{random_uuid}'")
    return random_uuid
