PKGNAME := friskola-access
ARCH := all

VERSION := $(shell git tag --points-at HEAD)
ifeq ($(VERSION),)
    VERSION := 0
endif


BRANCH := $(shell git branch | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
UNCOMMITTED := $(shell git status --short | wc --lines)
AHEAD :=  $(shell git status --short --branch | grep $(BRANCH) | grep ahead | wc --lines)
ifneq ($(UNCOMMITTED), 0)
    STATUS := dirty
    VERSION := $(VERSION)+dirty
else ifneq ($(AHEAD), 0)
    STATUS := dirty
    VERSION := $(VERSION)+dirty
else
    VERSION := $(VERSION)+$(shell git log --no-walk --pretty='%h' HEAD)
endif


BUILDDIR := build/$(PKGNAME)_$(VERSION)_$(ARCH)
DEPLOYDIR := prodadmin@sshgateway:/var/www/proddata/www/deb/$(REPO)/$(ARCH)/
DEBFILE := build/$(PKGNAME)_$(VERSION)_$(ARCH).deb


$(DEBFILE):
	mkdir -p $(BUILDDIR)
	rsync -a --delete --delete-excluded --exclude '*~' --exclude '__pycache__' src/ $(BUILDDIR)/
	python3 -m compileall $(BUILDDIR)
	mkdir -p $(BUILDDIR)/DEBIAN
	cat control | sed 's/PKGNAME/$(PKGNAME)/g' \
	            | sed 's/VERSION/$(VERSION)/g' \
	            | sed 's/ARCH/$(ARCH)/g' \
	            > $(BUILDDIR)/DEBIAN/control
	dpkg-deb --build --root-owner-group $(BUILDDIR)


clean:
	rm -rf build tmp
