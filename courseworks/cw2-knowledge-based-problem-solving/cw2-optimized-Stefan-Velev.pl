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

optimal_path() :- optimal_path([], _, _).

inter_path(S, F, Visit, [S, F], PathLength) :-
    move(S, F),
    PathLengthIncreased is PathLength + 1,
    nb_getval(globalMinPath, CurrentMinPath),
    PathLengthIncreased =< CurrentMinPath,
    nb_setval(globalMinPath, PathLengthIncreased).

inter_path(S, F, Visit, [S | Rest], PathLength) :-
    move(S, Z),
    Z \= F,
    not(member(Z, Visit)),
    PathLengthIncreased is PathLength + 1,
    nb_getval(globalMinPath, CurrentMinPath),
    PathLengthIncreased =< CurrentMinPath,
    inter_path(Z, F, [S | Visit], Rest, PathLengthIncreased).

% Selects paths that are of a given length
compare_path_length(PathList, PathLength, OptimalPath) :-
    member(A, PathList),
    length(A, CurrentPathLength),
    CurrentPathLength = PathLength,
    OptimalPath = A.

optimal_path(Visit, Path, PathLength) :-
    nb_setval(globalMinPath, 1000),
    PathLength = 1,
    findall(Path, (Visit = [], inter_path(c00, c45, Visit, Path, PathLength)), PathList),
    nb_getval(globalMinPath, PrintPath),
    compare_path_length(PathList, PrintPath, OptimalPath),
    write(OptimalPath), nl.

all_optimal_paths(Visit, Path, PathLength) :-
    nb_setval(globalMinPath, 1000),
    PathLength = 1,
    findall(Path, (Visit = [], inter_path(c00, c45, Visit, Path, PathLength)), PathList),
    nb_getval(globalMinPath, PrintPath),
    findall(OptimalPath, compare_path_length(PathList, PrintPath, OptimalPath), PathListOptimal),
    write(PathListOptimal), nl.