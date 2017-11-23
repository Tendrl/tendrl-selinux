# based on Makefile of tendrl-ansible
NAME = tendrl-selinux
VERSION = 1.5.4
COMMIT := $(shell git rev-parse HEAD)
SHORTCOMMIT := $(shell echo $(COMMIT) | cut -c1-7)

# based on example fedora wikipage
# https://fedoraproject.org/wiki/SELinux/IndependentPolicy
TARGETS?=tendrl carbon collectd grafana
MODULES?=${TARGETS:=.pp.bz2}
DATADIR?=/usr/share

all: srpm
modules: ${TARGETS:=.pp.bz2}

%.pp.bz2: %.pp
	@echo Compressing $^ -\> $@
	bzip2 -9 $^

%.pp: %.te
	make -f ${DATADIR}/selinux/devel/Makefile $@

clean:
	rm -f *~  *.tc *.pp *.pp.bz2
	rm -rf tmp *.tar.gz
	rm -f collectd.fc collectd.if grafana.if
	rm -rf $(NAME)-$(VERSION)
	rm -f $(NAME)-$(VERSION).tar.gz
	rm -f $(NAME)-$(VERSION)*.rpm
	rm -f *.log

dist: clean
	mkdir $(NAME)-$(VERSION)
	cp LICENSE $(NAME)-$(VERSION)
	cp README.md $(NAME)-$(VERSION)
	cp Makefile $(NAME)-$(VERSION)
	cp ${TARGETS:=.te} $(NAME)-$(VERSION)
	cp carbon.if $(NAME)-$(VERSION)
	cp tendrl.if $(NAME)-$(VERSION)
	cp carbon.fc $(NAME)-$(VERSION)
	cp tendrl.fc $(NAME)-$(VERSION)
	cp grafana.fc $(NAME)-$(VERSION)
	tar caf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION)

srpm: dist
	fedpkg --dist epel7 srpm

rpm: srpm
	mock -r epel-7-x86_64 rebuild $(NAME)-$(VERSION)-*.src.rpm --resultdir=. --define "dist .el7"

gitversion:
	# Set version and release to the latest values from Git
	sed -i $(NAME).spec \
	  -e "/^Release:/cRelease: $(shell date +"%Y%m%dT%H%M%S").$(SHORTCOMMIT)"

snapshot: gitversion srpm

.PHONY: dist rpm srpm gitversion snapshot
