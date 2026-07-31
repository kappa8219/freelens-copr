spec := freelens.spec

.PHONY: srpm
srpm:
	dnf --assumeyes install rpmdevtools
	spectool --target x86_64 --get-files --force $(spec)
	rpmbuild -bs --target x86_64 --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
