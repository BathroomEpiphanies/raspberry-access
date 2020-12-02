PKGNAME := friskola-access
ARCH    := all

VERSION := $(shell git tag --points-at HEAD)
ifeq ($(VERSION),)
    VERSION := 0
endif


UNCOMMITTED := $(shell git status --short | wc --lines)
AHEAD :=  $(shell git status --short --branch | grep master | grep ahead | wc --lines)
ifneq ($(UNCOMMITTED), 0)
    STATUS := dirty
    VERSION := $(VERSION)+dirty
else ifneq ($(AHEAD), 0)
    STATUS := dirty
    VERSION := $(VERSION)+dirty
else
    VERSION := $(VERSION)+$(shell git log --no-walk --pretty="%h" HEAD)
endif


BUILDDIR := "build/$(PKGNAME)_$(VERSION)_$(ARCH)"
DEBFILE := "build/$(PKGNAME)_$(VERSION)_$(ARCH).deb"


package: $(DEBFILE)
$(DEBFILE): src
	mkdir -p "$(BUILDDIR)"
	rsync -a "src/" "$(BUILDDIR)/"
	mkdir -p "$(BUILDDIR)"
	mkdir -p "$(BUILDDIR)/DEBIAN"
	cat "control" | sed "s/PKGNAME/$(PKGNAME)/g" \
                | sed "s/VERSION/$(VERSION)/g" \
                | sed "s/ARCH/$(ARCH)/g" \
                > "$(BUILDDIR)/DEBIAN/control"
	cp preinst "$(BUILDDIR)/DEBIAN/"
	cp postinst "$(BUILDDIR)/DEBIAN/"
	dpkg-deb --build --root-owner-group "$(BUILDDIR)"


install: $(DEBFILE)
	dpkg -i "$(DEBFILE)"


clean:
	rm -rf build tmp
