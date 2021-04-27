#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
---
module: Armbian Facts
author:
    - Sam Doran (@samdoran)
version_added: '1.0.0'
short_description: Collect facts about Armbian
notes: []
description:
    - Gather detailed facts about Armbian from C(/etc/armbian-release). If facts are unable to be gathered,
      an empty dictionary is returned. This can be run safelay against non-Armbian hosts.
    - This module can be added to the default list of C(FACTS_MODULES).
    
options: {}
"""

EXAMPLES = """
- armbian_facts:
"""

RETURN = """
armbian:
    description: Main key containing the Armbian facts. Empty if parsing failed.
    returned: always
    type: complex
    contains:
        arch:
          description: Architecture
          returned: success
          type: str
          sample: "arm"
        board:
          description: Board
          returned: success
          type: str
          sample: "helios4"
        board_name:
          description: Board name
          returned: success
          type: str
          sample: "Helios4"
        board_type:
          description: Board type
          returned: success
          type: str
          sample: "conf"
        board_family:
          description: Board family
          returned: success
          type: str
          sample: "mvebu"
        branch:
          description: Branch
          returned: success
          type: str
          sample: "next"
        build_repository_commit:
          description: Build repository
          returned: success
          type: str
          sample: "0d21d90f"
        build_repsitory_url:
          description: Build repository
          returned: success
          type: str
          sample: "https://github.com/armbian/build"
        image_type:
          description: Image type
          returned: success
          type: str
          sample: "user-built"
        initrd_arch:
          description: initrd architecture
          returned: success
          type: str
          sample: "arm"
        kernel_image_type:
          description: Kernel image type
          returned: success
          type: str
          sample: "zImage"
        linux_family:
          description: Linux family
          returned: success
          type: str
          sample: "mvebu"
        version:
          description: Armbian version
          returned: success
          type: str
          sample: "5.91"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.facts.utils import get_file_lines

# Eample of /etc/armbian-release:
#
#     BOARD=helios4
#     BOARD_NAME="Helios4"
#     BOARDFAMILY=mvebu
#     BUILD_REPOSITORY_URL=https://github.com/armbian/build
#     BUILD_REPOSITORY_COMMIT=0d21d90f
#     VERSION=5.91
#     LINUXFAMILY=mvebu
#     BRANCH=next
#     ARCH=arm
#     IMAGE_TYPE=user-built
#     BOARD_TYPE=conf
#     INITRD_ARCH=arm
#     KERNEL_IMAGE_TYPE=zImage


KEY_TRANSFORMATION = {
    'LINUXFAMILY': 'linux_family',
    'BOARDFAMILY': 'board_family',
}


def parse_armbian_release():
    release_file = '/etc/armbian-release'

    lines = get_file_lines(release_file)

    parsed = {}
    for line in lines:
        if line.startswith('#'):
            continue

        try:
            key, value = line.split('=', 1)
        except ValueError:
            continue

        key = KEY_TRANSFORMATION.get(key, key)
        parsed[key.lower()] = value.strip('\'"')

    return parsed


def main():
    module = AnsibleModule(
        argument_spec={
            'fact_path': {'type': 'path'},
        },
        supports_check_mode=True,
    )

    parsed = parse_armbian_release()
    results = {'ansible_facts': {'armbian': parsed}}
    module.exit_json(**results)


if __name__ == '__main__':
    main()
