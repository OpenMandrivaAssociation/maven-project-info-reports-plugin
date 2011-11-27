Name:           maven-project-info-reports-plugin
Version:        2.2
Release:        8
Summary:        Maven Project Info Reports Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-project-info-reports-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
#- Modified maven version from 2.1.0 to 2.0.8 which is available now in koji,
#  will remove this from patch once maven is upgraded to version 2.2.1.
#- Removed junit-addons dependency as there is no junit-addons available in koji, meanwhile set test skip as true.
Patch0:        %{name}-pom.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: apache-commons-parent
BuildRequires: maven-plugin-plugin
BuildRequires: maven-shared-reporting-api
BuildRequires: maven-shared-reporting-impl
BuildRequires: maven-shared-dependency-tree 
BuildRequires: maven-doxia-tools
BuildRequires: maven-shared-jar
BuildRequires: maven-wagon
BuildRequires: maven-scm
BuildRequires: maven-doxia
BuildRequires: plexus-container-default
BuildRequires: plexus-component-api
BuildRequires: plexus-i18n
BuildRequires: plexus-utils
BuildRequires: apache-commons-validator
BuildRequires: httpunit
BuildRequires: maven-plugin-testing-harness
BuildRequires: servlet25
BuildRequires: netbeans-cvsclient

Requires:       maven2
Requires:       java
Requires:       jpackage-utils
Requires:       plexus-container-default
Requires:       plexus-component-api
Requires:       plexus-i18n
Requires:       plexus-utils
Requires:       apache-commons-validator
Requires:       httpunit
Requires:       servlet25

Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

Obsoletes: maven2-plugin-project-info-reports <= 0:2.0.8
Provides: maven2-plugin-project-info-reports = 0:%{version}-%{release}

%description
The Maven Project Info Reports Plugin is a plugin 
that generates standard reports for the specified project.
  

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q 
%patch0 -p0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -Dpm 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins %{name} %{version} JPP %{name}

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

