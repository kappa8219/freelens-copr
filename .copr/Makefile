spec := freelens.spec

.PHONY: srpm
srpm:
	dnf --assumeyes install rpmdevtools
	spectool --get-files --force $(spec)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
