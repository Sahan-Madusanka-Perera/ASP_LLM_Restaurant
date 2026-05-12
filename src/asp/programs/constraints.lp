% Constraints

% A user cannot order an item that does not exist on the menu.
:- request(X), not item(X, _, _).

% A user cannot order an item that is currently unavailable.
:- request(X), not available(X).

% Dietary constraints: 
% Let's say user specifies vegetarian requirement
% :- requirement(vegetarian), request(X), not is_vegetarian(X).
% is_vegetarian(margherita).
% is_vegetarian(veggie).
% is_vegetarian(fries).
% is_vegetarian(garlic_bread).
% is_vegetarian(X) :- is_drink(X).

% For this phase, we just flag error states
error(invalid_item, X) :- request(X), not item(X, _, _).
error(unavailable, X) :- request(X), not available(X).

% A model is valid only if there are no errors (Hard Constraint)
:- error(_, _).
