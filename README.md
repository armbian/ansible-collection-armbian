[![Galaxy](https://img.shields.io/badge/galaxy-armbian.armbian-blue)](https://galaxy.ansible.com/armbian/armbian)


This collection contains a module for gathering facts on [Armbian](https://www.armbian.com). More Armbian related things may be added in the future.

**Ansible 2.9 and later is required.**

The module parses `/etc/armbian-release` and stores the result in `ansible_facts.armbian`. Here is an example:

```
"ansible_facts": {
    "armbian": {
        "arch": "arm",
        "board": "orangepiplus2e",
        "board_family": "sun8i",
        "board_name": "Orange Pi+ 2E",
        "board_type": "conf",
        "branch": "current",
        "build_repository_commit": "e6fa811d-dirty",
        "build_repository_url": "https://github.com/armbian/build",
        "distribution_codename": "buster",
        "distribution_status": "supported",
        "image_type": "stable",
        "initrd_arch": "arm",
        "kernel_image_type": "Image",
        "linux_family": "sunxi",
        "version": "20.08.1"
    }
}
```

If `/etc/armbian-release` is not available `ansible_facts.armbian` will be an empty dictionary. It is safe to run this on non-Armbian hosts without causing your playbook to fail. See `ansible-doc armbian.armbian.armbian_facts` for more details.

### Installation ###

`ansible-galaxy collection install armbian.armbian`

### Usage ###

This module can either be called explicitly by a task or added to the list of [`FACTS_MODULES`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#facts-modules) that run automatically during the fact gathering stage.

#### Adding to the default Facts Modules ####

Add the module to the configuration: 

```ini
[default]
facts_modules = armbian.armbian.armbian_facts
```

This means that any time fact gathering is run, `armbian_facts` will be run in addition to the default fact gathering. This can be done in a playbook:

```yaml
- hosts: armbian
  gather_facts: yes
``` 

Or ad hoc:

 ```
 ansible all -m armbian.armbian.armbian_facts
 ansible all -m gather_facts
 ```

#### Explicit Task ####

You can call the module at any time using a task. Since this is a facts module, there is no need to register the output. The returned facts will automatically be set for the host. If fact caching is enabled, the gathered facts will be cached.

```
- hosts: armbian
  gather_facts: yes
  
  tasks:
    - name: Gather Armbian facts
      armbian.armbian.armbian_facts
```


### Modules in this Collection ###

- `armbian.armbian.armbian_facts` - Gather facts about Armbian.
