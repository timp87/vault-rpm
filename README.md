# Vault-RPM
A set of files to build RPM for HashiCorp Vault - a tool for managing secrets https://www.vaultproject.io/

## How to build RPM
1. Install prerequisite software

   ```
   sudo yum install -y rpm-build rpmdevtools
   ```
2. Clone this repository

   ```
   git clone https://github.com/timp87/vault-rpm.git
   ```
3. Copy build dir into home

   ```
   cp -r vault-rpm/rpmbuild ~/
   ```
4. Download distfile and build RPM

   ```
   spectool -g -R ~/rpmbuild/SPECS/vault.spec && \
   rpmbuild -ba ~/rpmbuild/SPECS/vault.spec
   ```

After all you'll find RPM package in ~/rpmbuild/RPMS/x86_64/

Please, note, this was originally made for Centos 7 x86_64.
