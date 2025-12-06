# TODO: system lexicon, yaml
# completions (bash, fish, zsh: invoke/completion/*.completion)
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

%define		module		invoke
Summary:	Managing shell-oriented subprocesses and organizing executable Python code into CLI-invokable tasks
Summary(pl.UTF-8):	Zarządzanie podprocesami powłoki i organizowanie kodu Pythona w zadania wywoływane z CLI
Name:		python3-%{module}
Version:	2.2.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/invoke/
Source0:	https://files.pythonhosted.org/packages/source/i/invoke/%{module}-%{version}.tar.gz
# Source0-md5:	4dc9b866df5e3835fe180197d1d112d2
URL:		https://www.pyinvoke.org/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:56
%if %{with tests}
BuildRequires:	python3-icecream >= 2.1
#BuildRequires:	python3-invocations >= 3.3
BuildRequires:	python3-pytest >= 4.6.3
BuildRequires:	python3-pytest-relaxed >= 2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-alabaster >= 0.7.12
BuildRequires:	python3-releases >= 2
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Invoke is a Python task execution tool & library, drawing inspiration
from various sources to arrive at a powerful & clean feature set.

%description -l pl.UTF-8
Invoke to narzędzie i biblioteka do uruchamiania zadań napisanych w
Pythonie, czerpiąca inspiracje z różnych źródeł, dostarczająca duży i
i czysty zbiór możliwości.

%package apidocs
Summary:	API documentation for Python invoke module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona invoke
Group:		Documentation

%description apidocs
API documentation for Python invoke module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona invoke.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# many failures in runners.py because of stdin catching(?)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_relaxed.plugin \
%{__python3} -m pytest tests -k 'not Runner_ and not Local_'
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html sites/docs sites/docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/inv{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/invoke{,-3}
ln -s inv-3 $RPM_BUILD_ROOT%{_bindir}/inv
ln -s invoke-3 $RPM_BUILD_ROOT%{_bindir}/invoke

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/inv-3
%attr(755,root,root) %{_bindir}/invoke-3
%{_bindir}/inv
%{_bindir}/invoke
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc sites/docs/_build/html/{_static,api,concepts,*.html,*.js}
%endif
