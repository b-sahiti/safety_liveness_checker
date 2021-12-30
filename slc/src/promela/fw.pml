bool r0=1;
bool r1=1;
bool r2=1;
bool r3=1;
bool r4=1;
bool r5=1;


proctype A0(){
      (r0==1) -> r0=0;r1=0;r3=0;
}

proctype A1(){
     (r1==1) -> r0=0;r1=0;r4=0;
}

init
{
    run A0();
    run A1();
    }
