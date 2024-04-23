premise(a).
premise(b).
premise(c).

strict_head(1,x).
strict_body(1,z).
strict_body(1,y).

head(2,y).
body(2,a).

head(3,z).
body(3,b).

head(4,nx).
body(4,c).

contradictory(x,nx).
%contradictory(c,a).


%%% INPUT
%in(a).
%in(b).
%in(2).
%in(3).
preferred(4,2).
