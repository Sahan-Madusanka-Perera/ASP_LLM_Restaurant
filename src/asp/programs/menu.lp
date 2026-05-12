% Menu Definition
% format: item(ID, Category, Price).
item(margherita, pizza, 12).
item(pepperoni, pizza, 14).
item(veggie, pizza, 13).
item(hawaiian, pizza, 14).

item(coke, drink, 3).
item(sprite, drink, 3).
item(water, drink, 2).

item(fries, side, 5).
item(garlic_bread, side, 6).

% Availability (everything is available by default except sprite right now)
available(X) :- item(X, _, _), X != sprite.

% Categories for easier reasoning
is_pizza(X) :- item(X, pizza, _).
is_drink(X) :- item(X, drink, _).
is_side(X) :- item(X, side, _).
