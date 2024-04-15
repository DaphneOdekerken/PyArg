is_in(X) :- topic(X), lab(in,X).
is_out(X) :- topic(X), lab(out,X).
is_undec(X) :- topic(X), lab(undec,X).

#show is_in/1.
#show is_out/1.
#show is_undec/1.