%if 0%{?rhel} && ! 0%{?epel}
%bcond_with ansible
%else
%bcond_without ansible
%endif

%bcond_with collection_artifact

Name: ansible-collection-microsoft-sql
Url: https://github.com/linux-system-roles/mssql
Summary: The Ansible role to manage Microsoft SQL Server
Version: 0.0.1
Release: 1%{?dist}

#Group: Development/Libraries
License: MIT
%global installbase %{_datadir}/microsoft
%global _pkglicensedir %{_licensedir}/%{name}

%global collection_namespace microsoft
%global collection_name sql

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
# We don't have ansible-galaxy.
# Simply copy everything instead of galaxy-installing the built artifact.
%define ansible_collection_build_install() tar -cf %{_tmppath}/%{collection_namespace}-%{collection_name}-%{version}.tar.gz .; mkdir -p %{buildroot}%{ansible_collection_files}/%{collection_name}; (cd %{buildroot}%{ansible_collection_files}/%{collection_name}; tar -xf %{_tmppath}/%{collection_namespace}-%{collection_name}-%{version}.tar.gz)
%else
%define ansible_collection_build_install() ansible-galaxy collection build; ansible-galaxy collection install -n -p %{buildroot}%{_datadir}/ansible/collections %{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

# For each role, call defcommit() and the point to it with SourceN: %{archiveurlN}.
%global archiveext tar.gz
# list of source role names
%global rolenames %nil
# list of assignments that can be used to populate a bash associative array variable
%global rolestodir %nil
# list of target rolenames to copy the roles to
%global target_rolenames %nil
# list of collection rolenames to convert the roles to
%global collection_rolenames %nil

%define getarchivedir() %(p=%{basename:%{S:%{1}}}; echo ${p%%.%{archiveext}})

%global parenturl https://github.com/linux-system-roles/

%define defcommit() %{expand:%%global ref%{1} %{2}
%%global shortcommit%{1} %%(c=%%{ref%{1}}; echo ${c:0:7})
%%global extractdir%{1} %%{expand:%%getarchivedir %{1}}
%%{!?repo%{1}:%%global repo%{1} %%{rolename%{1}}}
%%global archiveurl%{1} %%{?forgeorg%{1}}%%{!?forgeorg%{1}:%%{parenturl}}%%{repo%{1}}/archive/%%{ref%{1}}/%%{repo%{1}}-%%{ref%{1}}.tar.gz
%%global rolenames %%{?rolenames} %%{rolename%{1}}
%%global roletodir%{1} [%{rolename%{1}}]="%{extractdir%{1}}"
%%global rolestodir %%{?rolestodir} %{roletodir%{1}}
%%{!?target_rolename%{1}:%%global target_rolename%{1} %%{rolename%{1}}}
%%global target_rolenames %%{?target_rolenames} [%{rolename%{1}}]="%{target_rolename%{1}}"
%%{!?collection_rolename%{1}:%%global collection_rolename%{1} %%{rolename%{1}}}
%%global collection_rolenames %%{?collection_rolenames} [%{rolename%{1}}]="%{collection_rolename%{1}}"
}

%defcommit 1 adcf38c822225d5964a89489e9c18ecec289d1bf
%global rolename1 mssql
%global target_rolename1 sql-server
%global collection_rolename1 server

%global mainid 17baba973c8c77b32ae65838a98dc4fbaf7b7b3e
Source: %{parenturl}auto-maintenance/archive/%{mainid}/auto-maintenance-%{mainid}.tar.gz
Source1: %{archiveurl1}

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

%if %{undefined __ansible_provides}
Provides: ansible-collection(%{collection_namespace}.%{collection_name}) = %{collection_version}
%endif
# be compatible with the usual Fedora Provides:
Provides: ansible-collection-%{collection_namespace}-%{collection_name} = %{version}-%{release}

%description
The collection containing the Ansible role for Microsoft SQL Server management.

%if %{with collection_artifact}
%package collection-artifact
Summary: Collection artifact to import to Automation Hub / Ansible Galaxy

%description collection-artifact
Collection artifact for %{name}. This package contains %{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

%prep
%setup -q -a1 -n %{getarchivedir 0}

# Declare the array containing names of directories to copy roles to for prep
declare -A ROLESTODIR=(%{rolestodir})
for rolename in %{rolenames}; do
    mv "${ROLESTODIR[${rolename}]}" ${rolename}
done

# Removing symlinks in tests/roles
for rolename in %{rolenames}; do
    if [ -d ${rolename}/tests/roles ]; then
        find ${rolename}/tests/roles -type l -exec rm {} \;
        if [ -d ${rolename}/tests/roles/linux-system-roles.${rolename} ]; then
            rm -r ${rolename}/tests/roles/linux-system-roles.${rolename}
        fi
    fi
done

# transform ambiguous #!/usr/bin/env python shebangs to python3 to stop brp-mangle-shebangs complaining
find -type f -executable -name '*.py' -exec \
     sed -i -r -e '1s@^(#! */usr/bin/env python)(\s|$)@#\13\2@' '{}' +

%build
# Convert README.md to README.html in the source roles
readmes=""
for rolename in %{rolenames}; do
    readmes="${readmes} $rolename/README.md"
done
sh md2html.sh $readmes

mkdir .collections
# Copy README.md for the collection build
cp mssql/.collection/README.md lsr_role2collection/collection_readme.md
# Copy galaxy.yml for the collection build
cp mssql/.collection/galaxy.yml ./
# Ensure the correct entries in galaxy.yml
./galaxy_transform.py "%{collection_namespace}" "%{collection_name}" "%{collection_version}" "The Ansible role that manages Microsoft SQL Server" > galaxy.yml.tmp
mv galaxy.yml.tmp galaxy.yml

# Declare the array containing collection rolenames to convert roles to
declare -A COLLECTION_ROLENAMES=(%{collection_rolenames})

# Convert roles to the collection format
for rolename in %{rolenames}; do
    python3 lsr_role2collection.py --role "$rolename" --src-path "$rolename" \
        --dest-path .collections \
        --readme lsr_role2collection/collection_readme.md \
        --namespace %{collection_namespace} --collection %{collection_name} \
        --new-role "${COLLECTION_ROLENAMES[${rolename}]}"
done

# removing dot files/dirs
rm -r .collections/ansible_collections/%{collection_namespace}/%{collection_name}/.[A-Za-z]*

# Copy galaxy.yml to the collection directory
cp -p galaxy.yml .collections/ansible_collections/%{collection_namespace}/%{collection_name}

%install
mkdir -p $RPM_BUILD_ROOT%{installbase}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

# Declare the array containing target rolenames to copy roles to
declare -A TARGET_ROLENAMES=(%{target_rolenames})

for rolename in %{rolenames}; do
    cp -pR "$rolename" "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}"
done

# Copy README, COPYING, and LICENCE files to the corresponding directories
mkdir -p $RPM_BUILD_ROOT%{_pkglicensedir}
for rolename in %{rolenames}; do
    mkdir -p "$RPM_BUILD_ROOT%{_pkgdocdir}/${TARGET_ROLENAMES[${rolename}]}"
    cp -p "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}/README.md" \
       "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}/README.html" \
       "$RPM_BUILD_ROOT%{_pkgdocdir}/${TARGET_ROLENAMES[${rolename}]}"
    if [ -f "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}/COPYING" ]; then
        cp -p "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}/COPYING" \
           "$RPM_BUILD_ROOT%{_pkglicensedir}/${TARGET_ROLENAMES[${rolename}]}.COPYING"
    fi
    if [ -f "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}/LICENSE" ]; then
        cp -p "$RPM_BUILD_ROOT%{installbase}/${TARGET_ROLENAMES[${rolename}]}/LICENSE" \
           "$RPM_BUILD_ROOT%{_pkglicensedir}/${TARGET_ROLENAMES[${rolename}]}.LICENSE"
    fi
done

# Remove dot files
rm -r $RPM_BUILD_ROOT%{installbase}/*/.[A-Za-z]*

# Remove the molecule directory
rm -r $RPM_BUILD_ROOT%{installbase}/*/molecule

pushd .collections/ansible_collections/%{collection_namespace}/%{collection_name}/
%ansible_collection_build_install
popd

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/collection
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles

# Copy the collection README files to the collection
cp -p %{buildroot}%{ansible_collection_files}/%{collection_name}/README.md \
   $RPM_BUILD_ROOT%{_pkgdocdir}/collection

# Declare the array containing collection rolenames to convert roles to
declare -A COLLECTION_ROLENAMES=(%{collection_rolenames})

for rolename in %{rolenames}; do
  if [ -f "%{buildroot}%{ansible_collection_files}%{collection_name}/roles/${COLLECTION_ROLENAMES[${rolename}]}/README.md" ]; then
    mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles/${COLLECTION_ROLENAMES[${rolename}]}
    cp -p %{buildroot}%{ansible_collection_files}/%{collection_name}/roles/${COLLECTION_ROLENAMES[${rolename}]}/README.md \
        $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles/${COLLECTION_ROLENAMES[${rolename}]}
  fi
done

# converting README.md to README.html for collection in $RPM_BUILD_ROOT%{_pkgdocdir}/collection
readmes="$RPM_BUILD_ROOT%{_pkgdocdir}/collection/README.md"
for rolename in %{rolenames}; do
    readmes="${readmes} $RPM_BUILD_ROOT%{_pkgdocdir}/collection/roles/${COLLECTION_ROLENAMES[${rolename}]}/README.md"
done
sh md2html.sh $readmes

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
%{_pkgdocdir}/collection/roles/*/README.md
%{_pkgdocdir}/collection/roles/*/README.html
%license %{_pkglicensedir}/*

%if %{with collection_artifact}
%files collection-artifact
%{_datadir}/ansible/collections/%{collection_namespace}-%{collection_name}-%{version}.tar.gz
%endif

%changelog
* Thu Jun 3 2021 Sergei Petrosian <spetrosi@redhat.com> - 0.0.1-1
- Initiale release
