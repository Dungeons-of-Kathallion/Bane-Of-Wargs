# uuid_handling.py
# Copyright (c) 2024 by @Cromha
#
# Bane Of Wargs is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Bane Of Wargs is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

# source imports
import logger_sys
# external imports
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
