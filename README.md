SQL Ansible Collection
=====================================

The SQL collection contains a role for managing Microsoft SQL Server.

## Currently supported distributions

* Fedora
* Red Hat Enterprise Linux (RHEL 7+)
* RHEL 7+ derivatives such as CentOS 7+

## Installation

There are currently two ways to use the Microsoft SQL Collection in your setup.

### Installation from Ansible Galaxy

You can install the collection from Ansible Galaxy by running:
```
ansible-galaxy collection install microsoft.sql
```

After the installation, the role is available as `microsoft.sql.server`.

Please see the [Using Ansible collections documentation](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for further details.

## Support

### Supported Ansible Versions

The supported Ansible versions are aligned with currently maintained Ansible versions that support Collections (Ansible 2.9 and later). You can find the list of maintained Ansible versions [here](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#release-status).

### Supported Roles

  * server
