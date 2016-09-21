FILES :=                              \
    Netflix.html                      \
    Netflix.log                       \
    Netflix.py                        \
    RunNetflix.in                     \
    RunNetflix.out                    \
    RunNetflix.py                     \
    TestNetflix.out                   \
    TestNetflix.py                    \
 #   netflix-tests/ajr3334-RunCollatz.in   \
 #   netflix-tests/ajr3334-RunCollatz.out  \
 #   netflix-tests/ajr3334-TestCollatz.out \
 #   netflix-tests/ajr3334-TestCollatz.py  \

netflix-tests:
	git clone https://github.com/CS373-Fall-2016/netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunCollatz.tmp: RunNetflix.in RunNetflix.out RunNetflix.py
	./RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	diff RunNetflix.tmp RunNetflix.out

TestNetflix.tmp: TestNetflix.py
	python3.5 -m coverage run    --branch TestNetflix.py >  TestNetflix.tmp 2>&1
	python3.5 -m coverage report -m                      >> TestNetflix.tmp
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

#test: scrub Netflix.html Netflix.log RunNetflix.tmp TestNetflix.tmp netflix-tests check
test: scrub 