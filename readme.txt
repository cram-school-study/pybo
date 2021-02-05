sqlite -> mariadb 연결 바로 지원하지않음.
mysql을 사용하여 연결 과정 필요

[문제] sqlite3 사용 후 db를 변경하면 migrate시 아래와 같은 에러가 발생함.
ERROR [root] Error: Target database is not up to 
https://tinyurl.com/y5wo3dlm

* orm 현재 사용 중이니, sqlite3에서도 프로시저 구성이 가능한지 여부!
* 만약 구성이 불가능하다면 mariadb 구성 후에 프로시저로 만들어보고 해보도록 하기 -> 해당 부분만 교체하면 되는것인지 확인 필요
* 가능하면 mariadb -> mssql or oracle 마이그레이션 작업도 해보자~

* sqlite3 -> mariadb 마이그레이션 작업 해볼 것! (orm의 장점 활용)
1. sqlite의 값이 빈 상태일 경우에서 마이그레이션
2. sqlite의 값이 쌓인 상태로 마이그레이션
-> 초창기 세팅을 바꾸고 들어가는 환경과, 기존 고객사 데이터가 쌓여있는 도중에 들어가는 환경 구분 테스트

