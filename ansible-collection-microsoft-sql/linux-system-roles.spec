%if 0%{?rhel} && ! 0%{?epel}
%bcond_with ansible
%else
%bcond_without ansible
%endif

%bcond_with collection_artifact

%if 0%{?rhel}
Name: rhel-system-roles
%else
Name: linux-system-roles
%endif
Url: https://github.com/linux-system-roles/
Summary: Set of interfaces for unified system management
Version: 1.1.0
Release: 2%{?dist}

#Group: Development/Libraries
License: GPLv3+ and MIT and BSD
%global installbase %{_datadir}/linux-system-roles
%global _pkglicensedir %{_licensedir}/%{name}
%global rolealtprefix linux-system-roles.
%global roleprefix %{name}.
%global roleinstprefix %{nil}
%global rolealtrelpath ../../linux-system-roles/
%if 0%{?rhel}
%global roleinstprefix %{roleprefix}
%global installbase %{_datadir}/ansible/roles
%global rolealtrelpath %{nil}
%endif

%if 0%{?rhel}
%global collection_namespace redhat
%global collection_name rhel_system_roles
%else
%global collection_namespace fedora
%global collection_name linux_system_roles
%endif
%global subrole_prefix "private_${role}_subrole_"

%global collection_version %{version}

# Helper macros originally from macros.ansible by Igor Raits <ignatenkobrain>
# Not available on RHEL, so we must define those macros locally here without using ansible-galaxy

# Not used (yet). Could be made to point to AH in RHEL - but what about CentOS Stream?
#%%{!?ansible_collection_url:%%define ansible_collection_url() https://galaxy.ansible.com/%%{collection_namespace}/%%{collection_name}}

%{!?ansible_collection_files:%define ansible_collection_files %{_datadir}/ansible/collections/ansible_collections/%{collection_namespace}}

%if %{with ansible}
BuildRequires: ansible >= 2.9.10
%endif

%if %{without ansible}
# Empty command. We don't have ansible-galaxy.
%define ansible_collection_build() tar -cf %{_tmppath}/%{collection_namespace}-%{collection_name}-%{version}.tar.gz .
%else
%define ansible_collection_build() ansible-galaxy collection build
%endif

%if %{without ansible}
# Simply copy everything instead of galaxy-installing the built artifact.
%define ansible_collection_install() mkdir -p %{buildroot}%{ansible_collection_files}/%{collection_name}; (cd %{buildroot}%{ansible_collection_files}/%{collection_name}; tar -xf %{_tmppath}/%{collection_namespace}-%{collection_name}-%{version}.tar.gz)
%else
%define ansible_collection_install() ansible-galaxy collection install -n -p %{buildroot}%{_datadir}/ansible/collections %{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

# For each role, call either defcommit() or deftag(). The other macros
# (%%id and %%shortid) can be then used in the same way in both cases.
# This way  the rest of the spec file des not need to know whether we are
# dealing with a tag or a commit.
%global archiveext tar.gz
# list of role names
%global rolenames %nil
# list of assignments that can be used to populate a bash associative array variable
%global rolestodir %nil
%define getarchivedir() %(p=%{basename:%{S:%{1}}}; echo ${p%%.%{archiveext}})

%define defcommit() %{expand:%%global ref%{1} %{2}
%%global shortcommit%{1} %%(c=%%{ref%{1}}; echo ${c:0:7})
%%global extractdir%{1} %%{expand:%%getarchivedir %{1}}
%%{!?repo%{1}:%%global repo%{1} %%{rolename%{1}}}
%%global archiveurl%{1} %%{?forgeorg%{1}}%%{!?forgeorg%{1}:%%{url}}%%{repo%{1}}/archive/%%{ref%{1}}/%%{repo%{1}}-%%{ref%{1}}.tar.gz
%%global rolenames %%{?rolenames} %%{rolename%{1}}
%%global roletodir%{1} [%{rolename%{1}}]="%{extractdir%{1}}"
%%global rolestodir %%{?rolestodir} %{roletodir%{1}}
}

%define deftag() %{expand:%%global ref%{1} %{2}
%%global extractdir%{1} %%{expand:%%getarchivedir %{1}}
%%{!?repo%{1}:%%global repo%{1} %%{rolename%{1}}}
%%global archiveurl%{1} %%{?forgeorg%{1}}%%{!?forgeorg%{1}:%%{url}}%%{repo%{1}}/archive/%%{ref%{1}}/%%{repo%{1}}-%%{ref%{1}}.tar.gz
%%global rolenames %%{?rolenames} %%{rolename%{1}}
%%global roletodir%{1} [%{rolename%{1}}]="%{extractdir%{1}}"
%%global rolestodir %%{?rolestodir} %%{roletodir%{1}}
}

%defcommit 1 bbf5784849d362cc3443fde8b09da26ea698a8ce
%global rolename1 postfix
#%%deftag 1 0.1

%defcommit 2 557546f922886fc1e73012f2af08ec80fec82fe2
%global rolename2 selinux
#%%deftag 2 1.1.1

%defcommit 3 8a95989e158519ce4bebe10091c47ef88b29261b
%global rolename3 timesync
#%%deftag 3 1.0.0

%defcommit 4 77596fdd976c6160d6152c200a5432c609725a14
%global rolename4 kdump
#%%deftag 4 1.0.0

%defcommit 5 0f5a882bcab58baba527015b7cde01c7c52d2254
%global rolename5 network
#%%deftag 5 1.0.0

%defcommit 6 2c3eeb8b2dd898d8c589a0740c2ba9b707e4ed2c
%global rolename6 storage
#%%deftag 6 1.2.2

%defcommit 7 c9b2ee085ccc741b5a9fa8a4b2a7a2f8c8551579
%global rolename7 metrics
#%%deftag 7 0.1.0

%defcommit 8 103d3996436c98dccf89e645378e76bd9add2abb
%global rolename8 tlog
#%%deftag 8 1.1.0

%defcommit 9 a8ab76f8076078763dacacf3384315c86b342d52
%global rolename9 kernel_settings
#%%deftag 9 1.0.1

%defcommit 10 07e08107e7ccba5822f8a7aaec1a2ff0a221bede
%global rolename10 logging
#%%deftag 10 0.2.0

%defcommit 11 4dfc5e2aca74cb82f2a50eec7e975a2b78ad9678
%global rolename11 nbde_server
#%%deftag 11 1.0.1

%defcommit 12 19f06159582550c8463f7d8492669e26fbdf760b
%global rolename12 nbde_client
#%%deftag 12 1.0.1

%defcommit 13 23f1a414ab022a506614c5be8eadf1708dc45b2b
%global rolename13 certificate
#%%deftag 13 1.0.1

%defcommit 14 ff335b87017954c0b47bfe818700e0f1600b04db
%global rolename14 crypto_policies

%global forgeorg15 https://github.com/willshersystems/
%global repo15 ansible-sshd
%global rolename15 sshd
%defcommit 15 428d390668077f0baf5e88c5834ee810ae11113c

%defcommit 16 54bec0855966cc3eed65b26a7c90962eb103d66d
%global rolename16 ssh

%defcommit 17 d97f48a21002497e1ac1bd1385841f2939d7b840
%global rolename17 ha_cluster

%defcommit 18 73e8f5e3b514a8e7a3637dc204d5c106adddeea7
%global rolename18 vpn

%global mainid 17baba973c8c77b32ae65838a98dc4fbaf7b7b3e
Source: %{url}auto-maintenance/archive/%{mainid}/auto-maintenance-%{mainid}.tar.gz
Source1: %{archiveurl1}
Source2: %{archiveurl2}
Source3: %{archiveurl3}
Source4: %{archiveurl4}
Source5: %{archiveurl5}
Source6: %{archiveurl6}
Source7: %{archiveurl7}
Source8: %{archiveurl8}
Source9: %{archiveurl9}
Source10: %{archiveurl10}
Source11: %{archiveurl11}
Source12: %{archiveurl12}
Source13: %{archiveurl13}
Source14: %{archiveurl14}
Source15: %{archiveurl15}
Source16: %{archiveurl16}
Source17: %{archiveurl17}
Source18: %{archiveurl18}

# Script to convert the collection README to Automation Hub.
# Not used on Fedora.
Source998: collection_readme.sh

Patch21: selinux-tier1-tags.diff

Patch31: timesync-tier1-tags.diff

Patch41: rhel-system-roles-kdump-pr22.diff
Patch42: kdump-tier1-tags.diff
Patch43: kdump-meta-el8.diff
Patch44: kdump-fix-newline.diff

Patch51: network-epel-minimal.diff
# Not suitable for upstream, since the files need to be executable there
Patch52: network-tier1-tags.diff
Patch53: network-disable-bondtests.diff
Patch54: network-ansible-test.diff

Patch61: storage-ansible-test.diff

BuildArch: noarch

# Requirements for md2html.sh to build the documentation
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires: rubygem-kramdown-parser-gfm
%else
BuildRequires: pandoc
BuildRequires: asciidoc
BuildRequires: highlight
%endif

# Requirements for galaxy_transform.py
BuildRequires: python3
BuildRequires: python3-six
BuildRequires: python3dist(ruamel.yaml)

Requires: python3-jmespath
Requires: python3-netaddr

Obsoletes: rhel-system-roles-techpreview < 1.0-3

%if %{undefined __ansible_provides}
Provides: ansible-collection(%{collection_namespace}.%{collection_name}) = %{collection_version}
%endif
# be compatible with the usual Fedora Provides:
Provides: ansible-collection-%{collection_namespace}-%{collection_name} = %{version}-%{release}

# We need to put %%description within the if block to avoid empty
# lines showing up.
%if 0%{?rhel}
%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Red Hat Enterprise Linux.
%else
%description
Collection of Ansible roles and modules that provide a stable and
consistent configuration interface for managing multiple versions
of Fedora, Red Hat Enterprise Linux & CentOS.
%endif

%if %{with collection_artifact}
%package collection-artifact
Summary: Collection artifact to import to Automation Hub / Ansible Galaxy

%description collection-artifact
Collection artifact for %{name}. This package contains %{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

%prep
%setup -q -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -a18 -n %{getarchivedir 0}

declare -A ROLESTODIR=(%{rolestodir})
for rolename in %{rolenames}; do
    mv "${ROLESTODIR[${rolename}]}" ${rolename}
done

cd %{rolename2}
%patch21 -p1
cd ..
cd %{rolename3}
%patch31 -p1
cd ..
cd %{rolename4}
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
cd ..
cd %{rolename5}
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
cd ..
cd %{rolename6}
%patch61 -p1
cd ..
cd %{rolename15}
sed -r -i -e "s/ansible-sshd/linux-system-roles.sshd/" tests/*.yml examples/*.yml
sed -r -i  -e "s/ willshersystems.sshd/ linux-system-roles.sshd/" tests/*.yml examples/*.yml README.md
cd ..

# Replacing "linux-system-roles.rolename" with "rhel-system-roles.rolename" in each role
%if "%{roleprefix}" != "linux-system-roles."
for rolename in %{rolenames}; do
    find $rolename -type f -exec \
         sed "s/linux-system-roles[.]${rolename}\\>/%{roleprefix}${rolename}/g" -i {} \;
done
%endif

# Removing symlinks in tests/roles
for rolename in %{rolenames}; do
    if [ -d ${rolename}/tests/roles ]; then
        find ${rolename}/tests/roles -type l -exec rm {} \;
        if [ -d ${rolename}/tests/roles/linux-system-roles.${rolename} ]; then
            rm -r ${rolename}/tests/roles/linux-system-roles.${rolename}
        fi
    fi
done
rm %{rolename5}/tests/modules
rm %{rolename5}/tests/module_utils
rm %{rolename5}/tests/playbooks/roles

# transform ambiguous #!/usr/bin/env python shebangs to python3 to stop brp-mangle-shebangs complaining
find -type f -executable -name '*.py' -exec \
     sed -i -r -e '1s@^(#! */usr/bin/env python)(\s|$)@#\13\2@' '{}' +

%build
readmes=""
for role in %{rolenames}; do
    readmes="${readmes} $role/README.md"
done
sh md2html.sh $readmes

mkdir .collections
%if 0%{?rhel}
# Convert the upstream collection readme to the downstream one
%{SOURCE998} lsr_role2collection/collection_readme.md
%endif
./galaxy_transform.py "%{collection_namespace}" "%{collection_name}" "%{collection_version}" "Red Hat Enterprise Linux System Roles Ansible Collection" > galaxy.yml.tmp
mv galaxy.yml.tmp galaxy.yml

for role in %{rolenames}; do
    python3 lsr_role2collection.py --role "$role" --src-path "$role" \
        --src-owner %{name} --subrole-prefix %{subrole_prefix} --dest-path .collections \
        --readme lsr_role2collection/collection_readme.md \
        --namespace %{collection_namespace} --collection %{collection_name}
done

# copy requirements.txt and bindep.txt from auto-maintenance/lsr_role2collection
if [ -f lsr_role2collection/collection_requirements.txt ]; then
    cp lsr_role2collection/collection_requirements.txt \
       .collections/ansible_collections/%{collection_namespace}/%{collection_name}/requirements.txt
fi
if [ -f lsr_role2collection/collection_bindep.txt ]; then
    cp lsr_role2collection/collection_bindep.txt \
       .collections/ansible_collections/%{collection_namespace}/%{collection_name}/bindep.txt
fi

rm -f .collections/ansible_collections/%{collection_namespace}/%{collection_name}/tests/sanity/ignore-2.9.txt
# Merge .sanity-ansible-ignore-2.9-ROLENAME.txt into tests/sanity/ignore-2.9.txt
mkdir -p .collections/ansible_collections/%{collection_namespace}/%{collection_name}/tests/sanity
for role in %{rolenames}; do
    if [ -f .collections/ansible_collections/%{collection_namespace}/%{collection_name}/.sanity-ansible-ignore-2.9-"$role".txt ];
    then
      cat .collections/ansible_collections/%{collection_namespace}/%{collection_name}/.sanity-ansible-ignore-2.9-"$role".txt \
        >> .collections/ansible_collections/%{collection_namespace}/%{collection_name}/tests/sanity/ignore-2.9.txt
      rm -f .collections/ansible_collections/%{collection_namespace}/%{collection_name}/.sanity-ansible-ignore-*-"$role".txt
    fi
done

# removing dot files/dirs
rm -r .collections/ansible_collections/%{collection_namespace}/%{collection_name}/.[A-Za-z]*

cp -p galaxy.yml lsr_role2collection/.ansible-lint \
    .collections/ansible_collections/%{collection_namespace}/%{collection_name}

# converting README.md to README.html for collection
readmes=".collections/ansible_collections/%{collection_namespace}/%{collection_name}/README.md"
for role in %{rolenames}; do
    readmes="${readmes} .collections/ansible_collections/%{collection_namespace}/%{collection_name}/roles/$role/README.md"
done
sh md2html.sh $readmes

pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_build
popd

%install
mkdir -p $RPM_BUILD_ROOT%{installbase}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

for role in %{rolenames}; do
    cp -pR "$role" "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role"
done

%if 0%{?rolealtprefix:1}
for role in %{rolenames}; do
    ln -s    "%{rolealtrelpath}%{roleinstprefix}$role"   "$RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{rolealtprefix}$role"
done
%endif

mkdir -p $RPM_BUILD_ROOT%{_pkglicensedir}
rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}network/examples/roles
for role in %{rolenames}; do
    mkdir -p "$RPM_BUILD_ROOT%{_pkgdocdir}/$role"
    cp -p "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/README.md" \
       "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/README.html" \
       "$RPM_BUILD_ROOT%{_pkgdocdir}/$role"
    if [ -f "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/COPYING" ]; then
        cp -p "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/COPYING" \
           "$RPM_BUILD_ROOT%{_pkglicensedir}/$role.COPYING"
    fi
    if [ -f "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/LICENSE" ]; then
        cp -p "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/LICENSE" \
           "$RPM_BUILD_ROOT%{_pkglicensedir}/$role.LICENSE"
    fi
    if [ -d "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/examples" ]; then
        for file in "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/examples/"*.yml ; do
            basename=$(basename "$file" .yml)
            newname="$basename"
            if [[ "$newname" != example-* ]]; then
                newname="example-$newname"
            fi
            if [[ "$newname" != *-playbook ]]; then
                newname="${newname}-playbook"
            fi
            cp "$file" "$RPM_BUILD_ROOT%{_pkgdocdir}/$role/${newname}.yml"
            rm "$file"
        done
        if [ -f "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/examples/inventory" ]; then
            cp "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/examples/inventory" \
               "$RPM_BUILD_ROOT%{_pkgdocdir}/$role/example-inventory"
            rm "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/examples/inventory"
        fi
        # special case for network
        # this will error if the directory is unexpectedly empty
        rmdir "$RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}$role/examples"
    fi
done

rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/semaphore
rm -r $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/molecule

rm -r $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/.[A-Za-z]*
rm $RPM_BUILD_ROOT%{installbase}/%{roleinstprefix}*/tests/.git*

# NOTE: sshd/examples/example-root-login.yml is
# referenced in the configuring-openssh-servers-using-the-sshd-system-role documentation module
# must be updated if changing the file path

pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_install
popd

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/collection
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles

cp -p %{buildroot}%{ansible_collection_files}/%{collection_name}/README.md \
   %{buildroot}%{ansible_collection_files}/%{collection_name}/README.html \
   $RPM_BUILD_ROOT%{_pkgdocdir}/collection
# no html files in collection directory
rm -f %{buildroot}%{ansible_collection_files}/%{collection_name}/README.html

for rolename in %{rolenames}; do
  if [ -f %{buildroot}%{ansible_collection_files}/%{collection_name}/roles/${rolename}/README.md ]; then
    mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles/${rolename}
    cp -p %{buildroot}%{ansible_collection_files}/%{collection_name}/roles/${rolename}/README.md \
        %{buildroot}%{ansible_collection_files}/%{collection_name}/roles/${rolename}/README.html \
        $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles/${rolename}
    # no html files in collection directory
    rm -f %{buildroot}%{ansible_collection_files}/%{collection_name}/roles/${rolename}/README.html
  fi
done

%if %{with collection_artifact}
# Copy collection artifact to /usr/share/ansible/collections/ for collection-artifact
pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
if [ -f %{collection_namespace}-%{collection_name}-%{version}.tar.gz ]; then
    mv %{collection_namespace}-%{collection_name}-%{version}.tar.gz \
       $RPM_BUILD_ROOT%{_datadir}/ansible/collections/
fi
popd
%endif

# generate the %files section in the file files_section.txt
format_item_for_files() {
    # $1 is directory or file name in buildroot
    # $2 - if true, and item is a directory, use %dir
    local item
    local files_item
    item="$1"
    files_item=${item##"%{buildroot}"}
    if [ -L "$item" ]; then
        echo "$files_item"
    elif [ -d "$item" ]; then
        if [[ "$item" == */doc* ]]; then
            echo "%doc $files_item"
        elif [ "${2:-false}" = true ]; then
            echo "%dir $files_item"
        else
            echo "$files_item"
        fi
    elif [[ "$item" == */README.md ]] || [[ "$item" == */README.html ]]; then
        if [[ "$item" == */private_* ]]; then
            # mark as regular file, not %doc
            echo "$files_item"
        else
            echo "%doc $files_item"
        fi
    elif [[ "$item" == */COPYING* ]] || [[ "$item" == */LICENSE* ]]; then
        echo "%%license $files_item"
    else
        echo "$files_item"
    fi
}

files_section=files_section.txt
rm -f $files_section
touch $files_section
%if %{without ansible}
echo '%dir %{_datadir}/ansible' >> $files_section
echo '%dir %{_datadir}/ansible/roles' >> $files_section
%endif
%if "%{installbase}" != "%{_datadir}/ansible/roles"
echo '%dir %{installbase}' >> $files_section
%endif
echo '%dir %{ansible_collection_files}' >> $files_section
echo '%dir %{ansible_collection_files}/%{collection_name}' >> $files_section
find %{buildroot}%{ansible_collection_files}/%{collection_name} -mindepth 1 -maxdepth 1 | \
    while read item; do
        if [[ "$item" == */roles ]]; then
            format_item_for_files "$item" true >> $files_section
            find "$item" -mindepth 1 -maxdepth 1 | while read roles_dir; do
                format_item_for_files "$roles_dir" true >> $files_section
                find "$roles_dir" -mindepth 1 -maxdepth 1 | while read roles_item; do
                    format_item_for_files "$roles_item" >> $files_section
                done
            done
        else
            format_item_for_files "$item" >> $files_section
        fi
    done

find %{buildroot}%{installbase} -mindepth 1 -maxdepth 1 | \
    while read item; do
        if [ -d "$item" ]; then
            format_item_for_files "$item" true >> $files_section
            find "$item" -mindepth 1 -maxdepth 1 | while read roles_item; do
                format_item_for_files "$roles_item" >> $files_section
            done
        else
            format_item_for_files "$item" >> $files_section
        fi
    done
if [ "%{installbase}" != "%{_datadir}/ansible/roles" ]; then
    find %{buildroot}%{_datadir}/ansible/roles -mindepth 1 -maxdepth 1 | \
        while read item; do
            if [ -d "$item" ]; then
                format_item_for_files "$item" true >> $files_section
                find "$item" -mindepth 1 -maxdepth 1 | while read roles_item; do
                    format_item_for_files "$roles_item" >> $files_section
                done
            else
                format_item_for_files "$item" >> $files_section
            fi
        done
fi
# cat files_section.txt
# done with files_section.txt generation


%files -f files_section.txt
%{_pkgdocdir}/*/README.md
%{_pkgdocdir}/*/README.html
%{_pkgdocdir}/*/example-*
%{_pkgdocdir}/collection/roles/*/README.md
%{_pkgdocdir}/collection/roles/*/README.html
%license %{_pkglicensedir}/*

%if %{with collection_artifact}
%files collection-artifact
%{_datadir}/ansible/collections/%{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

%changelog
* Mon May 10 2021 Sergei Petrosian <spetrosi@redhat.com> - 1.1.0-2
- Add BuildRequires: rubygem-kramdown for Fedora and RHEL >= 9

* Wed Apr 14 2021 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1
- rebase timesync role to latest upstream
  Resolves rhbz#1937938
- timesync - add timesync_chrony_custom_settings variable for free-form
  local configs
  Resolves rhbz#1938023
- do not use ignore_errors in timesync role
  Resolves rhbz#1938014
- support for timesync_max_distance to configure maxdistance/maxdist parameter
  Resolves rhbz#1938016
- support for ntp xleave, filter, and hw timestamping
  Resolves rhbz#1938020
- rebase selinux role to latest upstream
  Resolves rhbz#1937938
- should not reload the SELinux policy if its not changed
  Resolves rhbz#1757869
- Ability to install custom SELinux module via Ansible
  Resolves rhbz#1848683
- rebase storage role to latest upstream
  Resolves rhbz#1937938
- rebase network role to latest upstream
  Resolves rhbz#1937938
- support for ipv6_disabled to disable ipv6 for address
  Resolves rhbz#1939711
- rebase postfix role to latest upstream
  Resolves rhbz#1937938
- rebase metrics role to latest upstream
  Resolves rhbz#1937938
- rebase sshd role to latest upstream
  Resolves rhbz#1937938
- rebase remaining roles to latest upstream
  Resolves rhbz#1937938
- Generate %%files dynamically
- add vpn role
  Resolves rhbz#1943679

* Tue Apr 13 2021 Noriko Hosoi <nhosoi@redhat.com> - 1.0.1-2
- Adding the -collection-artifact subpackage, enabled using
  "--with collection_artifact". It is used for importing to
  ansible galaxy/automation hub.
- README.html files (main README for the collection and README
  for each role) are not located in /usr/share/ansible/collections,
  but just put in /usr/share/doc/linux-system-roles/collection in rpm.
- The README.html files are not included in the collection artifact.
- Fixing "sshd role README.md examples use incorrect role name".

* Tue Apr  6 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.1-1
- Sync with RHEL version 1.0.1-1.el8
  Fix description field in galaxy.yml
  Remove "Technology Preview" from Collection README
  Merging individual ignore file and add it to the package
  Add a note to each module Doc to indicate it is private
  Add patches for network and storage role ansible-test fixes
  Simplify doc tags in %%files, corrects a forgotten doc tag for ha_cluster
  Suppress one ansible-lint warning in ha_cluster
  Add patch for the inclusive language leftover on network-role README.md

* Mon Feb 22 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-16
- Sync with RHEL version 1.0.0-31
  Rebase certificate role to pick up a test fix
  Rebase logging role to fix default private key path,
  upstream PR #218
  Update collection doc transformation to match a modified text
  and include the Tech Preview note again (for RHEL)

* Fri Feb 19 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-15
- Sync with RHEL version 1.0.0-29
  Added roles: ssh, ha_cluster
  Updated roles: certificate, kernel_settings, nbde_client,
  logging, network
  Improvements to collection build and metadata
- Two further improvements from RHEL:
  Corrected merge botch in files list - make ssh README a docfile
  Dynamically update galaxy.yml with our metadata even on Fedora,
  we can't rely on correct version number in auto-maintenance

* Tue Feb  9 2021 Pavel Cahyna <pcahyna@redhat.com> - 1.0.0-14
- Synchronize with RHEL, new roles added:
  storage, metrics, tlog, kernel_settings, logging, nbde_server,
  nbde_client, certificate, crypto_policies, sshd, and the
  fedora.linux_system_roles collection.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Till Maas <opensource@till.name> - 1.0-8
- Install roles at /usr/share/linux-system-roles, use symlinks in
  /usr/share/ansible/roles/ to allow using alternatives

* Wed Nov 14 2018 Mike DePaulo <mikedep333@gmail.com> - 1.0-7
- spec file improvement: Remove unnecessary %%doc for files under _pkgdocdor
- Install license files under /usr/share/licenses instead of /usr/share/doc

* Tue Nov 06 2018 Mike DePaulo <mikedep333@gmail.com> - 1.0-7
- Fix rpm build for added example timesync example playbooks
- Misc spec file comments fixes
- Fix rpmlint error by escaping a previous changelog entry with a macro
- Comply with Fedora guidelines by always using "cp -p" in %%install
- Update %%description to be different for Fedora.

* Wed Oct 24 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-7
- Update to latest versions of selinux, kdump and timesync.
- Update to the latest revision of postfix, fixes README markup
- Add Obsoletes for the -techpreview subpackage introduced mistakenly in 1.0-1
- spec file improvement: Unify the source macros with deftag() and defcommit()

* Tue Oct 23 2018 Till Maas <opensource@till.name> - 1.0-6
- Update Network system role to latest commit to include Fedora 29 fixes
- Update example timesync example playbooks
- Add comments about upstream status

* Tue Aug 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-4
- Format the READMEs as html, by vdolezal, with changes to use highlight
  (source-highlight does not understand YAML)

* Thu Aug  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 1.0-3
- Rebase the network role to the last revision (d866422).
  Many improvements to tests, introduces autodetection of the current provider
  and defaults to using profile name as interface name.
- Rebase the selinux, timesync and kdump roles to their 1.0rc1 versions.
  Many changes to the role interfaces to make them more consistent
  and conforming to Ansible best practices.
- Update the description.

* Fri May 11 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-4
- Fix complaints about /usr/bin/python during RPM build by making the affected scripts non-exec
- Fix merge botch

* Mon Mar 19 2018 Troy Dawson <tdawson@redhat.com> - 0.6-3.1
- Use -a (after cd) instead of -b (before cd) in %%setup

* Wed Mar 14 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-3
- Minor corrections of the previous change by Till Maas.

* Fri Mar  9 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-2
- Document network role options: static routes, ethernet, dns
  Upstream PR#36, bz1550128, documents bz1487747 and bz1478576

* Tue Jan 30 2018 Pavel Cahyna <pcahyna@redhat.com> - 0.6-1
- Drop hard dependency on ansible (#1525655), patch from Yaakov Selkowitz
- Update the network role to version 0.4, solves bz#1487747, bz#1478576

* Tue Dec 19 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-3
- kdump: fix the wrong conditional for ssh checking and improve test (PR#10)

* Tue Nov 07 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-2
- kdump: add ssh support. upstream PR#9, rhbz1478707

* Tue Oct 03 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.5-1
- SELinux: fix policy reload when SELinux is disabled on CentOS/RHEL 6
  (bz#1493574)
- network: update to b856c7481bf5274d419f71fb62029ea0044b3ec1 :
  makes the network role idempotent (bz#1476053) and fixes manual
  network provider selection (bz#1485074).

* Mon Aug 28 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.4-1
- network: update to b9b6f0a7969e400d8d6ba0ac97f69593aa1e8fa5:
  ensure that state:absent followed by state:up works (bz#1478910), and change
  the example IP adresses to the IANA-assigned ones.
- SELinux: fix the case when SELinux is disabled (bz#1479546).

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-2
- We can't change directories to symlinks (rpm bug #447156) so keep the old
  names and create the new names as symlinks.

* Tue Aug 8 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.3-1
- Change the prefix to linux-system-roles., keeping compatibility
  symlinks.
- Update the network role to dace7654feb7b5629ded0734c598e087c2713265:
  adds InfiniBand support and other fixes.
- Drop a patch included upstream.

* Mon Jun 26 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-2
- Leave a copy of README and COPYING in every role's directory, as suggested by T. Bowling.
- Move the network example inventory to the documentation directory together.
  with the example playbooks and delete the now empty "examples" directory.
- Use proper reserved (by RFC 7042) MAC addresses in the network examples.

* Tue Jun 6 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.2-1
- Update the networking role to version 0.2 (#1459203)
- Version every role and the package separately. They live in separate repos
  and upstream release tags are not coordinated.

* Mon May 22 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-2
- Prefix the roles in examples and documentation with rhel-system-roles.

* Thu May 18 2017 Pavel Cahyna <pcahyna@redhat.com> - 0.1-1
- Update to 0.1 (first upstream release).
- Remove the tuned role, it is not ready yet.
- Move the example playbooks to /usr/share/doc/rhel-system-roles/$SUBSYSTEM
  directly to get rid of an extra directory.
- Depend on ansible.

* Thu May 4 2017  Pavel Cahyna <pcahyna@redhat.com> - 0-0.1.20170504
- Initial release.
- kdump r. fe8bb81966b60fa8979f3816a12b0c7120d71140
- postfix r. 43eec5668425d295dce3801216c19b1916df1f9b
- selinux r. 1e4a21f929455e5e76dda0b12867abaa63795ae7
- timesync r. 33a1a8c349de10d6281ed83d4c791e9177d7a141
- tuned r. 2e8bb068b9815bc84287e9b6dc6177295ffdf38b
- network r. 03ff040df78a14409a0d89eba1235b8f3e50a750

