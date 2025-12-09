from matchers import And, HasAtLeast, PlaysIn, All, HasFewerThan, Or

class QueryBuilder:
    def __init__(self, matchers=All()):
        self._matchers = matchers

    def build(self):
        return self._matchers

    def has_at_least(self, value, attr):
        return QueryBuilder(And((self._matchers), HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(And((self._matchers), HasFewerThan(value, attr)))

    def plays_in(self, team):
        return QueryBuilder(And((self._matchers), PlaysIn(team)))

    def one_of(self, *builders):
        matchers = [build.build() for build in builders]
        return QueryBuilder(Or(*matchers))
