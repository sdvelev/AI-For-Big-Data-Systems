% Facts

direct_path(c00, c10).
direct_path(c10, c11).
direct_path(c10, c20).
direct_path(c20, c30).
direct_path(c30, c40).
direct_path(c40, c41).
direct_path(c41, c42).
direct_path(c42, c43).
direct_path(c42, c32).
direct_path(c43, c33).
direct_path(c33, c32).
direct_path(c32, c22).
direct_path(c22, c12).
direct_path(c11, c12).
direct_path(c12, c02).
direct_path(c12, c13).
direct_path(c02, c03).
direct_path(c13, c03).
direct_path(c13, c14).
direct_path(c03, c04).
direct_path(c04, c05).
direct_path(c04, c14).
direct_path(c14, c15).
direct_path(c14, c24).
direct_path(c24, c25).
direct_path(c05, c15).
direct_path(c15, c25).
direct_path(c25, c35).
direct_path(c35, c45).

% Rules
move(X, Y) :- direct_path(X, Y).
move(X, Y) :- direct_path(Y, X).

path() :- path(_).

inter_path(S, F, _, [S, F]) :-
    move(S, F).

inter_path(S, F, Visit, [S | Rest]) :-
    move(S, Z),
    Z \= F,
    not(member(Z, Visit)),
    inter_path(Z, F, [S | Visit], Rest).

path(Path) :-
    inter_path(c00, c45, [], Path),
    write(Path), nl.

all_paths(Visit, Path) :-
    findall(Path, (Visit = [], inter_path(c00, c45, Visit, Path)), Z),
    write(Z), nl.