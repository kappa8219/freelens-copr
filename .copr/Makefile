spec := freelens.spec
source_url := https://github.com/freelensapp/freelens/releases/download/v1.10.3/Freelens-1.10.3-linux-amd64.rpm

.PHONY: srpm
srpm:
	curl --fail --location --output Freelens-1.10.3-linux-amd64.rpm $(source_url)
	rpmbuild -bs --target x86_64 --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
