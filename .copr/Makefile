spec := freelens.spec
version := 1.10.3
source := Freelens-$(version)-linux-amd64.rpm
source_url := https://github.com/freelensapp/freelens/releases/download/v$(version)/$(source)

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
