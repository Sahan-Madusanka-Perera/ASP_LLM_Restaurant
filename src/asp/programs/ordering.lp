% Ordering logic and calculations

% If a request is valid and passes constraints, it becomes an official order
order(X) :- request(X).

% Calculate totals (simplified for now, assumes quantity 1 per unique item)
% In a real scenario, we'd add quantities: request(Item, Quantity).
total_price(S) :- S = #sum { P, X : order(X), item(X, _, P) }.

% Output the final confirmed orders and total
#show order/1.
#show total_price/1.
