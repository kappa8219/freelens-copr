spec := freelens.spec

.PHONY: srpm
srpm:
	dnf --assumeyes install rpmdevtools
	spectool --define "_target_cpu x86_64" --get-files --force $(spec)
	rpmbuild -bs --target x86_64 --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
