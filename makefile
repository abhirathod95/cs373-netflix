FILES :=                              \
    Netflix.html                      \
    Netflix.log                       \
    Netflix.py                        \
    RunNetflix.in                     \
    RunNetflix.out                    \
    RunNetflix.py                     \
    TestNetflix.out                   \
    TestNetflix.py                    \
    netflix-tests/ajr3334-aaj742-RunNetflix.in \
    netflix-tests/ajr3334-aaj742-RunNetflix.out  \
    netflix-tests/ajr3334-aaj742-TestNetflix.out \
    netflix-tests/ajr3334-aaj742-TestNetflix.py  \

.pylintrc:
	pylint --disable=bad-whitespace,missing-docstring,pointless-string-statement --reports=n --generate-rcfile > $@

netflix-tests:
	git clone https://github.com/CS373-Fall-2016/netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.tmp: RunNetflix.in RunNetflix.out RunNetflix.py
	-pylint Netflix.py
	-pylint RunNetflix.py
	python3.5 RunNetflix.py < RunNetflix.in > RunNetflix.out

TestNetflix.tmp: TestNetflix.py
	-pylint Netflix.py
	-pylint TestNetflix.py
	python3.5 -m coverage run    --branch TestNetflix.py >  TestNetflix.tmp 2>&1
	python3.5 -m coverage report -m --omit=/lusr/lib/python3.5/dist-packages/*,/home/travis/virtualenv/python3.5.0/lib/python3.5/site-packages/* >> TestNetflix.tmp
	cat TestNetflix.tmp 					 >  TestNetflix.out
	cat TestNetflix.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__

config:
	git config -l

format:
	autopep8 -i Netflix.py
	autopep8 -i RunNetflix.py
	autopep8 -i TestNetflix.py

scrub:
	make clean
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -rf netflix-tests

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

versions:
	pip --version
	coverage --version
	pylint --version
	pydoc3 --version

test: Netflix.html Netflix.log RunNetflix.tmp TestNetflix.tmp netflix-tests check