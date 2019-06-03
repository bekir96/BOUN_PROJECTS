% bekir yildirim
% 2014400054
% compiling: yes
% complete: yes

:- [pokemon_data].

%pokemon_types(+TypeList, +InitialPokemonList, -PokemonList)
%This predicate will be used to find every Pok´emon from InitialPokemonList that are at least one of
%the types from TypeList.
%Conditions in setof:
%1-member of InitialPokemonList
%2-pokemon-types-2
pokemon_types(TypeList, InitialPokemonList, PokemonList) :-
    setof(Pokemon, (member(Pokemon, InitialPokemonList), pokemon_types_2(TypeList, Pokemon)) , PokemonList).

%pokemon_types_2 provides if member of PokemonTypes in TypeList, stop.
pokemon_types_2([H|TypeList], Pokemon) :-
    pokemon_stats(Pokemon, PokemonTypeList, _, _, _),
    (member(H, PokemonTypeList); pokemon_types_2(TypeList, Pokemon)).

%find_pokemon_evolution(+PokemonLevel, +Pokemon, -EvolvedPokemon)
%is recursive function and enter until PokemonLevel do not exceed the requirement level that can evolve or do not find evolution stats on knowledge base.
%at the end in fail situation, put cut in order to get print all evolvedpokemon members.
find_pokemon_evolution(PokemonLevel, Pokemon, EvolvedPokemon) :- 
    (pokemon_evolution(Pokemon, X, RQ1) , RQ1 =< PokemonLevel , find_pokemon_evolution(PokemonLevel,X,EvolvedPokemon),!)
    ;EvolvedPokemon = Pokemon.

%pokemon_level_stats(+PokemonLevel, ?Pokemon, -PokemonHp, -PokemonAttack, -PokemonDefense)
%This predicate evaluates the statistics of a Pokemon for the given level. With every level a Pokemon
%gains 2 health points, 1 attack point and 1 defense point. You can get the base statistics from pokemon_stats.
pokemon_level_stats(PokemonLevel, Pokemon, PokemonHp, PokemonAttack, PokemonDefense) :-
    pokemon_stats(Pokemon, _, Hp, Attack, Defense),
    PokemonHp is PokemonLevel * 2 + Hp,
    PokemonAttack is PokemonLevel + Attack,
    PokemonDefense is PokemonLevel + Defense.

%single_type_multiplier(?AttackerType, ?DefenderType, ?Multiplier)
%This predicate will be used to find single-type advantage/disadvantage multiplier. It can also be used
%to find types that achieves a given multiplier.
%In this predicate, type_chart_attack and type_method is used.
%This 2 method ensure that trueness of 3 parameters of predicate.  
single_type_multiplier(AttackerType, DefenderType, Multiplier) :-
    pokemon_types(PokemonTypes),
    (type_chart_attack(AttackerType, TypeMultipliers), type_method(DefenderType,  PokemonTypes, TypeMultipliers, Multiplier )).

%base case of type_method provide that DefenderType and Multiplier match PokemonTypes and TypeMultipliers.
type_method(DefenderType, [DefenderType|_], [Multiplier|_], Multiplier).

%This recursive function provides iterates PokemonTypes until ensure base case.
type_method(DefenderType, [Head1|PokemonTypes], [Head2|TypeMultipliers], Multiplier) :-
    type_method(DefenderType, PokemonTypes, TypeMultipliers, Multiplier).

%type_multiplier(?AttackerType, +DefenderTypeList, ?Multiplier)
%This predicate will be used to find double-type advantage/disadvantage multiplier. It can also be
%used to find types that achieves a given multiplier.
%In this predicate, type_chart_attack, type_multiplier_2 and  list_multiply
%This 3 method ensure that trueness of 3 parameters of predicate.  
type_multiplier(AttackerType, DefenderTypeList, Multiplier) :-
    type_chart_attack(AttackerType, TypeMultipliers), type_multiplier_2(AttackerType, DefenderTypeList, MultiplierList), list_multiply(MultiplierList, Multiplier).


%base case of type_multiplier_2 provide that iterates DefenderTypeList and Multiplier shall stop.
type_multiplier_2(_, [], []).

%This predicates construct MultiplierList with recursive function and single_type_multiplier.
type_multiplier_2(AttackerType, [Head1|DefenderTypeList], [Head2|Multiplier]) :-
    single_type_multiplier(AttackerType, Head1, Head2),
    type_multiplier_2(AttackerType, DefenderTypeList, Multiplier),!.


%base case of list_multiply
list_multiply([],0).
%At the end of iteration, to dfs, fill Product.
list_multiply([Head],Head).
%Recursive function of list_multiply 
list_multiply([Head|Tail], Product) :-
    list_multiply(Tail, Rest), Product is Head * Rest,!.

%pokemon_type_multiplier(?AttackerPokemon, ?DefenderPokemon, ?Multiplier)
%This predicate will be used to find type multiplier between two Pok´emon. It can also be used to find
%different attacker/defender Pok´emon that achieves a given multiplier. If an attacker Pok´emon has two
%types, then the Pok´emon uses the type that gives the higher multiplier against the defender Pok´emon.
%This predicate use pokemon_stats, pokemon_type_multiplier_2 and max_ element to this aim.
pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier) :-
    pokemon_stats(AttackerPokemon, AttackerList, _, _, _),
    pokemon_stats(DefenderPokemon, DefenderTypeList, _, _, _),
    pokemon_type_multiplier_2(AttackerList, DefenderTypeList, MultiplierList),
    max_element(MultiplierList, Multiplier).

%Recursive function of max element to use in H<Y
max_element([H|T], Y):- 
    max_element(T, Y),
    H < Y,!.
%Recursive function of max element to use in H>=Y
max_element([H|T], H):-
    max_element(T,Y),
    H >= Y,!.
%base case of max_element
max_element([X],X).

%base case of pokemon_type_multiplier_2 provide that iterates AttackerList and MultiplierList shall stop.
pokemon_type_multiplier_2([],_,[]).

%This predicate use type_multiplier and recursive function.
pokemon_type_multiplier_2([Head1|AttackerList], DefenderTypeList, [Head2|MultiplierList]) :-
    type_multiplier(Head1, DefenderTypeList, Head2),
    pokemon_type_multiplier_2(AttackerList, DefenderTypeList, MultiplierList),!.

%pokemon_attack(+AttackerPokemon, +AttackerPokemonLevel, +DefenderPokemon, +DefenderPokemonLevel, -Damage)
%This predicate finds the damage dealt from the attack of the AttackerPokemon to the DefenderPokemon.
%Damage = (0.5 × AttackerPokemonLevel × (AttackerPokemonAttack / DefenderPokemonDefense) × TypeMultiplier) + 1
%This predicate use pokemon_stats and pokemon_type_multiplier to this aim.
pokemon_attack(AttackerPokemon, AttackerPokemonLevel, DefenderPokemon, DefenderPokemonLevel, Damage) :-
    pokemon_type_multiplier(AttackerPokemon, DefenderPokemon, Multiplier),
    pokemon_level_stats(AttackerPokemonLevel, AttackerPokemon, AttackerHp, AttackerAttack, AttackerDefense),
    pokemon_level_stats(DefenderPokemonLevel, DefenderPokemon, DefenderHp, DefenderAttack, DefenderDefense),
    pokemon_stats(AttackerPokemon, AttackerList, _, _, _),
    pokemon_stats(DefenderPokemon, DefenderList, _, _, _),
    Damage is 0.5 * AttackerPokemonLevel * (AttackerAttack / DefenderDefense) * Multiplier + 1.

%pokemon fight(+Pokemon1, +Pokemon1Level, +Pokemon2, +Pokemon2Level, -Pokemon1Hp, -Pokemon2Hp, -Rounds)
%This predicate simulates a fight between two Pok´emon then finds health points of each Pok´emon at
%the end of the fight and the number of rounds. Each Pok´emon attacks at the same time and each
%attack sequence count as one round. After each attack, health points of each Pok´emon reduced by
%the amount of calculated damage points. When a Pok´emon’s health points reach or drop below zero
%(HP <= 0), the fight ends.
%This predicate use pokemon_level_stats, pokemon_attack and pokemon_fight_2 to this aim.
%To reach Rounds, Temp is defined.
%At the end, after the pokemon_fight_2 Pokemon1Hp and Pokemon2Hp > 0 so one more decrease is defined.
pokemon_fight(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level, Pokemon1Hp, Pokemon2Hp, Rounds) :- 
    Temp is 0,
    pokemon_level_stats(Pokemon1Level, Pokemon1, AttackerHp1, _, _),
    pokemon_level_stats(Pokemon2Level, Pokemon2, AttackerHp2, _, _),
    pokemon_attack(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level, Damage1) , pokemon_attack(Pokemon2, Pokemon2Level, Pokemon1, Pokemon1Level, Damage2),
    pokemon_fight_2(AttackerHp1, AttackerHp2, Temp, Damage1, Damage2, Pokemon1X, Pokemon2X, TempX),
    Pokemon1Hp is Pokemon1X - Damage2,
    Pokemon2Hp is Pokemon2X - Damage1,
    Rounds is TempX + 1,!.

%pokemon_fight_2 is recursive predicate and trueness of this predicate is provided according to health point > 0 
% at the end, health points transfer Temp definition.
pokemon_fight_2(Pokemon1Hp, Pokemon2Hp, Temp, Damage1, Damage2, Pokemon1X, Pokemon2X, TempX) :-
    Pokemon1Temp is Pokemon1Hp - Damage2,
    Pokemon2Temp is Pokemon2Hp - Damage1,
    Temp2 is Temp + 1,
    ((Pokemon1Temp > 0 , Pokemon2Temp > 0), pokemon_fight_2(Pokemon1Temp, Pokemon2Temp, Temp2, Damage1, Damage2, Pokemon1X, Pokemon2X, TempX))
    ;(Pokemon1X is Pokemon1Hp, Pokemon2X is Pokemon2Hp, TempX is Temp),!.

%pokemon tournament(+PokemonTrainer1, +PokemonTrainer2, -WinnerTrainerList)
%This predicate simulates a tournament between two Pok´emon trainers then finds the winner Pok´emon
%trainer of each fight. Pok´emon trainers must have the same number of Pok´emon. Pok´emon fights
%in order. First Pok´emon of the first Pok´emon trainer fights with the first Pok´emon of the second
%Pok´emon trainer, second Pok´emon of the first Pok´emon trainer fights with the second Pok´emon of
%the second Pok´emon trainer. A fight ends when a Pok´emon’s health points drop below zero. At the
%end of the fight, Pok´emon with more health points win the fight, so does the Pok´emon trainer that
%owns the winner Pok´emon. In case of a tie, PokemonTrainer1 wins. 
%This predicate use pokemon_trainer and pokemon_X to this aim.
pokemon_tournament(PokemonTrainer1, PokemonTrainer2, WinnerTrainerList) :-
    pokemon_trainer(PokemonTrainer1, PokemonTeam1, PokemonLevel1),
    pokemon_trainer(PokemonTrainer2, PokemonTeam2, PokemonLevel2),
    pokemon_X(PokemonTeam1, PokemonTeam2, PokemonLevel1, PokemonLevel2, PokemonTrainer1, PokemonTrainer2, WinnerTrainerList),!.

%base case of pokemon_type_multiplier_2 provide that iterates PokemonTeam1, PokemonTeam2, PokemonLevel1, PokemonLevel2 and WinnerTrainerList shall stop.
pokemon_X([], [], [], [], PokemonTrainer1, PokemonTrainer2, []).

%pokemon_X iterate PokemonTeam1, PokemonTeam2, WinnerTrainerList and at each iteration 
%fill WinnerTrainerList by who wins fight(PokemonTrainer)
pokemon_X([HeadPokemon1|PokemonTeam1], [HeadPokemon2|PokemonTeam2], [HeadLevel1|PokemonLevel1], [HeadLevel2|PokemonLevel2], PokemonTrainer1, PokemonTrainer2, [Head|WinnerTrainerList]) :-
    (find_pokemon_evolution(HeadLevel1, HeadPokemon1, EvolvedPokemon1), find_pokemon_evolution(HeadLevel2, HeadPokemon2, EvolvedPokemon2),
    pokemon_fight(EvolvedPokemon1, HeadLevel1, EvolvedPokemon2, HeadLevel2, Pokemon1Hp, Pokemon2Hp, _),
    ((Pokemon1Hp >= Pokemon2Hp, Head = PokemonTrainer1) 
    ;(Pokemon2Hp > Pokemon1Hp, Head = PokemonTrainer2)),
    pokemon_X(PokemonTeam1, PokemonTeam2, PokemonLevel1, PokemonLevel2, PokemonTrainer1, PokemonTrainer2, WinnerTrainerList)).

%best pokemon(+EnemyPokemon, +LevelCap, -RemainingHP, -BestPokemon)
%This predicate finds the best Pok´emon against the given EnemyPokemon where the both Pok´emon’s
%levels are LevelCap. We define the best Pok´emon as the Pok´emon with the
%most remaining health points after the fight.
%This predicate use pokemon_level_stats, all_members for take all Pokemons and best_pokemon_2 to this aim.
best_pokemon(EnemyPokemon, LevelCap, RemainingHP, BestPokemon) :-
    pokemon_level_stats(LevelCap, EnemyPokemon, EnemyPokemonHp, EnemyPokemonAttack, EnemyPokemonDefense),
    all_members(PokemonList),
    best_pokemon_2(PokemonList, Hp, LevelCap, EnemyPokemon, _,  RemainingHP , _, BestPokemon),!.

%This predicate use for one temporary Hp for base compare Hp and transfer best_pokemon_3
best_pokemon_2([Head | PokemonList], Hp, LevelCap, EnemyPokemon, _,  RemainingHP , _, BestPokemon) :-
    pokemon_fight(Head, LevelCap, EnemyPokemon, LevelCap, Pokemon1Hp, Pokemon2Hp, _),
    best_pokemon_3(PokemonList, Pokemon1Hp, LevelCap, EnemyPokemon, HpTemp, RemainingHP, Head, BestPokemon),!.

%base case of best_pokemon_3 provide that iterates PokemonList shall stop and set RemaininHp and BestPokemon.
best_pokemon_3([], Hp, _, _, _, Hp, BestPokemonTemp, BestPokemonTemp).

%This predicate iterates PokemonList and check if better pokemon and to the result go to 2 different iteration.
%To maintain RemaininHp and BestPokemon, HpTemp and BestPokemonTemp is defined.
best_pokemon_3([Head|PokemonList], Hp, LevelCap, EnemyPokemon, HpTemp, BestPokemonHp, BestPokemonTemp, BestPokemon) :-
    pokemon_fight(Head, LevelCap, EnemyPokemon, LevelCap, Pokemon1Hp, Pokemon2Hp, _),
    ((Pokemon1Hp > Pokemon2Hp , Pokemon1Hp > Hp , HpTemp is Pokemon1Hp, best_pokemon_3(PokemonList, HpTemp, LevelCap, EnemyPokemon, NewHpTemp, BestPokemonHp, Head, BestPokemon)) ;
    best_pokemon_3(PokemonList, Hp, LevelCap, EnemyPokemon, HpTemp, BestPokemonHp, BestPokemonTemp, BestPokemon)).   

%Hold the all Pokemons.
all_members(List) :-
    findall(Pokemon, pokemon_stats(Pokemon, _, _, _, _), List).

%best pokemon team(+OpponentTrainer, -PokemonTeam)
%This predicate finds the best Pok´emon Team against the given OpponentTrainer where the levels of
%each Pok´emon of our best Pok´emon Team are the same with the corresponding Opponent’s Pok´emon
%levels (e.g. Level of the first Pok´emon of the best Pok´emon Team is same with the level of the first
%Pok´emon of the Opponent Trainer). Both Pokemon should be evolved according to their level before
%fighting like in the tournament. We define the best Pok´emon as the Pok´emon with the most remaining
%health points after the fight.
%This predicate use pokemon_trainer, best_pokemon_team_1 to this aim.
best_pokemon_team(OpponentTrainer, PokemonTeam) :-
    pokemon_trainer(OpponentTrainer, EnemyTeam, EnemyPokemonLevels),
    best_pokemon_team_1(EnemyTeam, EnemyPokemonLevels, PokemonTeam),!.

%base case of best_pokemon_3 provide that iterates EnemyTeam, EnemyPokemonLevels and PokemonTeam  shall stop.
best_pokemon_team_1([],[],[]).

%best_pokemon_team_1 iterates EnemyTeam, EnemyPokemonLevels and PokemonTeam and at each iteration
%finds best pokemon to one member of EnemyTeam
best_pokemon_team_1([Head1|EnemyTeam],[Head2|EnemyPokemonLevels],[Head3|PokemonTeam]) :-
    best_pokemon(Head1, Head2, _, Head3),
    best_pokemon_team_1(EnemyTeam, EnemyPokemonLevels, PokemonTeam).

%generate pokemon team(+LikedTypes, +DislikedTypes, +Criterion, +Count, -PokemonTeam)
%This predicate generates a Pok´emon team based on liked and disliked types and some criteria. This
%team can only have Pok´emon from LikedTypes and can’t have Pok´emon from DislikedTypes. The
%predicate sorts Pok´emon according to one of the three criterion in descending order: health points
%(h), attack (a), defense (d). Then selects Count number of Pok´emon that have highest values in the
%selected criterion. If two or more Pok´emon has the same value, the order is not important between
%these Pok´emon.
%This predicate use findall, remove_list, create_list, quick_sort2 and liked_pokemon_team to this aim.
%Conditions in findall1:
%1-at least one LikedTypes 
%2-pokemon_stats
%Conditions in findall2:
%1-at least one DislikedTypes 
%2-pokemon_stats
generate_pokemon_team(LikedTypes, DislikedTypes, Criterion, Count, PokemonTeam) :-
    findall(LikedPokemon, (pokemon_stats(LikedPokemon, LikedPokemonTypes, _, _, _), generate_pokemon(LikedTypes, LikedPokemon, 0, Control), Control >= 1), LikedPokemonList),
    findall(DislikedPokemon, (pokemon_stats(DislikedPokemon, _, _, _, _), generate_pokemon(DislikedTypes, DislikedPokemon, 0, Control), Control >= 1), DislikedPokemonList),
    remove_list(LikedPokemonList, DislikedPokemonList, SortingPokemonList),
    create_list(SortingPokemonList, List, Criterion),
    quick_sort2(List, SortedList),
    liked_pokemon_team(Count, SortedList, PokemonTeam),!.

%To take first count elements from Sorted List.
liked_pokemon_team(N, _, Xs) :- N =< 0, !, N =:= 0, Xs = [].
liked_pokemon_team(_, [], []).
liked_pokemon_team(N, [[Head2,Head1]|Tail1],[[Head1,H1,H2,H3]|Tail2]) :- pokemon_stats(Head1, _, H1, H2, H3), M is N-1, liked_pokemon_team(M, Tail1, Tail2).

%base case of create_list provide that iterates SortingPokemonList, List shall stop.
create_list([],[],_).

%create_list create List which each element have Pokemon and Criterion elements.
create_list([Head1|SortingPokemonList], [[Head2,Head1]|List], Criterion):-
    ((Criterion == h , pokemon_stats(Head1, _, Head2, _, _))
    ;(Criterion == a, pokemon_stats(Head1, _, _, Head2, _))
    ;(Criterion == d, pokemon_stats(Head1, _, _, _ , Head2)))
    ,create_list(SortingPokemonList, List, Criterion),!.

%base case of generate_pokemon
generate_pokemon([], _, Control, Control).

%iterates LikedTypes and if Pokemon Types have member of LikedTypes, control increasing.
generate_pokemon([Head1|Types], Pokemon, Temp, Control):-
    pokemon_stats(Pokemon, PokemonTypes, _, _, _),
    ((member(Head1, PokemonTypes), NewTemp is Temp + 1)
    ;(NewTemp is Temp)),
    generate_pokemon(Types, Pokemon, NewTemp, Control),!.

%remove_list create new List by substract one list to other list.
remove_list([], _, []).
remove_list([X|Tail], L2, Result):- member(X, L2), !, remove_list(Tail, L2, Result). 
remove_list([X|Tail], L2, [X|Result]):- remove_list(Tail, L2, Result).

%quick sort algorithm to one criterion.
quick_sort2(List,Sorted):-q_sort(List,[],Sorted).
q_sort([],Acc,Acc).
q_sort([[H1,H2]|T],Acc,Sorted):-
	pivoting([H1,H2],T,L1,L2),
	q_sort(L1,Acc,Sorted1),q_sort(L2,[[H1,H2]|Sorted1],Sorted).

pivoting([H1,H2],[],[],[]).
pivoting([H1,H2],[[H3,H4]|T],[[H3,H4]|L],G):-H3=<H1,pivoting([H1,H2],T,L,G).
pivoting([H1,H2],[[H3,H4]|T],L,[[H3,H4]|G]):-H3>H1,pivoting([H1,H2],T,L,G).